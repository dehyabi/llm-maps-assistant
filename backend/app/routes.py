from fastapi import APIRouter, Request
from .schemas import SearchRequest, PlaceDetailsRequest, DirectionsRequest, SearchResponse, DetailsResponse, DirectionsResponse, EmbedPlaceResponse, EmbedDirectionsResponse
from .google_maps import GoogleMapsClient
from .config import get_settings
from .rate_limit import limiter
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import httpx
import json

from .llm_client import OllamaClient

router = APIRouter()

# LLM Chat Schema
class ChatMessage(BaseModel):
    role: str
    content: str

class LLMChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class LLMChatResponse(BaseModel):
    response: str
    map_data: Dict[str, Any] | None = None

@router.post("/search", response_model=SearchResponse)
@limiter.limit("10/10 seconds")
async def search_places(request: Request, payload: SearchRequest) -> SearchResponse:
    client = GoogleMapsClient()
    try:
        data = await client.text_search(payload.query, payload.location, payload.radius)
        return SearchResponse(raw=data)
    finally:
        await client.close()

@router.post("/place", response_model=DetailsResponse)
@limiter.limit("30/minute")
async def place_details(request: Request, payload: PlaceDetailsRequest) -> DetailsResponse:
    client = GoogleMapsClient()
    try:
        data = await client.place_details(payload.place_id)
        return DetailsResponse(raw=data)
    finally:
        await client.close()

@router.post("/directions", response_model=DirectionsResponse)
@limiter.limit("30/minute")
async def get_directions(request: Request, payload: DirectionsRequest) -> DirectionsResponse:
    client = GoogleMapsClient()
    try:
        data = await client.directions(payload.origin, payload.destination, payload.mode)
        return DirectionsResponse(raw=data)
    finally:
        await client.close()

@router.get("/embed/place/{place_id}", response_model=EmbedPlaceResponse)
async def embed_place(place_id: str) -> EmbedPlaceResponse:
    settings = get_settings()
    url = GoogleMapsClient.embed_place_url(place_id, settings.google_maps_api_key)
    return EmbedPlaceResponse(embed_url=url, external_url=f"https://maps.google.com/?q=place_id:{place_id}")

@router.get("/embed/directions", response_model=EmbedDirectionsResponse)
async def embed_directions(origin: str, destination: str, mode: str | None = None) -> EmbedDirectionsResponse:
    settings = get_settings()
    url = GoogleMapsClient.embed_directions_url(origin, destination, settings.google_maps_api_key, mode)
    ext = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"
    if mode:
        ext += f"&travelmode={mode}"
    return EmbedDirectionsResponse(embed_url=url, external_url=ext)

# Tool-call friendly wrappers (optional): allow Open WebUI to call via name mapping
@router.post("/tool/search_places", response_model=SearchResponse)
async def tool_search_places(request: Request, payload: SearchRequest) -> SearchResponse:
    return await search_places(request, payload)

@router.get("/tool/embed_place/{place_id}", response_model=EmbedPlaceResponse)
async def tool_embed_place(place_id: str) -> EmbedPlaceResponse:
    return await embed_place(place_id)

@router.get("/tool/embed_directions", response_model=EmbedDirectionsResponse)
async def tool_embed_directions(origin: str, destination: str, mode: str | None = None) -> EmbedDirectionsResponse:
    return await embed_directions(origin, destination, mode)

# LLM Chat endpoint
@router.post("/llm/chat", response_model=LLMChatResponse)
async def llm_chat(request: Request, payload: LLMChatRequest) -> LLMChatResponse:
    """
    Chat with LLM that can call Google Maps APIs
    """
    llm_client = OllamaClient()
    maps_client = GoogleMapsClient()
    
    try:
        # Build system prompt
        system_prompt = """You are a helpful Maps Assistant. Be brief and conversational. When users ask about places or directions, acknowledge their request in 1-2 short sentences."""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend([{"role": msg.role, "content": msg.content} for msg in payload.history])
        messages.append({"role": "user", "content": payload.message})
        
        # Call LLM
        llm_response = await llm_client.chat(
            model="phi3:mini",
            messages=messages
        )
        
        if "error" in llm_response:
            # Still try to process the query even if LLM fails
            assistant_message = llm_response.get("message", {}).get("content", "Let me help you with that.")
        else:
            assistant_message = llm_response.get("message", {}).get("content", "")
        
        # Try to detect if we need to call Maps APIs
        user_query_lower = payload.message.lower()
        map_data = None
        
        # Check for direction request
        if any(keyword in user_query_lower for keyword in ["direction", "how to get", "from", "to"]):
            # Try to extract origin and destination
            import re
            # Try multiple patterns
            match = re.search(r'from\s+(.+?)\s+to\s+(.+?)(?:\s+by\s+(\w+))?(?:\?|$)', payload.message, re.IGNORECASE)
            if not match:
                # Try pattern: "direction seoul to busan" or "seoul to busan"
                match = re.search(r'(?:direction|show|get)\s+(?:me\s+)?(?:direction\s+)?(?:from\s+)?([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+by\s+(\w+))?(?:\?|$)', payload.message, re.IGNORECASE)
            if match:
                origin = match.group(1).strip()
                destination = match.group(2).strip()
                mode = match.group(3).lower() if match.group(3) else "driving"
                
                # Get directions embed
                settings = get_settings()
                embed_url = GoogleMapsClient.embed_directions_url(origin, destination, settings.google_maps_api_key, mode)
                external_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"
                if mode:
                    external_url += f"&travelmode={mode}"
                
                map_data = {
                    "type": "directions",
                    "embed_url": embed_url,
                    "external_url": external_url,
                    "origin": origin,
                    "destination": destination,
                    "mode": mode
                }
                
                assistant_message += f"\n\nI've shown the route on the map. You can also open it in Google Maps using the link provided."
        
        # Check for place search
        elif any(keyword in user_query_lower for keyword in ["find", "show", "where", "restaurant", "coffee", "shop", "place"]):
            # Search for places
            search_data = await maps_client.text_search(payload.message, None, 5000)
            results = search_data.get("results", [])
            
            if results:
                top_place = results[0]
                place_id = top_place.get("place_id")
                
                if place_id:
                    settings = get_settings()
                    embed_url = GoogleMapsClient.embed_place_url(place_id, settings.google_maps_api_key)
                    external_url = f"https://maps.google.com/?q=place_id:{place_id}"
                    
                    map_data = {
                        "type": "place",
                        "embed_url": embed_url,
                        "external_url": external_url,
                        "place": {
                            "name": top_place.get("name"),
                            "address": top_place.get("formatted_address"),
                            "rating": top_place.get("rating")
                        }
                    }
                    
                    # Enhance LLM response with place details
                    place_info = f"\n\n**{top_place.get('name')}**\n"
                    if top_place.get('formatted_address'):
                        place_info += f"📍 {top_place.get('formatted_address')}\n"
                    if top_place.get('rating'):
                        place_info += f"⭐ Rating: {top_place.get('rating')}/5\n"
                    
                    assistant_message += place_info + "\nI've shown it on the map. You can also open it in Google Maps using the link provided."
        
        return LLMChatResponse(
            response=assistant_message,
            map_data=map_data
        )
        
    finally:
        await llm_client.close()
        await maps_client.close()

from fastapi import APIRouter, Request
from .schemas import SearchRequest, PlaceDetailsRequest, DirectionsRequest, SearchResponse, DetailsResponse, DirectionsResponse, EmbedPlaceResponse, EmbedDirectionsResponse
from .google_maps import GoogleMapsClient
from .config import get_settings
from .rate_limit import limiter

router = APIRouter()

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

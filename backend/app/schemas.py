from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    location: Optional[str] = Field(default=None, description="lat,lng")
    radius: Optional[int] = Field(default=None, ge=1, le=50000)

class PlaceDetailsRequest(BaseModel):
    place_id: str = Field(min_length=5)

class DirectionsRequest(BaseModel):
    origin: str = Field(min_length=1)
    destination: str = Field(min_length=1)
    mode: Optional[str] = Field(default=None)

class EmbedPlaceResponse(BaseModel):
    embed_url: str
    external_url: str

class EmbedDirectionsResponse(BaseModel):
    embed_url: str
    external_url: str

class SearchResponse(BaseModel):
    raw: Dict[str, Any]

class DetailsResponse(BaseModel):
    raw: Dict[str, Any]

class DirectionsResponse(BaseModel):
    raw: Dict[str, Any]

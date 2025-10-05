from __future__ import annotations
import httpx
from typing import Any, Dict
from .config import get_settings

_GOOGLE_BASE = "https://maps.googleapis.com/maps/api"

class GoogleMapsClient:
    def __init__(self, api_key: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.google_maps_api_key
        self._client = httpx.AsyncClient(base_url=_GOOGLE_BASE, timeout=15)

    async def close(self) -> None:
        await self._client.aclose()

    async def text_search(self, query: str, location: str | None = None, radius: int | None = None) -> Dict[str, Any]:
        params = {"query": query, "key": self.api_key}
        if location:
            params["location"] = location
        if radius:
            params["radius"] = str(radius)
        r = await self._client.get("/place/textsearch/json", params=params)
        r.raise_for_status()
        return r.json()

    async def place_details(self, place_id: str) -> Dict[str, Any]:
        params = {"place_id": place_id, "key": self.api_key}
        r = await self._client.get("/place/details/json", params=params)
        r.raise_for_status()
        return r.json()

    async def directions(self, origin: str, destination: str, mode: str | None = None) -> Dict[str, Any]:
        params = {"origin": origin, "destination": destination, "key": self.api_key}
        if mode:
            params["mode"] = mode
        r = await self._client.get("/directions/json", params=params)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def embed_place_url(place_id: str, api_key: str) -> str:
        return f"https://www.google.com/maps/embed/v1/place?key={api_key}&q=place_id:{place_id}"

    @staticmethod
    def embed_directions_url(origin: str, destination: str, api_key: str, mode: str | None = None) -> str:
        mode_param = f"&mode={mode}" if mode else ""
        return f"https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={origin}&destination={destination}{mode_param}"

## LLM Maps Assistant

FastAPI backend that calls Google Maps (Places, Details, Directions) and returns embeddable map URLs and external links. Minimal static frontend to preview the map.

### Prereqs
- Python 3.10+
- Google Cloud project with: Places API, Directions API, Maps Embed API enabled

### Setup
1. Create `.env` from `.env.example` and set `GOOGLE_MAPS_API_KEY` (server-side, restricted).
2. Create a venv (if missing venv support: `sudo apt install -y python3-venv`):
   - `python3 -m venv .venv && source .venv/bin/activate`
3. Install deps:
   - `pip install -r requirements.txt`
4. Run backend:
   - `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload`
5. Open `frontend/public/index.html` in your browser (it assumes backend on `:8000`).

### API
- POST `/api/search` → body: `{ "query": "sushi near nyc", "location":"40.7,-74.0", "radius": 2000 }`
- POST `/api/place` → body: `{ "place_id": "..." }`
- POST `/api/directions` → body: `{ "origin": "...", "destination": "...", "mode": "driving|walking|..." }`
- GET  `/api/embed/place/{place_id}` → returns `{ embed_url, external_url }`
- GET  `/api/embed/directions?origin=...&destination=...&mode=...` → `{ embed_url, external_url }`

### Security and limits
- Keep the API key server-side only. Restrict it by IPs/referrers and set budgets/quotas.
- Requests are validated via Pydantic. Basic rate limiting is enabled (SlowAPI). Adjust in `backend/app/config.py`.
- CORS is restricted via `allowed_origins` in `backend/app/config.py`.

### Open WebUI
- Create a tool that calls `/api/search` or `/api/directions`, then render the `embed_url` (iframe) or use `external_url` to open Google Maps.

### Local LLM
- You can run Open WebUI and connect it to any local LLM. The LLM can call the backend endpoints and return the embed URL or link as part of its response.

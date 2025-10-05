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
1. Ensure Ollama is running (e.g., `ollama run phi3:mini`) and Open WebUI is up at `http://localhost:3000`.
2. In Open WebUI, import tools/actions from this backend:
   - Tools (OpenAI-style): `http://localhost:8000/openwebui-tools.json`
   - Actions (HTTP requests): `http://localhost:8000/openwebui-actions.json`
3. Or add manually three tools mapped to your API:
   - `POST http://localhost:8000/api/search`
   - `GET  http://localhost:8000/api/embed/place/{place_id}`
   - `GET  http://localhost:8000/api/embed/directions?origin=...&destination=...&mode=...`
4. Suggested system prompt:
   - "You are a Maps assistant. When asked for places or directions, call the provided tools. For places: call search_places with the user query, pick the top result, then call embed_place. For directions: call embed_directions with origin, destination, and optional mode. Always include the iframe `embed_url` and `external_url` in the final answer."
5. If Open WebUI cannot render iframes inside chat, present the `external_url` for the user to open. If you customize UI, render an iframe with the `embed_url`.

### Local LLM
- You can run Open WebUI and connect it to any local LLM. The LLM can call the backend endpoints and return the embed URL or link as part of its response.

# Testing Guide

## Prerequisites
1. Google Cloud account with Maps APIs enabled (Places, Directions, Maps Embed)
2. API key configured in `.env`
3. Python 3.10+ installed
4. (Optional) Ollama and Open WebUI for LLM integration

## Backend Testing

### 1. Start the Backend
```bash
source .venv/bin/activate
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Test Health Endpoint
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"ok"}`

### 3. Test Search Places
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "coffee shops in New York", "radius": 5000}'
```

### 4. Test Embed Place
```bash
# Use a place_id from the search results
curl http://localhost:8000/api/embed/place/ChIJN1t_tDeuEmsRUsoyG83frY4
```

### 5. Test Directions
```bash
curl -X GET "http://localhost:8000/api/embed/directions?origin=Times%20Square,%20New%20York&destination=Central%20Park,%20New%20York&mode=walking"
```

## Frontend Testing

### 1. Open Frontend
Open `frontend/public/index.html` in your browser (ensure backend is running on port 8000)

### 2. Test Search Flow
1. Enter "sushi restaurants in Tokyo" in search query
2. Click "Search Places"
3. Click on any result to view on embedded map
4. Verify map loads and external link works

### 3. Test Directions Flow
1. Switch to "Get Directions" tab
2. Enter origin: "Shibuya Station, Tokyo"
3. Enter destination: "Tokyo Tower"
4. Select mode: "walking"
5. Click "Get Directions"
6. Verify embedded map shows route
7. Click external link to verify it opens in Google Maps

## Open WebUI Integration Testing

### 1. Setup Open WebUI
```bash
# Install and run Open WebUI (if not already installed)
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

### 2. Configure Ollama
```bash
# Pull a local LLM (e.g., phi3:mini)
ollama pull phi3:mini
ollama run phi3:mini
```

### 3. Import Tools in Open WebUI
1. Navigate to http://localhost:3000
2. Go to Settings → Tools/Functions
3. Import from URL: `http://host.docker.internal:8000/openwebui-tools.json`
4. Or manually add tools pointing to your backend endpoints

### 4. Test LLM Integration
**System Prompt:**
```
You are a Maps assistant. When asked for places or directions, call the provided tools. 
For places: call search_places with the user query, pick the top result, then call embed_place. 
For directions: call embed_directions with origin, destination, and optional mode. 
Always include the iframe embed_url and external_url in the final answer.
```

**Test Prompts:**
1. "Find me sushi restaurants near Times Square"
2. "Show me directions from Central Park to Empire State Building"
3. "Where can I find coffee shops in Brooklyn?"

### 5. Verify LLM Response
The LLM should:
- Call the appropriate backend API
- Return both `embed_url` (for iframe) and `external_url` (for opening in Google Maps)
- Present the map link to the user

## Security Verification

### 1. API Key Protection
- Verify `.env` file contains API key
- Verify API key is NOT exposed in frontend code
- Check that API key is only used server-side

### 2. CORS Testing
```bash
# Should succeed (from allowed origin)
curl -X POST http://localhost:8000/api/search \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Should fail (from disallowed origin)
curl -X POST http://localhost:8000/api/search \
  -H "Origin: http://malicious-site.com" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### 3. Rate Limiting
```bash
# Run this script to test rate limiting
for i in {1..15}; do
  curl -X POST http://localhost:8000/api/search \
    -H "Content-Type: application/json" \
    -d '{"query": "test"}' &
done
```
Expected: Some requests should return 429 (Too Many Requests)

### 4. Input Validation
```bash
# Should fail - empty query
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": ""}'

# Should fail - invalid radius
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "radius": 100000}'
```

## Google Cloud Configuration

### Required APIs
1. Places API (New)
2. Directions API
3. Maps Embed API
4. Maps JavaScript API (optional, for advanced features)

### API Key Restrictions (Recommended)
1. **Application restrictions:**
   - HTTP referrers: `http://localhost:*`, `http://127.0.0.1:*`
   - IP addresses: Your server IP

2. **API restrictions:**
   - Restrict to: Places API, Directions API, Maps Embed API

3. **Quotas:**
   - Set daily quota limits to prevent unexpected charges
   - Monitor usage in Google Cloud Console

## Troubleshooting

### Backend won't start
- Check `.env` file exists and contains valid API key
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

### Maps not loading in frontend
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify API key has Maps Embed API enabled

### Open WebUI can't call tools
- Ensure backend is accessible from Open WebUI container
- Use `host.docker.internal` instead of `localhost` in Docker
- Check tool definitions are correctly imported

### Rate limiting too aggressive
- Adjust limits in `backend/app/config.py`
- Modify `ratelimit_requests` and `ratelimit_window_seconds` in `.env`

# LLM Maps Assistant

Chat-based interface for finding places and getting directions using Google Maps. Ask natural language questions like "Find sushi restaurants in Tokyo" or "How do I get from Times Square to Central Park?" and see results on an embedded map.

<img width="1356" height="954" alt="Screenshot from 2025-10-06 07-50-35" src="https://github.com/user-attachments/assets/7f37177d-67d4-41d3-a590-1fd601f106c0" />

---

## 🚀 Quick Start

### 1. Start Ollama (LLM Server)
```bash
# Terminal 1: Start Ollama server
ollama serve

# Terminal 2: Pull and verify model
ollama pull phi3:mini
```

### 2. Setup Backend
```bash
# Navigate to project directory
cd llm-maps-assistant

# Activate virtual environment
source .venv/bin/activate

# Start backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Open Chat Interface
```bash
# Open in browser
xdg-open frontend/public/chat.html

# Or manually open: frontend/public/chat.html
```

### 4. Start Chatting!
Try these prompts:
- "Find sushi restaurants in Tokyo"
- "Show me coffee shops near Central Park"
- "How do I get from Times Square to Empire State Building?"
- "Directions from Brooklyn Bridge to Statue of Liberty by walking"

---

## 📋 Prerequisites

- **Python 3.10+**
- **Ollama** - For running local LLM (phi3:mini)
- **Google Cloud project** with: Places API, Directions API, Maps Embed API enabled
- **Modern web browser** (Chrome, Firefox, Safari)

---

## ⚙️ Setup

1. **Create `.env` file** from `.env.example` and set `GOOGLE_MAPS_API_KEY`:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Maps API key
   ```

2. **Create virtual environment** (if missing venv support: `sudo apt install -y python3-venv`):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run backend**:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Open chat interface**:
   - Open `frontend/public/chat.html` in your browser
   - Or run: `xdg-open frontend/public/chat.html`

---

## 💬 How to Use

### Search for Places
Just type what you're looking for:
- "Find pizza places in Manhattan"
- "Show me museums in Paris"
- "Coffee shops near Brooklyn Bridge"

### Get Directions
Use natural language:
- "How do I get from A to B?"
- "Directions from Times Square to Central Park"
- "Show me the way from Brooklyn to Manhattan by walking"

**Travel modes:** walking, driving, bicycling, transit

### View Results
- **Chat (left):** See place details, ratings, addresses
- **Map (right):** Interactive embedded Google Maps
- **Open in Google Maps:** Click link to open in full Google Maps app

---

## ✨ Features

### Chat Interface with Real LLM
The `chat.html` interface now uses **Ollama (phi3:mini)** for intelligent conversations:
- ✅ **Real LLM responses** - Powered by phi3:mini local model
- ✅ **Natural language understanding** - True conversational AI
- ✅ **Context awareness** - Remembers conversation history
- ✅ **Automatic Maps integration** - LLM calls Google Maps APIs
- ✅ **Split-screen view** - Chat on the left, embedded Google Maps on the right
- ✅ **Quick prompts** - Pre-built examples to get started
- ✅ **Typing indicator** - Shows when LLM is thinking
- ✅ **Responsive design** - Works on desktop and mobile

### How It Works
1. **You type** your question in natural language
2. **Frontend** sends message to backend `/api/llm/chat` endpoint
3. **Backend** forwards to Ollama (phi3:mini) with system prompt
4. **LLM** generates intelligent response
5. **Backend** detects if Maps API call is needed (places/directions)
6. **Backend** calls Google Maps APIs and enriches LLM response
7. **Frontend** displays LLM response in chat + embedded map on right
8. **You can** click "Open in Google Maps" for full navigation

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| **POST** | **`/api/llm/chat`** | **Chat with LLM (main endpoint)** |
| POST | `/api/search` | Search for places |
| POST | `/api/place` | Get place details |
| POST | `/api/directions` | Get directions |
| GET | `/api/embed/place/{place_id}` | Get embed URLs for place |
| GET | `/api/embed/directions` | Get embed URLs for directions |
| GET | `/docs` | Interactive API documentation (Swagger UI) |

### Example API Calls

**Chat with LLM (Main Endpoint):**
```bash
curl -X POST http://localhost:8000/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Find sushi restaurants in Tokyo", "history": []}'
```

**Search Places (Direct):**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "sushi near nyc", "location":"40.7,-74.0", "radius": 2000}'
```

**Get Place Embed:**
```bash
curl http://localhost:8000/api/embed/place/ChIJN1t_tDeuEmsRUsoyG83frY4
```

**Get Directions:**
```bash
curl "http://localhost:8000/api/embed/directions?origin=Times%20Square&destination=Central%20Park&mode=walking"
```

---

## 🔒 Security and Best Practices

### API Key Protection
- ✅ API key stored in `.env` file (server-side only)
- ✅ Never exposed to client/frontend
- ✅ `.env` in `.gitignore`
- ✅ `.env.example` provided as template

### Security Features
- ✅ **CORS protection** with configurable allowed origins
- ✅ **Rate limiting** enabled (60 requests/minute default)
- ✅ **Input validation** via Pydantic schemas
- ✅ **Server-side API calls** only

### Google Cloud Configuration

**Required APIs:**
1. Places API (New)
2. Directions API
3. Maps Embed API

**Recommended API Key Restrictions:**
```
Application Restrictions:
- IP addresses: Your server IP
- HTTP referrers: http://localhost:*

API Restrictions:
- Restrict to: Places API, Directions API, Maps Embed API

Quotas:
- Set daily quota limits to prevent unexpected charges
- Monitor usage in Google Cloud Console
```

---

## 🧪 Testing

### Backend Testing

**1. Health Check:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

**2. Search Places:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "coffee shops in New York", "radius": 5000}'
```

**3. Test Embed URLs:**
```bash
curl http://localhost:8000/api/embed/place/PLACE_ID_HERE
```

### Chat Interface Testing

**1. Open Chat Interface:**
```bash
xdg-open frontend/public/chat.html
```

**2. Test Place Search:**
- Type: "Find sushi restaurants in Tokyo"
- Verify: Results appear with map on right side

**3. Test Directions:**
- Type: "How do I get from Times Square to Central Park by walking?"
- Verify: Route appears on map with travel mode

**4. Test Quick Prompts:**
- Click any quick prompt button
- Verify it auto-fills and sends the query

### Automated Verification
```bash
python3 verify_setup.py
```

---

## 🔧 Troubleshooting

### "Failed to fetch" error
- Make sure backend is running on port 8000
- Check: `curl http://localhost:8000/health`
- Should return: `{"status":"ok"}`

### Map not loading
- Verify Google Maps API key is set in `.env`
- Check that Maps Embed API is enabled in Google Cloud Console
- Look for errors in browser console (F12)
- Verify "null" origin is in `allowed_origins` (for file:// protocol)

### Backend won't start
- Activate virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Check `.env` file exists with valid API key
- Check Python version: `python --version` (should be 3.10+)

### Chat not responding
- Check browser console for JavaScript errors
- Verify backend API is accessible
- Test API directly with curl commands

### Rate limiting too aggressive
- Adjust limits in `backend/app/config.py`
- Modify `ratelimit_requests` and `ratelimit_window_seconds`

---

## 🏗️ Architecture

### Project Structure
```
llm-maps-assistant/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI app, CORS, middleware
│       ├── routes.py            # API endpoints
│       ├── google_maps.py       # Google Maps client
│       ├── config.py            # Settings, environment vars
│       ├── schemas.py           # Pydantic models
│       └── rate_limit.py        # Rate limiting config
│
├── frontend/
│   └── public/
│       └── chat.html            # Chat interface (MAIN UI)
│
├── .env                         # API key (gitignored)
├── .env.example                 # Template for API key
├── requirements.txt             # Python dependencies
├── verify_setup.py              # Setup verification script
└── README.md                    # This file
```

### Technology Stack

**Backend:**
- Python 3.12
- FastAPI - Web framework
- Uvicorn - ASGI server
- httpx - Async HTTP client
- Pydantic - Data validation
- SlowAPI - Rate limiting

**Frontend:**
- HTML5 - Structure
- CSS3 - Styling with gradients and animations
- JavaScript (ES6+) - Logic and API calls
- No frameworks - Vanilla JS for simplicity

**APIs:**
- Google Places API (New) - Place search
- Google Directions API - Route calculation
- Google Maps Embed API - Map display

---

## 💡 Design Decisions

### Chat Interface Implementation
- **ChatGPT-like interface** for natural language interaction
- **No actual LLM required** - Simple intent detection
- **Client-side JavaScript** parses queries
- **Can be opened directly** in browser with `file://` protocol
- **Split-screen view** with embedded maps

### Intent Detection Logic
- **Direction keywords:** "direction", "how to get", "from...to"
- **Travel mode keywords:** "walk", "drive", "bike", "transit", "bus", "train"
- **Default behavior:** If no direction keywords, treat as place search
- **Parsing:** Uses regex to extract origin/destination from natural language

### User Journey: Search Places
1. User types: "Find sushi restaurants in Tokyo"
2. Interface detects search intent (no direction keywords)
3. Calls backend `/api/search` with query
4. Backend calls Google Places API
5. Interface receives results, displays top result
6. Calls `/api/embed/place` with place_id
7. Displays embedded map on right side
8. Shows place details in chat with "Open in Google Maps" link

### User Journey: Get Directions
1. User types: "How do I get from Times Square to Central Park?"
2. Interface detects direction intent ("from...to" pattern)
3. Parses origin and destination
4. Detects travel mode from keywords (walking/driving/etc.)
5. Calls `/api/embed/directions` with parameters
6. Displays route on embedded map
7. Shows directions info in chat with external link

---

## 🌟 Example Conversations

### Example 1: Finding Food
**You:** I'm hungry, find me a good burger place in NYC

**Assistant:** I found several great burger places! Here's the top result:

**Shake Shack**  
📍 Madison Square Park, New York, NY  
⭐ Rating: 4.3/5

You can view it on the map here: [Open in Google Maps]

### Example 2: Getting Directions
**You:** How do I get from Central Park to Times Square by walking?

**Assistant:** 🚶 Here are directions from Central Park to Times Square by walking!

I've shown the route on the map. You can also [open it in Google Maps] for turn-by-turn navigation.

---

## 🎓 Tips

1. **Be specific:** "Coffee shops in Brooklyn" works better than just "coffee"
2. **Use landmarks:** "Near Times Square" or "Near Central Park"
3. **Specify travel mode:** Add "by walking" or "by driving" for directions
4. **Try quick prompts:** Click the suggestion buttons to see examples

---

## ⚡ Advanced

### Configuration

Edit `backend/app/config.py` to adjust:
```python
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "null",  # For file:// protocol
]

ratelimit_requests = 60
ratelimit_window_seconds = 60
```

### Environment Variables (.env)
```bash
GOOGLE_MAPS_API_KEY=your_api_key_here
ENVIRONMENT=development
```

---

## 📈 Future Enhancements

### Optional Improvements
1. **Caching** - Redis for API response caching
2. **Authentication** - User accounts and API keys
3. **Database** - Store search history and favorites
4. **Real LLM** - Integrate with Ollama/Open WebUI for smarter conversations
5. **Multi-language** - Support for multiple languages
6. **Voice input** - Speech-to-text for queries
7. **Favorites** - Save favorite places
8. **Sharing** - Share maps with others

### Production Deployment
1. **Docker** - Containerize backend and frontend
2. **CI/CD** - GitHub Actions for automated testing
3. **Monitoring** - Prometheus + Grafana
4. **Logging** - Structured logging with ELK stack
5. **CDN** - CloudFlare for frontend assets
6. **Load balancing** - Nginx for multiple backend instances

---

## ✅ Requirements Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Local LLM interface | ✅ | Chat interface with intent detection |
| Find places | ✅ | Google Places API integration |
| Get directions | ✅ | Google Directions API integration |
| Embedded maps | ✅ | Google Maps Embed API |
| External links | ✅ | "Open in Google Maps" buttons |
| Python backend | ✅ | FastAPI with async/await |
| Security best practices | ✅ | Server-side API key, CORS, rate limiting |
| Usage limits | ✅ | Rate limiting, configurable quotas |

**Status: ✅ ALL REQUIREMENTS MET**

---

## 📞 Support

### API Documentation
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

### Verification
Run `python3 verify_setup.py` to check your setup

---

**Built with ❤️ in Indonesia**

*Last Updated: 2025-10-06*

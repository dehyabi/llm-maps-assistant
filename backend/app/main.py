from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from .config import get_settings
from .rate_limit import limiter
from .routes import router
from fastapi.responses import JSONResponse
from fastapi import Request

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(router, prefix="/api")

# Serve Open WebUI tool definitions (OpenAI-style function/tool schema)
@app.get("/openwebui-tools.json")
async def openwebui_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_places",
                "description": "Search for places using a free-text query and optional location/radius",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "location": {"type": "string", "description": "lat,lng (optional)"},
                        "radius": {"type": "integer", "minimum": 1, "maximum": 50000}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "embed_place",
                "description": "Get embeddable map URL and external link for a place",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "place_id": {"type": "string"}
                    },
                    "required": ["place_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "embed_directions",
                "description": "Get embeddable directions map URL and external link",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string"},
                        "destination": {"type": "string"},
                        "mode": {"type": "string", "enum": ["driving", "walking", "bicycling", "transit"]}
                    },
                    "required": ["origin", "destination"]
                }
            }
        }
    ]
    return JSONResponse(content={"tools": tools})

# Open WebUI Actions (HTTP) export with absolute URLs derived from request
@app.get("/openwebui-actions.json")
async def openwebui_actions(request: Request):
    base = str(request.base_url).rstrip("/")
    actions = [
        {
            "name": "search_places",
            "type": "request",
            "config": {
                "method": "POST",
                "url": f"{base}/api/search",
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "query": "{{query}}",
                    "location": "{{location}}",
                    "radius": "{{radius}}"
                }
            }
        },
        {
            "name": "embed_place",
            "type": "request",
            "config": {
                "method": "GET",
                "url": f"{base}/api/embed/place/{{place_id}}"
            }
        },
        {
            "name": "embed_directions",
            "type": "request",
            "config": {
                "method": "GET",
                "url": f"{base}/api/embed/directions?origin={{origin}}&destination={{destination}}&mode={{mode}}"
            }
        }
    ]
    return JSONResponse(content={"actions": actions})

# Assumptions and Design Decisions

## Technology Choices

### Backend: Python with FastAPI
**Rationale:**
- FastAPI provides automatic API documentation (OpenAPI/Swagger)
- Built-in request validation with Pydantic
- Async support for efficient Google Maps API calls
- Easy integration with Open WebUI tools
- Type hints improve code quality and IDE support

**Alternative considered:** Node.js/Express
- Would work equally well but Python has better ML/LLM ecosystem integration

### LLM: Open WebUI + Ollama
**Rationale:**
- Open WebUI is the suggested platform in requirements
- Supports local LLMs (privacy, no API costs)
- Built-in tool/function calling support
- Easy to set up and use
- Works with multiple LLM backends (Ollama, OpenAI, etc.)

**LLM Model Choice:** Phi-3-mini (default recommendation)
- Small, fast, runs on consumer hardware
- Good function calling capabilities
- Free and open source
- Alternatives: llama3, mistral, gemma

### Frontend: Vanilla HTML/CSS/JavaScript
**Rationale:**
- No build process required
- Simple to understand and modify
- Minimal dependencies
- Can be opened directly in browser
- Sufficient for demonstration purposes

**Alternative considered:** React/Vue
- Would be better for production but adds complexity
- Not necessary for this demo/test project

## Google Maps API Usage

### APIs Enabled
1. **Places API (New):** For text search and place details
2. **Directions API:** For route calculation
3. **Maps Embed API:** For displaying embedded maps

### API Key Security
**Assumptions:**
- API key is server-side only (never exposed to client)
- User will configure API restrictions in Google Cloud Console
- CORS is configured to limit frontend access
- Rate limiting prevents abuse

**Best Practices Implemented:**
- Environment variable storage (`.env`)
- Server-side API calls only
- Input validation to prevent malicious queries
- Rate limiting per IP address

### Usage Limits
**Assumptions:**
- User has Google Cloud free tier ($200 credit for new accounts)
- Moderate usage (< 1000 requests/day)
- User will set up billing alerts and quotas

**Recommendations:**
- Set daily quota limits in Google Cloud Console
- Monitor usage regularly
- Implement caching for repeated queries (future enhancement)

## Architecture Decisions

### Separation of Concerns
- **Backend:** All Google Maps API calls, business logic, security
- **Frontend:** Presentation only, no API keys
- **LLM:** Orchestration via tool calling

### Stateless Design
- No database required
- All data comes from Google Maps API
- Session-less (can add authentication later if needed)

### Error Handling
- Graceful degradation
- User-friendly error messages
- Proper HTTP status codes
- Logging for debugging (can be enhanced)

## Open WebUI Integration

### Tool Definition Format
**Assumption:** Open WebUI supports OpenAI-style function calling
- Exported at `/openwebui-tools.json`
- Also provided HTTP actions at `/openwebui-actions.json`
- Both formats supported for flexibility

### LLM Capabilities
**Assumptions:**
- LLM can parse function schemas
- LLM can make HTTP requests via tools
- LLM can format responses with URLs
- User will configure appropriate system prompt

### Iframe Rendering
**Assumption:** Open WebUI may not render iframes in chat
- Provided both `embed_url` (for iframe) and `external_url` (for opening in browser)
- User can customize Open WebUI to render iframes if desired
- External link always works as fallback

## Workflow Assumptions

### User Journey: Search Places
1. User asks LLM: "Find sushi restaurants in Tokyo"
2. LLM calls `search_places` tool with query
3. Backend calls Google Places API
4. LLM receives results, picks top result
5. LLM calls `embed_place` with place_id
6. Backend returns embed_url and external_url
7. LLM presents both to user

### User Journey: Get Directions
1. User asks LLM: "How do I get from A to B?"
2. LLM calls `embed_directions` with origin, destination, mode
3. Backend returns embed_url and external_url
4. LLM presents both to user

### Direct API Usage (without LLM)
- Frontend can call backend directly
- Useful for testing and debugging
- Demonstrates API functionality independently

## Security Assumptions

### Threat Model
**Protected against:**
- API key exposure
- CORS attacks from unauthorized domains
- Rate limiting abuse
- Invalid input injection

**Not protected against (future enhancements):**
- Authentication/authorization (no user system)
- DDoS attacks (basic rate limiting only)
- Advanced persistent threats

### Trust Boundaries
- Backend is trusted
- Frontend is untrusted (client-side)
- LLM is semi-trusted (can make valid API calls)
- Google Maps API is trusted

## Scalability Assumptions

### Expected Load
- Single user or small team
- Development/demo environment
- < 100 requests/hour
- No persistent storage needed

### Future Enhancements (if scaling needed)
- Add Redis for caching
- Implement database for user preferences
- Add authentication (OAuth, JWT)
- Deploy to cloud (AWS, GCP, Azure)
- Add monitoring (Prometheus, Grafana)
- Implement CDN for frontend

## Development Environment

### Assumptions
- Linux/macOS development environment
- Python 3.10+ available
- Internet connection for Google Maps API
- Port 8000 available for backend
- Modern web browser (Chrome, Firefox, Safari)

### Optional Components
- Docker (for Open WebUI)
- Ollama (for local LLM)
- Git (for version control)

## Testing Assumptions

### Manual Testing
- Developer will manually test via frontend
- Developer will test Open WebUI integration
- Developer will verify API key restrictions

### Automated Testing
- Not implemented (out of scope for this demo)
- Could add: pytest, integration tests, E2E tests

## Limitations and Known Issues

### Current Limitations
1. No caching (every request hits Google Maps API)
2. No user authentication
3. No persistent storage
4. Basic error handling
5. No logging/monitoring
6. No automated tests

### Known Issues
1. Open WebUI iframe rendering depends on configuration
2. CORS must be configured for production domains
3. Rate limiting is per-IP (can be bypassed with proxies)

### Future Improvements
1. Add caching layer (Redis)
2. Implement user accounts
3. Add favorites/history
4. Better error messages
5. Comprehensive logging
6. Automated tests
7. Docker deployment
8. CI/CD pipeline

## Compliance and Legal

### Assumptions
- User has accepted Google Maps Platform Terms of Service
- User will display required Google attribution
- User will not violate Google's usage policies
- This is for development/demo purposes only

### Production Considerations
- Review Google Maps Platform pricing
- Implement proper attribution
- Add privacy policy
- Comply with data protection regulations (GDPR, etc.)
- Add terms of service

## Documentation

### Provided Documentation
- README.md: Setup and usage
- TESTING.md: Testing procedures
- ASSUMPTIONS.md: This file
- Code comments: Inline documentation

### API Documentation
- Automatic via FastAPI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

"""
LLM client for Ollama integration
"""
import httpx
from typing import Dict, Any, List
import json


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def chat(self, model: str, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send chat request to Ollama with optional tool calling
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        if tools:
            payload["tools"] = tools
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {
                "error": "timeout",
                "message": {
                    "role": "assistant",
                    "content": "The LLM is taking too long to respond. This is normal for the first request as the model loads into memory."
                }
            }
        except httpx.ConnectError:
            return {
                "error": "connection",
                "message": {
                    "role": "assistant",
                    "content": "Cannot connect to Ollama. Please make sure it's running: ollama serve"
                }
            }
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "message": {
                    "role": "assistant",
                    "content": f"LLM error: {str(e)}"
                }
            }
    
    async def generate(self, model: str, prompt: str) -> Dict[str, Any]:
        """
        Simple text generation without chat history
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "response": "Sorry, I couldn't connect to the LLM. Please make sure Ollama is running."
            }

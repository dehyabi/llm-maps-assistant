from slowapi import Limiter
from slowapi.util import get_remote_address
from .config import get_settings

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.ratelimit_requests}/{settings.ratelimit_window_seconds} seconds"])

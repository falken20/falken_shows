from fastapi import APIRouter

from app.api.v1.endpoints import artists, auth, concerts, health, venues

# All v1 endpoints are registered here and mounted under /api/v1 in main.py.
api_router = APIRouter()

api_router.include_router(health.router, tags=["system"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(concerts.router, prefix="/concerts", tags=["concerts"])
api_router.include_router(artists.router, prefix="/artists", tags=["artists"])
api_router.include_router(venues.router, prefix="/venues", tags=["venues"])

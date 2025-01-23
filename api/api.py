from fastapi import APIRouter
from api.endpoints import players

api_router = APIRouter()

api_router.include_router(players.router, prefix="/players", tags=["Players"])
from fastapi import APIRouter
from api.endpoints import players,teams,games

api_router = APIRouter()

api_router.include_router(players.router, prefix="/players", tags=["Players"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
api_router.include_router(games.router, prefix="/games", tags=["Games"])
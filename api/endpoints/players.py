from fastapi import APIRouter, HTTPException, Query
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from nba_api.live.nba.endpoints import scoreboard

from utils.functions import *

router = APIRouter()

# Rota para buscar informações do jogador
@router.get("/player")
async def get_player_bio(name: str = Query(..., description="Nome completo do jogador")):
    player_list = players.get_players()
    player = next((p for p in player_list if remove_accents(p['full_name'].lower()) == remove_accents(name.lower())), None)

    if not player:
        raise HTTPException(status_code=404, detail=f"Jogador '{name}' não encontrado.")

    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id'])
    bio_data = player_info.get_data_frames()[0]
    bio_json = bio_data.to_dict(orient='records')[0]
    bio_json["PLAYER_IMG"] = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player['id']}.png"

    return {
        "bio": bio_json
    }

@router.get("/player-stats")
async def get_player_stats(name: str = Query(..., description="Nome completo do jogador")):
    player_list = players.get_players()
    player = next((p for p in player_list if remove_accents(p['full_name'].lower()) == remove_accents(name.lower())), None)

    if not player:
        raise HTTPException(status_code=404, detail=f"Jogador '{name}' não encontrado.")

    career_stats = playercareerstats.PlayerCareerStats(player_id=player['id'])
    stats_df = career_stats.get_data_frames()[0]
    stats_json = stats_df.to_dict(orient='records')

    return {
        "stats": stats_json
    }

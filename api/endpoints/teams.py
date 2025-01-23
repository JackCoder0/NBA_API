from fastapi import APIRouter, HTTPException, Query
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams

from utils.functions import *

router = APIRouter()

# Buscar time por nome completo ou abreviação
@router.get("/team")
async def get_team_info(name: str = Query(..., description="Nome completo ou abreviação do time")):
    # Busca o jogador pelo nome
    team_list = teams.get_teams()
    
    team = next(
        (t for t in team_list if 
         remove_accents(t['full_name'].lower()) == remove_accents(name.lower()) or 
         t['abbreviation'].lower() == name.lower()), 
        None
    )
    
    team["TEAM_IMG"] = f"https://cdn.nba.com/logos/nba/{team['id']}/global/L/logo.svg"
    
    if not team:
        raise HTTPException(status_code=404, detail=f"Time '{name}' não encontrado.")

    return {"team": team}

# Buscar time por ID
@router.get("/team/{team_id}")
async def get_team_by_id(team_id: int):
    team = teams.find_team_name_by_id(team_id)

    team["TEAM_IMG"] = f"https://cdn.nba.com/logos/nba/{team['id']}/global/L/logo.svg"
    
    if not team:
        raise HTTPException(status_code=404, detail=f"Time com ID '{team_id}' não encontrado.")

    return {"team": team}

# Buscar times por cidade
@router.get("/teams/city")
async def get_teams_by_city(city: str = Query(..., description="Cidade do time")):
    city = remove_accents(city.lower())
    teams_by_city = teams.find_teams_by_city(city)

    teams_by_city["TEAM_IMG"] = f"https://cdn.nba.com/logos/nba/{teams_by_city['id']}/global/L/logo.svg"
    
    if not teams_by_city:
        raise HTTPException(status_code=404, detail=f"Não foram encontrados times na cidade '{city}'.")

    return {"teams": teams_by_city}
  
# Endpoint para buscar o roster de um time
@router.get("/team/{team_id}/roster")
async def get_team_roster(team_id: int):
    team = teams.find_team_name_by_id(team_id)
    team["TEAM_IMG"] = f"https://cdn.nba.com/logos/nba/{team['id']}/global/L/logo.svg"
    
    if not team:
        raise HTTPException(status_code=404, detail=f"Time com ID '{team_id}' não encontrado.")
    
    try:
        roster = commonteamroster.CommonTeamRoster(team_id=team_id)
        roster_data = roster.get_data_frames()[0]
        coach_data = roster.get_data_frames()[1]
        
        roster_json = roster_data.to_dict(orient="records")
        for player in roster_json:
           player["PLAYER_IMG"] = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player['PLAYER_ID']}.png"
        
        coach_json = coach_data.to_dict(orient="records")
        for coach in coach_json:
           coach["COACH_IMG"] = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{coach['COACH_ID']}.png"
           
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar o roster do time: {str(e)}")

    return {
        "team": team,
        "roster": roster_json,
        "coaches": coach_json
    }
    
# Endpoint para buscar o roster do time pela abreviação
@router.get("/team/{abbreviation}/roster")
async def get_team_roster_by_abbreviation(abbreviation: str):
    # Busca o time pela abreviação
    team = teams.find_team_by_abbreviation(abbreviation.upper())
    if not team:
        raise HTTPException(status_code=404, detail=f"Time com abreviação '{abbreviation}' não encontrado.")
    
    try:
        # Busca o roster do time
        roster = commonteamroster.CommonTeamRoster(team_id=team['id'])
        roster_data = roster.get_data_frames()[0]  # Informações do elenco
        coach_data = roster.get_data_frames()[1]  # Informações dos técnicos
        roster_json = roster_data.to_dict(orient="records")
        coach_json = coach_data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar o roster do time: {str(e)}")

    return {
        "team": team,
        "roster": roster_json,
        "coaches": coach_json
    }
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from nba_api.live.nba.endpoints import scoreboard
import unicodedata

# Criação do app FastAPI
app = FastAPI()

# Configuração do CORS (permite acesso do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode restringir às origens específicas (URLs) do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Rota para buscar informações do jogador
@app.get("/player")
async def get_player_stats(name: str = Query(..., description="Nome completo do jogador")):
    # Busca o jogador pelo nome
    player_list = players.get_players()
    player = next((p for p in player_list if remove_accents(p['full_name'].lower()) == remove_accents(name.lower())), None)

    if not player:
        raise HTTPException(status_code=404, detail=f"Jogador '{name}' não encontrado.")

    # Obtém informações biográficas completas do jogador
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id'])
    bio_data = player_info.get_data_frames()[0]
    bio_json = bio_data.to_dict(orient='records')[0]
    bio_json["PLAYER_IMG"] = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player['id']}.png"

    # Obtém estatísticas de carreira do jogador
    career_stats = playercareerstats.PlayerCareerStats(player_id=player['id'])
    stats_df = career_stats.get_data_frames()[0]
    stats_json = stats_df.to_dict(orient='records')

    return {
        "bio": bio_json,
        "stats": stats_json
    }

# Rota para buscar os jogos do dia
@app.get("/games")
async def get_games():
    try:
        # Obtém os jogos do dia
        games = scoreboard.ScoreBoard()

        # Converte para dicionário
        games_dict = games.get_dict()

        return {"games": games_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os jogos: {str(e)}")

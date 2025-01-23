from fastapi import APIRouter, HTTPException, Query
from nba_api.live.nba.endpoints import scoreboard
from datetime import date

from utils.functions import *

router = APIRouter()

# Rota para buscar os jogos do dia
@router.get("/games")
async def get_games():
    try:
        # Obtém os jogos do dia
        games = scoreboard.ScoreBoard()

        # Converte para dicionário
        games_dict = games.get_dict()

        return {"games": games_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os jogos: {str(e)}")
      
# # Rota para buscar os jogos com parâmetros de offset
# @router.get("/games")
# async def get_games(day_offset: int = Query(0, description="Offset de dias para buscar jogos: 0 = hoje, -1 = ontem, 1 = próximos jogos")):
#     """
#     Retorna os jogos de acordo com o offset de dias.
#     :param day_offset: valor que representa o deslocamento de dias:
#                        0 - Hoje
#                        -1 - Jogos do dia anterior
#                        1 - Jogos futuros
#     """
#     try:
#         # Obtém os jogos com o deslocamento de dias
#         games = scoreboard.ScoreBoard(day_offset=day_offset)
        
#         # Converte os jogos para dicionário
#         games_dict = games.get_dict()
        
#         # Se desejar, você pode filtrar apenas os jogos ao vivo:
#         if day_offset == 0:  # Somente se for para buscar jogos de hoje
#             live_games = [game for game in games_dict['games'] if game['status'] == 'Live']
#             return {"games": live_games}
        
#         return {"games": games_dict}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro ao buscar os jogos: {str(e)}")
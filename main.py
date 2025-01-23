from fastapi import FastAPI
from api.api import api_router

app = FastAPI(
  title="NBA API",
  description="API para consultas dos dados do NBA",
  version="1.0.0",
)

app.include_router(api_router)
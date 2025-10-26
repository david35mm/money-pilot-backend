from api import config
from api.routers import perfiles
from api.routers import usuarios
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MoneyPilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=config.settings.ALLOWED_ORIGINS,
    allow_origins=["*"],  # Reemplazar con dominio del frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(perfiles.router)


@app.get("/", tags=["Root"])
def read_root():
  return {"message": "MoneyPilot API is running."}

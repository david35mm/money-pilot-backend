from api import config
from api.routers import auth
from api.routers import catalogos
from api.routers import financial_health
from api.routers import perfiles
from api.routers import usuarios
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="MoneyPilot API",
    description="API para la gestión financiera personal de MoneyPilot.",
    version="0.1.0",
    openapi_tags=[
        {
            "name":
                "auth",
            "description":
                "Operaciones de autenticación: login, registro, verificación."
        },
        {
            "name": "usuarios",
            "description": "Operaciones CRUD básicas de usuarios."
        },
        {
            "name": "perfiles",
            "description": "Operaciones CRUD del perfil detallado del usuario."
        },
        {
            "name":
                "financial_health",
            "description":
                "Endpoints para cálculo y obtención del Financial Health Score."
        },
        {
            "name":
                "catalogos",
            "description":
                "Endpoints para obtener listas de valores (categorías, fuentes, países)."
        },
    ])

# Configurar CORS (ajusta según sea necesario para producción)
app.add_middleware(
    CORSMiddleware,

    # Debe estar definida en config.py
    allow_origins=config.settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Puedes añadir expose_headers si envías headers personalizados
)

# Incluir los routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(usuarios.router, prefix="/api/v1", tags=["usuarios"])
app.include_router(perfiles.router, prefix="/api/v1", tags=["perfiles"])
app.include_router(financial_health.router,
                   prefix="/api/v1",
                   tags=["financial_health"])
app.include_router(catalogos.router, prefix="/api/v1", tags=["catalogos"])


# Ruta raíz simple
@app.get("/")
def read_root():
  return {"message": "Bienvenido a la API de MoneyPilot"}

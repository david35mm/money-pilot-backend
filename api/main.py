# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import config
from api.routers import alertas
from api.routers import auth
from api.routers import categorias
from api.routers import perfiles
from api.routers import presupuestos
from api.routers import transacciones
from api.routers import usuarios

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
            "name": "categorias",
            "description": "Operaciones CRUD de categorías de gastos/ingresos."
        },
        {
            "name": "transacciones",
            "description": "Operaciones CRUD de transacciones."
        },
        {
            "name": "presupuestos",
            "description": "Operaciones CRUD de presupuestos."
        },
        {
            "name": "alertas",
            "description": "Operaciones CRUD de alertas de presupuestos."
        },
    ])

# Configurar CORS (ajusta según sea necesario para producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,  # Debe estar definida en config.py
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Puedes añadir expose_headers si envías headers personalizados
)

# Incluir los routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(usuarios.router, prefix="/api/v1", tags=["usuarios"])
app.include_router(perfiles.router, prefix="/api/v1", tags=["perfiles"])
app.include_router(categorias.router, prefix="/api/v1", tags=["categorias"])
app.include_router(transacciones.router,
                   prefix="/api/v1",
                   tags=["transacciones"])
app.include_router(presupuestos.router, prefix="/api/v1", tags=["presupuestos"])
app.include_router(alertas.router, prefix="/api/v1", tags=["alertas"])


# Ruta raíz simple
@app.get("/")
def read_root():
  return {"message": "Bienvenido a la API de MoneyPilot"}

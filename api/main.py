from api import config
from api.routers import auth
from api.routers import categorias
from api.routers import eventos_financieros
from api.routers import financial_health
from api.routers import perfiles
from api.routers import usuarios
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI(title="MoneyPilot API", version="1.0.0")


class ForwardedProtoMiddleware(BaseHTTPMiddleware):
  """
    Ensures FastAPI respects the original protocol (https/http)
    when behind a reverse proxy (e.g., Nginx, Traefik, etc.)
    """

  async def dispatch(self, request: Request, call_next):
    forwarded_proto = request.headers.get("x-forwarded-proto")
    if forwarded_proto:
      scope = request.scope
      scope["scheme"] = forwarded_proto
    response = await call_next(request)
    return response


app.add_middleware(ForwardedProtoMiddleware)

# Conditional HTTPS redirect middleware for production
if config.settings.ENV == "production":
  app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.settings.allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(perfiles.router)
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(eventos_financieros.router)
app.include_router(financial_health.router)


@app.get("/", tags=["Root"])
def read_root():
  return {"message": "MoneyPilot API is running."}

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
logger = logging.getLogger(__name__)
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables, check_database_connection
from app.routers import usuarios, peliculas, favoritos
from app.config import settings



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup: Crear tablas en la base de datos
    create_db_and_tables()
    yield
    
    # Shutdown: Limpiar recursos si es necesario
    print("cerrando aplicación...")


# TODO: Crear la instancia de FastAPI con metadatos apropiados
# Incluir: title, description, version, contact, license_info
app = FastAPI(
    title="API de Películas",
    description="API RESTful para gestionar usuarios, películas y favoritos",
    version="1.0.0",
    lifespan=lifespan,

    contact={
        "name": "Tu Nombre",
        "email": "tu.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Solicitud: %s %s", request.method, request.url.path)

    response = await call_next(request)

    logger.info(
        "Respuesta: %s %s - %s",
        request.method,
        request.url.path,
        response.status_code,
    )

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "mensaje": exc.detail,
        },
    )
app.include_router(usuarios.router)
app.include_router(peliculas.router)
app.include_router(favoritos.router)
# TODO: Crear un endpoint raíz que retorne información básica de la API
@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.
    Retorna información básica y enlaces a la documentación.
    """
    return {
        "mensaje": "Bienvenido a la API de Películas",
        "version": "1.0.0",
        "documentacion": "/docs",
        "documentacion_alternativa": "/redoc",
        "endpoints": {
            "usuarios": "/api/usuarios",
            "peliculas": "/api/peliculas",
            "favoritos": "/api/favoritos"
        }
    }


# Crear un endpoint de health check para monitoreo
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint para verificar el estado de la API.
    Útil para sistemas de monitoreo y orquestación.
    """
    return {
        "status": "healthy",
        "database": "connected" if check_database_connection() else "disconnected"
    }



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
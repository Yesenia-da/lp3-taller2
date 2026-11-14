"""
Paquete de routers de la API.
Contiene los endpoints organizados por recurso.
"""

from .usuarios import router as usuarios_router
from .peliculas import router as peliculas_router
from .favoritos import router as favoritos_router

__all__ = [
    "usuarios_router",
    "peliculas_router",
    "favoritos_router",
]
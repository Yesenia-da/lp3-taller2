"""
Esquemas Pydantic para validación y serialización de datos.
Estos esquemas se usan en los endpoints de la API para:
- Validar datos de entrada (request)
- Serializar datos de salida (response)
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# =============================================================================
# ESQUEMAS DE USUARIO
# =============================================================================

class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, description="Nombre del usuario")
    correo: EmailStr = Field(description="Correo electrónico único")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez",
                "correo": "juan.perez@email.com"
            }
        }
    )


class UsuarioUpdate(BaseModel):
   
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[EmailStr] = None


class UsuarioRead(BaseModel):
  
    id: int
    nombre: str
    correo: str
    fecha_registro: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UsuarioWithFavoritos(UsuarioRead):
 
    favoritos: List["FavoritoRead"] = Field(default_factory=list)

# =============================================================================
# ESQUEMAS DE PELÍCULA
# =============================================================================

# TODO: Schema para crear una película (request)
class PeliculaCreate(BaseModel):
    
    titulo: str = Field(min_length=1, max_length=200)
    director: str = Field(min_length=1, max_length=150)
    genero: str = Field(min_length=1, max_length=100)
    duracion: int = Field(gt=0, description="Duración en minutos")
    año: int = Field(ge=1888, le=2100, description="Año de estreno")
    clasificacion: str = Field(max_length=10)
    sinopsis: Optional[str] = Field(None, max_length=1000)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "titulo": "Inception",
                "director": "Christopher Nolan",
                "genero": "Ciencia Ficción, Acción",
                "duracion": 148,
                "año": 2010,
                "clasificacion": "PG-13",
                "sinopsis": "Un ladrón que roba secretos mediante tecnología de sueños..."
            }
        }
    )
    pass


class PeliculaUpdate(BaseModel):
 
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, min_length=1, max_length=150)
    genero: Optional[str] = None
    duracion: Optional[int] = Field(None, gt=0)
    año: Optional[int] = Field(None, ge=1888, le=2100)
    clasificacion: Optional[str] = None
    sinopsis: Optional[str] = None



class PeliculaRead(BaseModel):

    id: int
    titulo: str
    director: str
    genero: str
    duracion: int
    año: int
    clasificacion: str
    sinopsis: Optional[str]
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# ESQUEMAS DE FAVORITO
# =============================================================================

class FavoritoCreate(BaseModel):
    id_usuario: int = Field(gt=0)
    id_pelicula: int = Field(gt=0)



class FavoritoRead(BaseModel):

    id: int
    id_usuario: int
    id_pelicula: int
    fecha_marcado: datetime
    
    model_config = ConfigDict(from_attributes=True)


class FavoritoWithDetails(FavoritoRead):
    usuario: UsuarioRead
    pelicula: PeliculaRead


# =============================================================================
# ESQUEMAS DE RESPUESTA GENÉRICOS
# =============================================================================

# TODO: Schema para respuestas con mensajes
class MessageResponse(BaseModel):
    """
    Schema genérico para respuestas con mensajes.
    """
    # message: str
    # detail: Optional[str] = None
    pass


# TODO: Schema para respuestas paginadas
class PaginatedResponse(BaseModel):
    """
    Schema genérico para respuestas paginadas.
    """
    # items: List[BaseModel]
    # total: int
    # page: int = 1
    # size: int = 50
    # pages: int
    pass


# TODO: Opcional - Schema para búsqueda de películas
class PeliculaSearchParams(BaseModel):
    """
    Parámetros de búsqueda para películas.
    """
    # titulo: Optional[str] = None
    # director: Optional[str] = None
    # genero: Optional[str] = None
    # año: Optional[int] = None
    # año_min: Optional[int] = None
    # año_max: Optional[int] = None
    pass


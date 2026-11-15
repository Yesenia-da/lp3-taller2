"""
Modelos de datos usando SQLModel.
Define la estructura de las tablas de la base de datos.
SQLModel combina SQLAlchemy con Pydantic para validación automática.
"""

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

# TODO: Modelo Usuario
class Usuario(SQLModel, table=True):
    """
    Modelo de Usuario.
    Representa a los usuarios registrados en la plataforma.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    correo: str = Field(unique=True, max_length=150, index=True)
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    favoritos: List["Favorito"] = Relationship(back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre={self.nombre}, correo={self.correo})>"

    @property
    def cantidad_favoritos(self) -> int:
        """Retorna la cantidad de películas favoritas del usuario."""
        return len(self.favoritos) if self.favoritos else 0

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Correo electrónico inválido")
        return v.lower()

# TODO: Modelo Pelicula
class Pelicula(SQLModel, table=True):
    """
    Modelo de Película.
    Representa las películas disponibles en la plataforma.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(max_length=200, index=True)
    director: str = Field(max_length=150)
    genero: str = Field(max_length=100)
    duracion: int = Field(description="Duración en minutos")
    año: int = Field(ge=1888, le=2100)
    clasificacion: str = Field(max_length=10)
    sinopsis: Optional[str] = Field(default=None, max_length=1000)
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    favoritos: List["Favorito"] = Relationship(back_populates="pelicula")
    


# TODO: Modelo Favorito
class Favorito(SQLModel, table=True):
    """
    Modelo de Favorito.
    Representa la relación muchos-a-muchos entre usuarios y películas.
    """
    __table_args__ = (
        UniqueConstraint("id_usuario", "id_pelicula", name="unique_user_movie"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id")
    id_pelicula: int = Field(foreign_key="pelicula.id")
    fecha_marcado: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    usuario: Optional[Usuario] = Relationship(back_populates="favoritos")
    pelicula: Optional[Pelicula] = Relationship(back_populates="favoritos")

# TODO: Opcional - Agregar métodos útiles a los modelos
# Ejemplo para Usuario:
# def __repr__(self):
#     return f"<Usuario(id={self.id}, nombre={self.nombre}, correo={self.correo})>"
#
# @property
# def cantidad_favoritos(self) -> int:
#     """Retorna la cantidad de películas favoritas del usuario."""
#     return len(self.favoritos) if self.favoritos else 0


# TODO: Opcional - Agregar validadores personalizados
# from sqlmodel import validator
#
# @validator('correo')
# def validar_correo(cls, v):
#     if '@' not in v:
#         raise ValueError('Correo electrónico inválido')
#     return v.lower()


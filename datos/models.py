from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Usuario:
    """Representa a un usuario de la aplicación."""

    id_usuario: Optional[int] = None
    nombre: str = ""
    email: str = ""

    def __str__(self) -> str:
        return self.nombre


@dataclass
class Categoria:
    """Representa una categoría o etiqueta de receta."""

    id_categoria: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""

    def __str__(self) -> str:
        return self.nombre


@dataclass
class Ingrediente:
    """Representa un ingrediente base disponible en la app."""

    id_ingrediente: Optional[int] = None
    nombre: str = ""
    categoria_ingrediente: str = ""

    def __str__(self) -> str:
        return self.nombre


@dataclass
class DetalleIngrediente:
    """Relaciona una receta con un ingrediente y su cantidad."""

    id_receta: Optional[int] = None
    id_ingrediente: Optional[int] = None
    ingrediente: Optional[Ingrediente] = None
    cantidad: Decimal = Decimal("0")
    unidad_medida: str = ""

    def __str__(self) -> str:
        if self.ingrediente:
            return f"{self.ingrediente.nombre}: {self.cantidad} {self.unidad_medida}"
        return f"{self.cantidad} {self.unidad_medida}"


@dataclass
class Valoracion:
    """Representa la valoración que un usuario hace a una receta."""

    id_valoracion: Optional[int] = None
    puntuacion: int = 0
    comentario: Optional[str] = None
    fecha: Optional[date] = None
    id_usuario: Optional[int] = None
    id_receta: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.puntuacion}/5"


@dataclass
class Receta:
    """Entidad principal del sistema: una receta con sus ingredientes y categorías."""

    id_receta: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    tiempo_preparacion: int = 0
    dificultad: str = "Fácil"
    instrucciones: str = ""
    porciones: int = 4
    imagen_url: Optional[str] = None
    id_usuario: Optional[int] = None
    autor: Optional[Usuario] = None
    categorias: list[Categoria] = field(default_factory=list)
    ingredientes: list[DetalleIngrediente] = field(default_factory=list)
    valoraciones: list[Valoracion] = field(default_factory=list)
    promedio_valoracion: Optional[float] = None
    total_valoraciones: int = 0

    def __str__(self) -> str:
        return self.nombre


@dataclass
class RecetaGuardada:
    """Representa la relación entre usuario y receta guardada."""

    id_usuario: Optional[int] = None
    id_receta: Optional[int] = None
    fecha_guardado: Optional[date] = None


__all__ = [
    "Usuario",
    "Categoria",
    "Ingrediente",
    "DetalleIngrediente",
    "Valoracion",
    "Receta",
    "RecetaGuardada",
]

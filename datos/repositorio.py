from __future__ import annotations

from decimal import Decimal

from datos.Recetas import RECETAS_CHILENAS
from datos.models import (
    Categoria,
    DetalleIngrediente,
    Ingrediente,
    Receta,
    Usuario,
)


class RepositorioRecetas:
    """Repositorio en memoria para gestionar recetas, usuarios, categorías e ingredientes."""

    def __init__(self) -> None:
        self.usuarios: dict[int, Usuario] = {}
        self.categorias: dict[int, Categoria] = {}
        self.ingredientes: dict[int, Ingrediente] = {}
        self.recetas: dict[int, Receta] = {}

        self._proximo_id_usuario = 1
        self._proximo_id_categoria = 1
        self._proximo_id_ingrediente = 1
        self._proximo_id_receta = 1

        self._cargar_datos_demo()

    # ---------- USUARIOS ----------

    def agregar_usuario(self, usuario: Usuario) -> Usuario:
        if usuario.id_usuario is None:
            usuario.id_usuario = self._proximo_id_usuario
            self._proximo_id_usuario += 1
        self.usuarios[usuario.id_usuario] = usuario
        return usuario

    def obtener_usuario(self, id_usuario: int) -> Usuario | None:
        return self.usuarios.get(id_usuario)

    def listar_usuarios(self) -> list[Usuario]:
        return list(self.usuarios.values())

    # ---------- CATEGORÍAS ----------

    def agregar_categoria(self, categoria: Categoria) -> Categoria:
        if categoria.id_categoria is None:
            categoria.id_categoria = self._proximo_id_categoria
            self._proximo_id_categoria += 1
        self.categorias[categoria.id_categoria] = categoria
        return categoria

    def obtener_categoria(self, id_categoria: int) -> Categoria | None:
        return self.categorias.get(id_categoria)

    def listar_categorias(self) -> list[Categoria]:
        return list(self.categorias.values())

    # ---------- INGREDIENTES ----------

    def agregar_ingrediente(self, ingrediente: Ingrediente) -> Ingrediente:
        if ingrediente.id_ingrediente is None:
            ingrediente.id_ingrediente = self._proximo_id_ingrediente
            self._proximo_id_ingrediente += 1
        self.ingredientes[ingrediente.id_ingrediente] = ingrediente
        return ingrediente

    def obtener_ingrediente(self, id_ingrediente: int) -> Ingrediente | None:
        return self.ingredientes.get(id_ingrediente)

    def listar_ingredientes(self) -> list[Ingrediente]:
        return list(self.ingredientes.values())

    # ---------- RECETAS ----------

    def agregar_receta(self, receta: Receta) -> Receta:
        if receta.id_receta is None:
            receta.id_receta = self._proximo_id_receta
            self._proximo_id_receta += 1

        if receta.autor is not None and receta.autor.id_usuario is None:
            self.agregar_usuario(receta.autor)

        if receta.id_usuario is not None and receta.autor is None:
            usuario = self.obtener_usuario(receta.id_usuario)
            if usuario is not None:
                receta.autor = usuario

        self.recetas[receta.id_receta] = receta
        return receta

    def obtener_receta(self, id_receta: int) -> Receta | None:
        return self.recetas.get(id_receta)

    def listar_recetas(self) -> list[Receta]:
        return list(self.recetas.values())

    def buscar_recetas_por_nombre(self, nombre: str) -> list[Receta]:
        texto = nombre.strip().lower()
        if not texto:
            return self.listar_recetas()
        return [
            receta
            for receta in self.recetas.values()
            if texto in receta.nombre.lower() or texto in receta.descripcion.lower()
        ]

    def buscar_recetas_por_categoria(self, nombre_categoria: str) -> list[Receta]:
        texto = nombre_categoria.strip().lower()
        if not texto:
            return self.listar_recetas()

        resultados: list[Receta] = []
        for receta in self.recetas.values():
            for categoria in receta.categorias:
                if texto in categoria.nombre.lower():
                    resultados.append(receta)
                    break
        return resultados

    def editar_receta(self, id_receta: int, receta_nueva: Receta) -> Receta:
        if id_receta not in self.recetas:
            raise ValueError(f"La receta con id {id_receta} no existe.")

        receta_nueva.id_receta = id_receta
        if receta_nueva.autor is not None and receta_nueva.autor.id_usuario is None:
            self.agregar_usuario(receta_nueva.autor)

        self.recetas[id_receta] = receta_nueva
        return receta_nueva

    def eliminar_receta(self, id_receta: int) -> bool:
        return self.recetas.pop(id_receta, None) is not None

    def agregar_ingrediente_a_receta(
        self,
        id_receta: int,
        ingrediente: Ingrediente,
        cantidad: Decimal | int | float,
        unidad_medida: str,
    ) -> DetalleIngrediente:
        receta = self.obtener_receta(id_receta)
        if receta is None:
            raise ValueError(f"La receta con id {id_receta} no existe.")

        ingrediente_guardado = self.obtener_ingrediente(ingrediente.id_ingrediente) if ingrediente.id_ingrediente is not None else None
        if ingrediente_guardado is None:
            ingrediente_guardado = self.agregar_ingrediente(ingrediente)

        detalle = DetalleIngrediente(
            id_receta=id_receta,
            id_ingrediente=ingrediente_guardado.id_ingrediente,
            ingrediente=ingrediente_guardado,
            cantidad=Decimal(str(cantidad)),
            unidad_medida=unidad_medida,
        )
        receta.ingredientes.append(detalle)
        return detalle

    def _cargar_datos_demo(self) -> None:
        usuario1 = self.agregar_usuario(Usuario(id_usuario=None, nombre="Antonia", email="antonia@gmail.com"))
        usuario2 = self.agregar_usuario(Usuario(id_usuario=None, nombre="Joaquín", email="joaquin@gmail.com"))

        for receta_data in RECETAS_CHILENAS:
            categorias = []
            if receta_data.get("tipo"):
                categorias.append(
                    Categoria(
                        id_categoria=None,
                        nombre=receta_data["tipo"],
                        descripcion="Receta chilena recomendada para cocinar en casa.",
                    )
                )
            receta = Receta(
                id_receta=None,
                nombre=receta_data["nombre"],
                descripcion=receta_data["descripcion"],
                tiempo_preparacion=int(receta_data["tiempo_preparacion"]),
                dificultad=receta_data["dificultad"],
                instrucciones="\n".join(receta_data["instrucciones"]),
                porciones=int(receta_data["porciones"]),
                imagen_url=None,
                id_usuario=usuario1.id_usuario,
                autor=usuario1,
                categorias=categorias,
            )

            for ingrediente_data in receta_data["ingredientes"]:
                ingrediente = self.obtener_ingrediente_by_name(ingrediente_data.strip())
                if ingrediente is None:
                    ingrediente = self.agregar_ingrediente(
                        Ingrediente(
                            id_ingrediente=None,
                            nombre=ingrediente_data.strip(),
                            categoria_ingrediente="General",
                        )
                    )

                receta.ingredientes.append(
                    DetalleIngrediente(
                        id_receta=None,
                        id_ingrediente=ingrediente.id_ingrediente,
                        ingrediente=ingrediente,
                        cantidad=Decimal("1"),
                        unidad_medida="unidad",
                    )
                )

            self.agregar_receta(receta)

    def obtener_ingrediente_by_name(self, nombre: str) -> Ingrediente | None:
        texto = nombre.strip().lower()
        for ingrediente in self.ingredientes.values():
            if ingrediente.nombre.lower() == texto:
                return ingrediente
        return None


__all__ = ["RepositorioRecetas"]

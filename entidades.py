"""
entidades.py
============
Define la clase abstracta base `Entidad`, raíz de la jerarquía de
objetos identificables dentro del sistema Software FJ.

Una Entidad representa cualquier objeto del dominio que tiene una
identidad propia (id) y un nombre. Actualmente `Cliente` es la única
subclase concreta, pero el diseño permite extender el sistema en el
futuro (por ejemplo, una clase Empleado) sin modificar código existente
(principio Open/Closed).
"""

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema.

    Toda entidad tiene un identificador único y un nombre. Las
    subclases están obligadas a implementar `validar()` (reglas de
    negocio propias) y `mostrar()` (representación legible para el
    usuario final).

    Attributes:
        id (int): Identificador único de la entidad.
        nombre (str): Nombre descriptivo de la entidad.
    """

    def __init__(self, id_entidad: int, nombre: str) -> None:
        self._id = id_entidad
        self._nombre = nombre

    @property
    def id(self) -> int:
        """int: Identificador único de la entidad (solo lectura)."""
        return self._id

    @property
    def nombre(self) -> str:
        """str: Nombre de la entidad."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre de la entidad no puede estar vacío")
        self._nombre = valor.strip()

    @abstractmethod
    def validar(self) -> bool:
        """Valida las reglas de negocio propias de la subclase.

        Returns:
            bool: True si la entidad es válida.

        Raises:
            SistemaFJError o subclase: si la validación falla.
        """
        raise NotImplementedError

    @abstractmethod
    def mostrar(self) -> str:
        """Devuelve una representación legible de la entidad.

        Returns:
            str: Descripción en texto de la entidad.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id} nombre='{self._nombre}'>"

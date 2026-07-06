"""
cliente.py
==========
Define la clase concreta `Cliente`, que hereda de `Entidad` (ver
entidades.py) y representa a un cliente de Software FJ.

Aplica encapsulamiento estricto: todos los atributos sensibles
(documento, correo, teléfono) se exponen únicamente mediante
propiedades (`@property` / `@x.setter`), que validan los datos en el
momento de la asignación. Esto garantiza que nunca exista en memoria
un objeto Cliente en estado inconsistente.
"""

import re
from typing import Final

from entidades import Entidad
from excepciones import ClienteInvalidoError
from logger import obtener_logger

logger = obtener_logger(__name__)

_PATRON_CORREO: Final[re.Pattern] = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)
_PATRON_TELEFONO: Final[re.Pattern] = re.compile(r"^\+?\d{7,15}$")


class Cliente(Entidad):
    """Representa un cliente de Software FJ.

    Hereda de `Entidad` y agrega los atributos propios de un cliente:
    documento de identidad, correo electrónico y teléfono de contacto.

    Attributes:
        documento (str): Número de documento de identidad (no vacío).
        correo (str): Correo electrónico en formato válido.
        telefono (str): Teléfono de contacto (7 a 15 dígitos, opcional '+').
    """

    def __init__(
        self,
        id_entidad: int,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str,
    ) -> None:
        # Se inicializan primero los atributos "privados" para que las
        # propiedades (con validación) puedan asignarse de forma segura.
        super().__init__(id_entidad, nombre)
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        logger.info(
            "Cliente inicializado: id=%s, nombre='%s', documento='%s'",
            self.id, self.nombre, self.documento,
        )

    # ------------------------------------------------------------------
    # Propiedad: documento
    # ------------------------------------------------------------------
    @property
    def documento(self) -> str:
        """str: Número de documento del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ClienteInvalidoError(
                "El documento del cliente no puede estar vacío"
            )
        self._documento = str(valor).strip()

    # ------------------------------------------------------------------
    # Propiedad: correo
    # ------------------------------------------------------------------
    @property
    def correo(self) -> str:
        """str: Correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not _PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(
                f"Correo electrónico inválido: '{valor}'"
            )
        self._correo = valor.strip().lower()

    # ------------------------------------------------------------------
    # Propiedad: telefono
    # ------------------------------------------------------------------
    @property
    def telefono(self) -> str:
        """str: Teléfono de contacto del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not _PATRON_TELEFONO.match(valor.strip()):
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{valor}' "
                "(se esperan entre 7 y 15 dígitos, '+' opcional)"
            )
        self._telefono = valor.strip()

    # ------------------------------------------------------------------
    # Implementación de métodos abstractos de Entidad
    # ------------------------------------------------------------------
    def validar(self) -> bool:
        """Valida que el cliente tenga todos sus datos en regla.

        Como los setters ya validan en el momento de la asignación,
        este método re-verifica el estado actual (útil si se llama
        explícitamente tras varias modificaciones).

        Returns:
            bool: True si el cliente es válido.

        Raises:
            ClienteInvalidoError: si algún dato no cumple las reglas.
        """
        # Reutiliza los propios setters para forzar la validación.
        self.documento = self._documento
        self.correo = self._correo
        self.telefono = self._telefono
        return True

    def mostrar(self) -> str:
        """Devuelve una representación legible del cliente."""
        return (
            f"Cliente #{self.id} | {self.nombre} | Doc: {self.documento} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )

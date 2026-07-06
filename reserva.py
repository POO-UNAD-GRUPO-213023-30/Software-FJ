"""
reserva.py
==========
Define la clase `Reserva`, que integra un `Cliente` (cliente.py) y un
`Servicio` (servicio.py), junto con duración y estado, e implementa el
ciclo de vida completo de una reserva: confirmación, cancelación y
procesamiento final (cálculo de costo).

Esta clase es un ejemplo de COMPOSICIÓN de objetos: una Reserva "tiene
un" Cliente y "tiene un" Servicio, en lugar de heredar de ellos.
"""

from enum import Enum
from typing import Optional

from cliente import Cliente
from excepciones import (
    CostoInvalidoError,
    DuracionInvalidaError,
    ReservaError,
)
from logger import obtener_logger
from servicio import Servicio

logger = obtener_logger(__name__)


class EstadoReserva(Enum):
    """Estados posibles del ciclo de vida de una reserva."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"


class Reserva:
    """Representa una reserva de un servicio de Software FJ por parte
    de un cliente.

    Attributes:
        id (int): Identificador único de la reserva.
        cliente (Cliente): Cliente que realiza la reserva.
        servicio (Servicio): Servicio reservado (polimórfico).
        duracion (float): Duración de la reserva (horas, días, etc.
            según el tipo de servicio).
        estado (EstadoReserva): Estado actual de la reserva.
    """

    def __init__(
        self,
        id_reserva: int,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
    ) -> None:
        if not isinstance(cliente, Cliente):
            raise ReservaError(
                f"Se esperaba un objeto Cliente, se recibió {type(cliente).__name__}"
            )
        if not isinstance(servicio, Servicio):
            raise ReservaError(
                f"Se esperaba un objeto Servicio, se recibió {type(servicio).__name__}"
            )

        self.id = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion  # usa el setter con validación
        self.estado = EstadoReserva.PENDIENTE
        self.costo_final: Optional[float] = None

        logger.info(
            "Reserva #%s creada (pendiente): cliente='%s', servicio='%s', duracion=%s",
            self.id, cliente.nombre, servicio.nombre, self.duracion,
        )

    @property
    def duracion(self) -> float:
        """float: Duración de la reserva. Debe ser un número positivo."""
        return self._duracion

    @duracion.setter
    def duracion(self, valor: float) -> None:
        try:
            valor_numerico = float(valor)
        except (TypeError, ValueError) as error:
            raise DuracionInvalidaError(
                f"La duración debe ser numérica (recibido {valor!r})"
            ) from error
        if valor_numerico <= 0:
            raise DuracionInvalidaError(
                f"La duración debe ser mayor que cero (recibido {valor_numerico})"
            )
        self._duracion = valor_numerico

    def confirmar(self) -> None:
        """Confirma la reserva, siempre que esté en estado PENDIENTE.

        Raises:
            ReservaError: si la reserva no está en un estado que
                permita ser confirmada (ej. ya cancelada o procesada).
        """
        if self.estado != EstadoReserva.PENDIENTE:
            raise ReservaError(
                f"No se puede confirmar la reserva #{self.id}: "
                f"estado actual es {self.estado.value}"
            )
        self.estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva #%s confirmada", self.id)

    def cancelar(self) -> None:
        """Cancela la reserva, siempre que no haya sido ya procesada.

        Raises:
            ReservaError: si la reserva ya fue procesada o ya estaba
                cancelada previamente.
        """
        if self.estado == EstadoReserva.PROCESADA:
            raise ReservaError(
                f"No se puede cancelar la reserva #{self.id}: ya fue procesada"
            )
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservaError(
                f"La reserva #{self.id} ya se encontraba cancelada"
            )
        self.estado = EstadoReserva.CANCELADA
        logger.warning("Reserva #%s cancelada", self.id)

    def procesar(
        self,
        impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
    ) -> float:
        """Procesa la reserva: calcula el costo final delegando en el
        servicio asociado (polimorfismo) y marca la reserva como
        PROCESADA.

        Debe confirmarse primero la reserva antes de procesarla.

        Args:
            impuesto: Porcentaje de impuesto opcional (ej. 0.19).
            descuento: Porcentaje de descuento opcional (ej. 0.10).

        Returns:
            float: Costo final de la reserva.

        Raises:
            ReservaError: si la reserva no está confirmada.
            CostoInvalidoError: si el cálculo de costo del servicio falla,
                encadenando la excepción original del servicio.
        """
        if self.estado != EstadoReserva.CONFIRMADA:
            raise ReservaError(
                f"No se puede procesar la reserva #{self.id}: "
                f"debe estar CONFIRMADA (estado actual: {self.estado.value})"
            )

        try:
            costo = self.servicio.calcular_costo(impuesto=impuesto, descuento=descuento)
        except CostoInvalidoError as error:
            # Encadenamiento de excepciones: se preserva la causa original.
            raise CostoInvalidoError(
                f"No fue posible calcular el costo de la reserva #{self.id}"
            ) from error

        self.costo_final = costo
        self.estado = EstadoReserva.PROCESADA
        logger.info(
            "Reserva #%s procesada correctamente: costo final=$%.2f",
            self.id, costo,
        )
        return costo

    def mostrar(self) -> str:
        """Devuelve una representación legible y completa de la reserva."""
        costo_str = f"${self.costo_final:,.2f}" if self.costo_final is not None else "N/A"
        return (
            f"Reserva #{self.id} | Estado: {self.estado.value} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | Costo final: {costo_str}"
        )

    def __repr__(self) -> str:
        return f"<Reserva id={self.id} estado={self.estado.value}>"

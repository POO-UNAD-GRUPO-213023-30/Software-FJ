"""
utilidades.py
=============
Funciones y clases auxiliares reutilizables por todo el sistema.

Contiene:
    - `GeneradorId`: generador simple de identificadores autoincrementales.
    - `GestorFJ`: fachada en memoria que administra las listas de
      clientes, servicios y reservas (sin base de datos), incluyendo
      detección de reservas duplicadas.
"""

from typing import List, Optional

from cliente import Cliente
from excepciones import ReservaError
from logger import obtener_logger
from reserva import Reserva
from servicio import Servicio

logger = obtener_logger(__name__)


class GeneradorId:
    """Generador simple de identificadores únicos autoincrementales."""

    def __init__(self, inicio: int = 1) -> None:
        self._actual = inicio

    def siguiente(self) -> int:
        """Devuelve el siguiente id disponible y avanza el contador."""
        valor = self._actual
        self._actual += 1
        return valor


class GestorFJ:
    """Fachada en memoria que centraliza clientes, servicios y reservas.

    Toda la información se mantiene únicamente en listas dentro de esta
    clase (sin bases de datos), tal como exige la guía de la actividad.

    Attributes:
        clientes (List[Cliente]): Clientes registrados exitosamente.
        servicios (List[Servicio]): Servicios creados exitosamente.
        reservas (List[Reserva]): Reservas creadas exitosamente.
    """

    def __init__(self) -> None:
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        self._id_clientes = GeneradorId()
        self._id_reservas = GeneradorId()

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------
    def registrar_cliente(
        self, nombre: str, documento: str, correo: str, telefono: str
    ) -> Cliente:
        """Crea, valida y registra un nuevo cliente.

        Raises:
            ClienteInvalidoError: si algún dato del cliente es inválido
                (propagada desde el constructor de Cliente).
        """
        nuevo_id = self._id_clientes.siguiente()
        cliente = Cliente(nuevo_id, nombre, documento, correo, telefono)
        cliente.validar()
        self.clientes.append(cliente)
        logger.info("Cliente registrado en el sistema: %s", cliente.mostrar())
        return cliente

    def buscar_cliente_por_documento(self, documento: str) -> Optional[Cliente]:
        """Busca un cliente registrado por su número de documento."""
        return next((c for c in self.clientes if c.documento == documento), None)

    # ------------------------------------------------------------------
    # Servicios
    # ------------------------------------------------------------------
    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        """Registra un servicio ya construido en el catálogo del sistema.

        El servicio debe haberse construido previamente (su propio
        constructor ya valida sus atributos); aquí solo se añade al
        catálogo interno.
        """
        self.servicios.append(servicio)
        logger.info("Servicio registrado en catálogo: %s", servicio.descripcion())
        return servicio

    # ------------------------------------------------------------------
    # Reservas
    # ------------------------------------------------------------------
    def existe_reserva_duplicada(self, cliente: Cliente, servicio: Servicio) -> bool:
        """Indica si ya existe una reserva activa (no cancelada) para el
        mismo cliente y el mismo servicio."""
        for reserva in self.reservas:
            if (
                reserva.cliente.documento == cliente.documento
                and reserva.servicio is servicio
                and reserva.estado.value != "CANCELADA"
            ):
                return True
        return False

    def crear_reserva(
        self, cliente: Cliente, servicio: Servicio, duracion: float
    ) -> Reserva:
        """Crea una nueva reserva, validando que no exista una duplicada.

        Raises:
            ReservaError: si ya existe una reserva activa para el mismo
                cliente y servicio.
            DuracionInvalidaError: si la duración no es válida
                (propagada desde el constructor de Reserva).
        """
        if self.existe_reserva_duplicada(cliente, servicio):
            raise ReservaError(
                f"El cliente '{cliente.nombre}' ya tiene una reserva activa "
                f"para el servicio '{servicio.nombre}'"
            )
        nuevo_id = self._id_reservas.siguiente()
        reserva = Reserva(nuevo_id, cliente, servicio, duracion)
        self.reservas.append(reserva)
        return reserva

    # ------------------------------------------------------------------
    # Reportes
    # ------------------------------------------------------------------
    def resumen(self) -> str:
        """Genera un resumen textual del estado actual del sistema."""
        lineas = [
            "=" * 60,
            "RESUMEN DEL SISTEMA - SOFTWARE FJ",
            "=" * 60,
            f"Clientes registrados: {len(self.clientes)}",
            f"Servicios en catálogo: {len(self.servicios)}",
            f"Reservas creadas: {len(self.reservas)}",
            "-" * 60,
        ]
        for reserva in self.reservas:
            lineas.append(reserva.mostrar())
        lineas.append("=" * 60)
        return "\n".join(lineas)

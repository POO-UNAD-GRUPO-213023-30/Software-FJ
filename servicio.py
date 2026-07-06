"""
servicio.py
===========
Define la clase abstracta `Servicio` y tres servicios especializados
que Software FJ ofrece: reserva de salas, alquiler de equipos y
asesorías especializadas.

Este módulo es el ejemplo central de POLIMORFISMO del sistema: la
clase `Reserva` (ver reserva.py) interactúa siempre con la interfaz
`Servicio`, sin importar cuál subclase concreta reciba. Cada subclase
sobrescribe `calcular_costo()` y `descripcion()` con su propia lógica.

También demuestra SOBRECARGA (simulada mediante argumentos opcionales
con valores por defecto, ya que Python no soporta firmas múltiples de
forma nativa): `calcular_costo()` admite variantes con impuesto y/o
descuento.
"""

from abc import ABC, abstractmethod
from typing import Optional

from excepciones import CostoInvalidoError, ServicioNoDisponibleError
from logger import obtener_logger

logger = obtener_logger(__name__)


class Servicio(ABC):
    """Clase abstracta que representa un servicio genérico de Software FJ.

    Attributes:
        nombre (str): Nombre comercial del servicio.
        costo_base (float): Costo base del servicio, siempre > 0.
    """

    def __init__(self, nombre: str, costo_base: float) -> None:
        self.nombre = nombre
        self.costo_base = costo_base  # usa el setter con validación

    @property
    def nombre(self) -> str:
        """str: Nombre del servicio."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ServicioNoDisponibleError(
                "El nombre del servicio no puede estar vacío"
            )
        self._nombre = valor.strip()

    @property
    def costo_base(self) -> float:
        """float: Costo base (antes de impuestos/descuentos)."""
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor: float) -> None:
        try:
            valor_numerico = float(valor)
        except (TypeError, ValueError) as error:
            raise CostoInvalidoError(
                f"El costo base debe ser numérico, se recibió: {valor!r}"
            ) from error
        if valor_numerico <= 0:
            raise CostoInvalidoError(
                f"El costo base debe ser mayor que cero (recibido {valor_numerico})"
            )
        self._costo_base = valor_numerico

    def _aplicar_impuesto_y_descuento(
        self,
        monto: float,
        impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
    ) -> float:
        """Aplica impuesto y descuento porcentuales a un monto base.

        Método auxiliar reutilizado por todas las subclases para evitar
        duplicar la lógica de impuestos/descuentos (DRY).

        Args:
            monto: Monto base sobre el cual calcular.
            impuesto: Porcentaje de impuesto (ej. 0.19 para 19%). Opcional.
            descuento: Porcentaje de descuento (ej. 0.10 para 10%). Opcional.

        Returns:
            float: Monto final ya con impuesto y descuento aplicados.

        Raises:
            CostoInvalidoError: si impuesto o descuento son negativos,
                o si el descuento supera el 100%.
        """
        if impuesto is not None and impuesto < 0:
            raise CostoInvalidoError(f"El impuesto no puede ser negativo ({impuesto})")
        if descuento is not None and not (0 <= descuento <= 1):
            raise CostoInvalidoError(
                f"El descuento debe estar entre 0 y 1 ({descuento})"
            )

        total = monto
        if descuento:
            total -= total * descuento
        if impuesto:
            total += total * impuesto

        if total < 0:
            raise CostoInvalidoError(
                f"El costo calculado resultó negativo ({total}), revise los parámetros"
            )
        return round(total, 2)

    @abstractmethod
    def calcular_costo(
        self,
        impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
    ) -> float:
        """Calcula el costo final del servicio.

        Args:
            impuesto: Porcentaje de impuesto opcional (ej. 0.19).
            descuento: Porcentaje de descuento opcional (ej. 0.10).

        Returns:
            float: Costo final calculado.
        """
        raise NotImplementedError

    @abstractmethod
    def descripcion(self) -> str:
        """Devuelve una descripción legible del servicio concreto."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} nombre='{self.nombre}'>"


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones o eventos.

    Attributes:
        capacidad (int): Número máximo de personas que admite la sala.
        aire_acondicionado (bool): Indica si la sala cuenta con A/C.
    """

    _RECARGO_AC = 0.15  # 15% adicional si tiene aire acondicionado

    def __init__(
        self,
        nombre: str,
        costo_base: float,
        capacidad: int,
        aire_acondicionado: bool = False,
    ) -> None:
        super().__init__(nombre, costo_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioNoDisponibleError(
                f"La capacidad de la sala debe ser un entero positivo (recibido {capacidad!r})"
            )
        self.capacidad = capacidad
        self.aire_acondicionado = aire_acondicionado

    def calcular_costo(
        self,
        impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
    ) -> float:
        base = self.costo_base
        if self.aire_acondicionado:
            base += base * self._RECARGO_AC
        return self._aplicar_impuesto_y_descuento(base, impuesto, descuento)

    def descripcion(self) -> str:
        ac = "con aire acondicionado" if self.aire_acondicionado else "sin aire acondicionado"
        return (
            f"Reserva de sala '{self.nombre}' | capacidad: {self.capacidad} "
            f"personas | {ac} | costo base: ${self.costo_base:,.2f}"
        )


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos.

    Attributes:
        tipo (str): Tipo de equipo (ej. 'Proyector', 'Portátil').
        cantidad (int): Cantidad de unidades a alquilar.
    """

    def __init__(
        self,
        nombre: str,
        costo_base: float,
        tipo: str,
        cantidad: int,
    ) -> None:
        super().__init__(nombre, costo_base)
        if not tipo or not tipo.strip():
            raise ServicioNoDisponibleError("El tipo de equipo no puede estar vacío")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioNoDisponibleError(
                f"La cantidad debe ser un entero positivo (recibido {cantidad!r})"
            )
        self.tipo = tipo.strip()
        self.cantidad = cantidad

    def calcular_costo(
        self,
        impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
    ) -> float:
        base = self.costo_base * self.cantidad
        return self._aplicar_impuesto_y_descuento(base, impuesto, descuento)

    def descripcion(self) -> str:
        return (
            f"Alquiler de equipo '{self.nombre}' | tipo: {self.tipo} | "
            f"cantidad: {self.cantidad} | costo base unitario: ${self.costo_base:,.2f}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada por horas.

    Attributes:
        especialidad (str): Área de la asesoría (ej. 'Ciberseguridad').
        horas (float): Cantidad de horas contratadas.
    """

    def __init__(
        self,
        nombre: str,
        costo_base: float,
        especialidad: str,
        horas: float,
    ) -> None:
        super().__init__(nombre, costo_base)
        if not especialidad or not especialidad.strip():
            raise ServicioNoDisponibleError("La especialidad no puede estar vacía")
        try:
            horas_numericas = float(horas)
        except (TypeError, ValueError) as error:
            raise ServicioNoDisponibleError(
                f"Las horas deben ser numéricas (recibido {horas!r})"
            ) from error
        if horas_numericas <= 0:
            raise ServicioNoDisponibleError(
                f"Las horas deben ser mayores que cero (recibido {horas_numericas})"
            )
        self.especialidad = especialidad.strip()
        self.horas = horas_numericas

    def calcular_costo(
        self,
        impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
    ) -> float:
        base = self.costo_base * self.horas
        return self._aplicar_impuesto_y_descuento(base, impuesto, descuento)

    def descripcion(self) -> str:
        return (
            f"Asesoría especializada '{self.nombre}' | especialidad: "
            f"{self.especialidad} | horas: {self.horas} | "
            f"costo base por hora: ${self.costo_base:,.2f}"
        )

"""
excepciones.py
===============
Módulo central de excepciones personalizadas para el Sistema de Gestión
de Clientes, Servicios y Reservas de Software FJ.

Todas las excepciones del dominio heredan de `SistemaFJError`, que a su
vez hereda de `Exception`. Esto permite capturar errores específicos
(por ejemplo, solo errores de reserva) o, si es necesario, capturar
cualquier error del dominio con una sola clase base.

Diseño:
    Exception
        └── SistemaFJError            (raíz común del dominio)
                ├── ClienteInvalidoError
                ├── ServicioNoDisponibleError
                ├── ReservaError
                ├── DuracionInvalidaError
                └── CostoInvalidoError
"""


class SistemaFJError(Exception):
    """Excepción base para todos los errores del dominio Software FJ.

    Permite capturar de forma genérica cualquier error propio del
    sistema sin atrapar excepciones ajenas (ValueError, TypeError, etc.)
    que no fueron previstas explícitamente.
    """

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ClienteInvalidoError(SistemaFJError):
    """Se lanza cuando los datos de un cliente no cumplen las reglas
    de validación (documento vacío, correo inválido, teléfono inválido,
    nombre vacío, etc.)."""


class ServicioNoDisponibleError(SistemaFJError):
    """Se lanza cuando se intenta operar sobre un servicio que no existe,
    no está registrado en el catálogo, o fue creado con parámetros que
    lo invalidan (por ejemplo, capacidad <= 0)."""


class ReservaError(SistemaFJError):
    """Se lanza ante cualquier operación inválida sobre una reserva:
    confirmar una reserva ya cancelada, cancelar una ya procesada,
    reservas duplicadas para el mismo cliente/servicio, etc."""


class DuracionInvalidaError(SistemaFJError):
    """Se lanza cuando la duración de una reserva es negativa, cero,
    o de un tipo no numérico."""


class CostoInvalidoError(SistemaFJError):
    """Se lanza cuando el cálculo de un costo produce un valor negativo
    o inconsistente (por ejemplo, un descuento mayor al 100%)."""

"""
logger.py
=========
Configuración centralizada de logging para todo el Sistema de Gestión
de Software FJ.

Objetivo:
    - Un único punto de configuración (evita handlers duplicados).
    - Salida simultánea a archivo (logs/sistema.log) y a consola.
    - Formato uniforme con fecha, nivel, módulo y mensaje.

Uso típico en otros módulos:
    from logger import obtener_logger
    logger = obtener_logger(__name__)
    logger.info("Cliente creado correctamente")
    logger.error("Fallo al crear reserva", exc_info=True)
"""

import logging
import os
from typing import Final

_CARPETA_LOGS: Final[str] = os.path.join(os.path.dirname(__file__), "logs")
_ARCHIVO_LOG: Final[str] = os.path.join(_CARPETA_LOGS, "sistema.log")

_configurado = False


def _configurar_logging_raiz() -> None:
    """Configura el logger raíz una única vez (idempotente).

    Crea la carpeta 'logs' si no existe y agrega dos handlers:
    uno de archivo (todos los niveles desde DEBUG) y uno de consola
    (desde INFO hacia arriba, para no saturar la salida estándar).
    """
    global _configurado
    if _configurado:
        return

    os.makedirs(_CARPETA_LOGS, exist_ok=True)

    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger_raiz = logging.getLogger("SistemaFJ")
    logger_raiz.setLevel(logging.DEBUG)

    handler_archivo = logging.FileHandler(_ARCHIVO_LOG, encoding="utf-8")
    handler_archivo.setLevel(logging.DEBUG)
    handler_archivo.setFormatter(formato)

    handler_consola = logging.StreamHandler()
    handler_consola.setLevel(logging.INFO)
    handler_consola.setFormatter(formato)

    logger_raiz.addHandler(handler_archivo)
    logger_raiz.addHandler(handler_consola)
    logger_raiz.propagate = False

    _configurado = True


def obtener_logger(nombre_modulo: str) -> logging.Logger:
    """Devuelve un logger hijo del logger raíz 'SistemaFJ'.

    Args:
        nombre_modulo: normalmente se pasa __name__ del módulo que
            solicita el logger, para identificar el origen del mensaje.

    Returns:
        Una instancia de logging.Logger lista para usar.
    """
    _configurar_logging_raiz()
    return logging.getLogger(f"SistemaFJ.{nombre_modulo}")

"""
main.py
=======
Punto de entrada del Sistema Integral de Gestión de Clientes, Servicios
y Reservas de Software FJ.

Simula más de 10 operaciones completas del negocio, incluyendo casos
válidos e inválidos, demostrando que el sistema permanece estable y
operativo incluso cuando se presentan errores graves. Cada operación
está aislada en su propio bloque try/except/else/finally para que un
fallo puntual jamás detenga la ejecución global del programa.
"""

from excepciones import (
    ClienteInvalidoError,
    CostoInvalidoError,
    DuracionInvalidaError,
    ReservaError,
    ServicioNoDisponibleError,
    SistemaFJError,
)
from logger import obtener_logger
from servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from utilidades import GestorFJ

logger = obtener_logger(__name__)


def operacion(numero: int, descripcion: str) -> None:
    """Imprime y registra el encabezado de cada operación de la simulación,
    manteniendo main.py legible."""
    print(f"\n[Operación {numero:02d}] {descripcion}")
    logger.info("Iniciando operación %02d: %s", numero, descripcion)


def main() -> None:
    """Ejecuta la simulación completa de operaciones del sistema."""
    gestor = GestorFJ()
    print("SISTEMA DE GESTIÓN SOFTWARE FJ — INICIO DE SIMULACIÓN")
    logger.info("=== Inicio de simulación del sistema Software FJ ===")

    # ------------------------------------------------------------------
    # Operación 1: Registrar cliente correcto
    # ------------------------------------------------------------------
    operacion(1, "Registrar cliente válido (Ana Torres)")
    cliente_ana = None
    try:
        cliente_ana = gestor.registrar_cliente(
            nombre="Ana Torres",
            documento="1020304050",
            correo="ana.torres@example.com",
            telefono="+573001234567",
        )
    except ClienteInvalidoError as error:
        print(f"  ERROR: {error}")
        logger.error("Fallo registrando cliente válido: %s", error)
    else:
        print(f"  OK: {cliente_ana.mostrar()}")
    finally:
        print("  -> Operación 1 finalizada.")

    # ------------------------------------------------------------------
    # Operación 2: Registrar cliente incorrecto (correo inválido)
    # ------------------------------------------------------------------
    operacion(2, "Registrar cliente inválido (correo mal formado)")
    try:
        gestor.registrar_cliente(
            nombre="Carlos Ruiz",
            documento="1122334455",
            correo="carlos_correo_invalido",
            telefono="3009876543",
        )
    except ClienteInvalidoError as error:
        print(f"  ERROR controlado: {error}")
        logger.warning("Registro de cliente rechazado: %s", error)
    else:
        print("  OK: cliente registrado (inesperado)")
    finally:
        print("  -> Operación 2 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Operación 3: Registrar segundo cliente válido
    # ------------------------------------------------------------------
    operacion(3, "Registrar cliente válido (Luis Gómez)")
    cliente_luis = None
    try:
        cliente_luis = gestor.registrar_cliente(
            nombre="Luis Gómez",
            documento="900123456",
            correo="luis.gomez@softwarefj.com",
            telefono="3157894561",
        )
    except ClienteInvalidoError as error:
        print(f"  ERROR: {error}")
        logger.error(error)
    else:
        print(f"  OK: {cliente_luis.mostrar()}")
    finally:
        print("  -> Operación 3 finalizada.")

    # ------------------------------------------------------------------
    # Operación 4: Crear servicio válido (ReservaSala)
    # ------------------------------------------------------------------
    operacion(4, "Crear servicio válido: ReservaSala")
    sala_juntas = None
    try:
        sala_juntas = ReservaSala(
            nombre="Sala de Juntas Principal",
            costo_base=150000,
            capacidad=12,
            aire_acondicionado=True,
        )
        gestor.registrar_servicio(sala_juntas)
    except ServicioNoDisponibleError as error:
        print(f"  ERROR: {error}")
        logger.error(error)
    else:
        print(f"  OK: {sala_juntas.descripcion()}")
    finally:
        print("  -> Operación 4 finalizada.")

    # ------------------------------------------------------------------
    # Operación 5: Crear servicio inválido (capacidad negativa)
    # ------------------------------------------------------------------
    operacion(5, "Crear servicio inválido: capacidad negativa")
    try:
        ReservaSala(
            nombre="Sala Defectuosa",
            costo_base=100000,
            capacidad=-5,
            aire_acondicionado=False,
        )
    except ServicioNoDisponibleError as error:
        print(f"  ERROR controlado: {error}")
        logger.warning("Creación de servicio rechazada: %s", error)
    else:
        print("  OK: servicio creado (inesperado)")
    finally:
        print("  -> Operación 5 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Operación 6: Crear servicios adicionales válidos (polimorfismo)
    # ------------------------------------------------------------------
    operacion(6, "Crear servicios adicionales: AlquilerEquipo y AsesoriaEspecializada")
    proyector = None
    asesoria_ti = None
    try:
        proyector = AlquilerEquipo(
            nombre="Proyector Full HD", costo_base=40000, tipo="Proyector", cantidad=2
        )
        asesoria_ti = AsesoriaEspecializada(
            nombre="Asesoría en Ciberseguridad",
            costo_base=80000,
            especialidad="Ciberseguridad",
            horas=5,
        )
        gestor.registrar_servicio(proyector)
        gestor.registrar_servicio(asesoria_ti)
    except SistemaFJError as error:
        print(f"  ERROR: {error}")
        logger.error(error)
    else:
        print(f"  OK: {proyector.descripcion()}")
        print(f"  OK: {asesoria_ti.descripcion()}")
    finally:
        print("  -> Operación 6 finalizada.")

    # ------------------------------------------------------------------
    # Operación 7: Crear reserva correcta y procesarla
    # ------------------------------------------------------------------
    operacion(7, "Crear y procesar reserva exitosa (Ana Torres / Sala de Juntas)")
    reserva_ana = None
    try:
        reserva_ana = gestor.crear_reserva(cliente_ana, sala_juntas, duracion=3)
        reserva_ana.confirmar()
        costo = reserva_ana.procesar(impuesto=0.19, descuento=0.05)
    except (ReservaError, DuracionInvalidaError, CostoInvalidoError) as error:
        print(f"  ERROR: {error}")
        logger.error(error)
    else:
        print(f"  OK: {reserva_ana.mostrar()} (costo calculado: ${costo:,.2f})")
    finally:
        print("  -> Operación 7 finalizada.")

    # ------------------------------------------------------------------
    # Operación 8: Intentar reservar un servicio inexistente (None)
    # ------------------------------------------------------------------
    operacion(8, "Intentar reservar un servicio inexistente")
    try:
        servicio_inexistente = None
        gestor.crear_reserva(cliente_luis, servicio_inexistente, duracion=2)
    except ReservaError as error:
        print(f"  ERROR controlado: {error}")
        logger.warning("Intento de reserva sobre servicio inexistente: %s", error)
    else:
        print("  OK: reserva creada (inesperado)")
    finally:
        print("  -> Operación 8 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Operación 9: Duración negativa (DuracionInvalidaError)
    # ------------------------------------------------------------------
    operacion(9, "Crear reserva con duración negativa")
    try:
        gestor.crear_reserva(cliente_luis, proyector, duracion=-4)
    except DuracionInvalidaError as error:
        print(f"  ERROR controlado: {error}")
        logger.warning("Duración inválida detectada: %s", error)
    else:
        print("  OK: reserva creada (inesperado)")
    finally:
        print("  -> Operación 9 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Operación 10: Reserva válida para Luis, luego cancelarla
    # ------------------------------------------------------------------
    operacion(10, "Crear reserva de asesoría para Luis y luego cancelarla")
    reserva_luis = None
    try:
        reserva_luis = gestor.crear_reserva(cliente_luis, asesoria_ti, duracion=5)
        reserva_luis.confirmar()
        print(f"  OK: {reserva_luis.mostrar()}")
        reserva_luis.cancelar()
        print(f"  OK: reserva cancelada -> {reserva_luis.mostrar()}")
    except (ReservaError, DuracionInvalidaError) as error:
        print(f"  ERROR: {error}")
        logger.error(error)
    else:
        print("  -> Cancelación completada sin errores.")
    finally:
        print("  -> Operación 10 finalizada.")

    # ------------------------------------------------------------------
    # Operación 11: Procesar una reserva ya cancelada
    #   (demuestra encadenamiento de excepciones con 'raise ... from')
    # ------------------------------------------------------------------
    operacion(11, "Intentar procesar una reserva ya cancelada")
    try:
        try:
            reserva_luis.procesar()
        except ReservaError as error_original:
            raise ReservaError(
                "No fue posible completar el procesamiento solicitado"
            ) from error_original
    except ReservaError as error:
        print(f"  ERROR controlado (encadenado): {error}")
        if error.__cause__:
            print(f"    Causa original: {error.__cause__}")
        logger.error("Error encadenado al procesar reserva cancelada: %s", error)
    else:
        print("  OK: reserva procesada (inesperado)")
    finally:
        print("  -> Operación 11 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Operación 12: Costo inválido (descuento fuera de rango)
    # ------------------------------------------------------------------
    operacion(12, "Procesar reserva con parámetros de costo inválidos")
    try:
        reserva_extra = gestor.crear_reserva(cliente_ana, proyector, duracion=1)
        reserva_extra.confirmar()
        reserva_extra.procesar(descuento=1.5)  # descuento > 100%, inválido
    except CostoInvalidoError as error:
        print(f"  ERROR controlado: {error}")
        if error.__cause__:
            print(f"    Causa original: {error.__cause__}")
        logger.error("Costo inválido detectado: %s", error)
    except ReservaError as error:
        print(f"  ERROR: {error}")
        logger.error(error)
    else:
        print("  OK: reserva procesada (inesperado)")
    finally:
        print("  -> Operación 12 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Operación 13: Reserva duplicada (mismo cliente + mismo servicio activo)
    # ------------------------------------------------------------------
    operacion(13, "Intentar crear una reserva duplicada")
    try:
        gestor.crear_reserva(cliente_ana, sala_juntas, duracion=2)
    except ReservaError as error:
        print(f"  ERROR controlado: {error}")
        logger.warning("Reserva duplicada rechazada: %s", error)
    else:
        print("  OK: reserva creada (inesperado)")
    finally:
        print("  -> Operación 13 finalizada. El sistema sigue activo.")

    # ------------------------------------------------------------------
    # Resumen final
    # ------------------------------------------------------------------
    print("\n" + gestor.resumen())
    logger.info("=== Fin de la simulación. El sistema finalizó sin caídas. ===")
    print("\nSimulación finalizada. Revise 'logs/sistema.log' para el detalle completo.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # noqa: BLE001 - salvaguarda de última instancia
        # Cualquier error verdaderamente inesperado (no contemplado por las
        # excepciones propias del dominio) se registra como CRITICAL y se
        # informa al usuario, pero SIN dejar que el intérprete termine con
        # un traceback crudo. Esta es la última línea de defensa del
        # sistema para garantizar que nunca finalice de forma abrupta.
        logger.critical("Error crítico no controlado en main(): %s", error, exc_info=True)
        print(
            "\nSe produjo un error crítico inesperado. La operación se "
            "detuvo de forma controlada. Revise 'logs/sistema.log' para "
            "más detalles."
        )

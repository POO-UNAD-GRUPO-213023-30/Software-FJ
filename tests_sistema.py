"""
tests_sistema.py
=================
Pruebas unitarias para verificar el correcto funcionamiento del
Sistema de Gestión de Software FJ. Usa el módulo estándar `unittest`
(no requiere dependencias externas).

Ejecución:
    python3 -m unittest tests_sistema.py -v
"""

import unittest

from cliente import Cliente
from excepciones import (
    ClienteInvalidoError,
    CostoInvalidoError,
    DuracionInvalidaError,
    ReservaError,
    ServicioNoDisponibleError,
)
from reserva import EstadoReserva, Reserva
from servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from utilidades import GestorFJ


class TestCliente(unittest.TestCase):
    """Pruebas de validación y encapsulamiento de la clase Cliente."""

    def test_cliente_valido_se_crea_correctamente(self) -> None:
        cliente = Cliente(1, "Ana Torres", "123456", "ana@example.com", "3001234567")
        self.assertEqual(cliente.nombre, "Ana Torres")
        self.assertTrue(cliente.validar())

    def test_correo_invalido_lanza_excepcion(self) -> None:
        with self.assertRaises(ClienteInvalidoError):
            Cliente(1, "Ana Torres", "123456", "correo-malo", "3001234567")

    def test_documento_vacio_lanza_excepcion(self) -> None:
        with self.assertRaises(ClienteInvalidoError):
            Cliente(1, "Ana Torres", "", "ana@example.com", "3001234567")

    def test_telefono_invalido_lanza_excepcion(self) -> None:
        with self.assertRaises(ClienteInvalidoError):
            Cliente(1, "Ana Torres", "123456", "ana@example.com", "abc")


class TestServicios(unittest.TestCase):
    """Pruebas de las subclases de Servicio y su polimorfismo."""

    def test_reserva_sala_calcula_costo_con_recargo_ac(self) -> None:
        sala = ReservaSala("Sala A", 100000, capacidad=10, aire_acondicionado=True)
        self.assertAlmostEqual(sala.calcular_costo(), 115000.0)

    def test_reserva_sala_sin_ac_no_aplica_recargo(self) -> None:
        sala = ReservaSala("Sala B", 100000, capacidad=10, aire_acondicionado=False)
        self.assertAlmostEqual(sala.calcular_costo(), 100000.0)

    def test_alquiler_equipo_multiplica_por_cantidad(self) -> None:
        equipo = AlquilerEquipo("Proyector", 40000, tipo="Proyector", cantidad=3)
        self.assertAlmostEqual(equipo.calcular_costo(), 120000.0)

    def test_asesoria_multiplica_por_horas(self) -> None:
        asesoria = AsesoriaEspecializada("Consultoría", 50000, "TI", horas=4)
        self.assertAlmostEqual(asesoria.calcular_costo(), 200000.0)

    def test_capacidad_negativa_lanza_excepcion(self) -> None:
        with self.assertRaises(ServicioNoDisponibleError):
            ReservaSala("Sala C", 100000, capacidad=-1)

    def test_costo_base_negativo_lanza_excepcion(self) -> None:
        with self.assertRaises(CostoInvalidoError):
            AlquilerEquipo("Proyector", -100, tipo="Proyector", cantidad=1)

    def test_polimorfismo_descripcion_distinta_por_subclase(self) -> None:
        servicios = [
            ReservaSala("Sala D", 100000, capacidad=5),
            AlquilerEquipo("Laptop", 30000, tipo="Portátil", cantidad=1),
            AsesoriaEspecializada("Asesoría legal", 60000, "Legal", horas=2),
        ]
        descripciones = {s.descripcion() for s in servicios}
        # Cada subclase produce una descripción distinta: confirma que
        # se ejecutó el método sobrescrito correcto (dynamic dispatch).
        self.assertEqual(len(descripciones), 3)

    def test_impuesto_y_descuento_combinados(self) -> None:
        sala = ReservaSala("Sala E", 100000, capacidad=5, aire_acondicionado=False)
        costo = sala.calcular_costo(impuesto=0.19, descuento=0.10)
        # 100000 - 10% = 90000; 90000 + 19% = 107100
        self.assertAlmostEqual(costo, 107100.0)

    def test_descuento_fuera_de_rango_lanza_excepcion(self) -> None:
        sala = ReservaSala("Sala F", 100000, capacidad=5)
        with self.assertRaises(CostoInvalidoError):
            sala.calcular_costo(descuento=1.5)


class TestReserva(unittest.TestCase):
    """Pruebas del ciclo de vida de una reserva."""

    def setUp(self) -> None:
        self.cliente = Cliente(1, "Luis Gómez", "900123", "luis@example.com", "3009876543")
        self.servicio = ReservaSala("Sala G", 100000, capacidad=8)

    def test_ciclo_de_vida_exitoso(self) -> None:
        reserva = Reserva(1, self.cliente, self.servicio, duracion=2)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)
        reserva.confirmar()
        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)
        costo = reserva.procesar()
        self.assertEqual(reserva.estado, EstadoReserva.PROCESADA)
        self.assertAlmostEqual(costo, 100000.0)

    def test_duracion_negativa_lanza_excepcion(self) -> None:
        with self.assertRaises(DuracionInvalidaError):
            Reserva(1, self.cliente, self.servicio, duracion=-3)

    def test_no_se_puede_procesar_sin_confirmar(self) -> None:
        reserva = Reserva(1, self.cliente, self.servicio, duracion=2)
        with self.assertRaises(ReservaError):
            reserva.procesar()

    def test_no_se_puede_confirmar_dos_veces(self) -> None:
        reserva = Reserva(1, self.cliente, self.servicio, duracion=2)
        reserva.confirmar()
        with self.assertRaises(ReservaError):
            reserva.confirmar()

    def test_no_se_puede_cancelar_reserva_procesada(self) -> None:
        reserva = Reserva(1, self.cliente, self.servicio, duracion=2)
        reserva.confirmar()
        reserva.procesar()
        with self.assertRaises(ReservaError):
            reserva.cancelar()

    def test_tipo_cliente_incorrecto_lanza_excepcion(self) -> None:
        with self.assertRaises(ReservaError):
            Reserva(1, "no soy un cliente", self.servicio, duracion=2)


class TestGestorFJ(unittest.TestCase):
    """Pruebas de la fachada en memoria GestorFJ."""

    def setUp(self) -> None:
        self.gestor = GestorFJ()
        self.cliente = self.gestor.registrar_cliente(
            "Ana Torres", "123456", "ana@example.com", "3001234567"
        )
        self.servicio = ReservaSala("Sala H", 100000, capacidad=8)
        self.gestor.registrar_servicio(self.servicio)

    def test_registrar_cliente_lo_agrega_a_la_lista(self) -> None:
        self.assertEqual(len(self.gestor.clientes), 1)
        self.assertIs(self.gestor.buscar_cliente_por_documento("123456"), self.cliente)

    def test_reserva_duplicada_es_rechazada(self) -> None:
        self.gestor.crear_reserva(self.cliente, self.servicio, duracion=2)
        with self.assertRaises(ReservaError):
            self.gestor.crear_reserva(self.cliente, self.servicio, duracion=1)

    def test_reserva_permitida_tras_cancelar_la_anterior(self) -> None:
        primera = self.gestor.crear_reserva(self.cliente, self.servicio, duracion=2)
        primera.cancelar()
        # Al estar cancelada, ya no cuenta como reserva activa duplicada.
        segunda = self.gestor.crear_reserva(self.cliente, self.servicio, duracion=1)
        self.assertIsInstance(segunda, Reserva)


if __name__ == "__main__":
    unittest.main(verbosity=2)

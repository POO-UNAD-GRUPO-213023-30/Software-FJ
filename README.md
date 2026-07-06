# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Proyecto académico para el curso **Programación (213023)** — UNAD.
Implementa un sistema orientado a objetos, **sin bases de datos**, para
gestionar clientes, servicios y reservas de la empresa ficticia
**Software FJ**.

---

## 1. Descripción

Software FJ ofrece tres tipos de servicios: reserva de salas, alquiler
de equipos y asesorías especializadas. Este sistema permite:

- Registrar clientes con validaciones estrictas de documento, correo y teléfono.
- Crear servicios de los tres tipos mencionados, cada uno con su propia lógica de costos.
- Crear, confirmar, cancelar y procesar reservas que vinculan un cliente con un servicio.
- Registrar **todos los eventos y errores** en un archivo de logs (`logs/sistema.log`).
- Mantener la aplicación **siempre activa y estable**, incluso cuando ocurren errores graves.

Toda la información vive en **memoria** (listas de objetos Python). Los
únicos archivos que el sistema escribe en disco son los de registro
(logs), tal como exige la guía de la actividad.

---

## 2. Requisitos

- Python 3.9 o superior (no requiere librerías externas).
- Sistema operativo: Windows, Linux o macOS.

---

## 3. Instalación

```bash
# 1. Clonar o copiar la carpeta del proyecto
cd SistemaGestion

# 2. (Opcional) crear un entorno virtual
python3 -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# No se requieren dependencias externas: el proyecto usa solo la
# biblioteca estándar de Python (abc, logging, enum, re, os).
```

---

## 4. Ejecución

```bash
python3 main.py
```

Esto ejecuta automáticamente una simulación de **13 operaciones**
(clientes válidos/inválidos, servicios válidos/inválidos, reservas
exitosas/fallidas, cancelaciones, encadenamiento de excepciones, etc.)
e imprime en consola el resultado de cada una. Al finalizar, se
imprime un resumen general y se puede consultar el detalle técnico
completo en `logs/sistema.log`.

---

## 5. Estructura del proyecto

```
SistemaGestion/
│
├── main.py            # Punto de entrada: simula 13 operaciones del negocio
├── entidades.py        # Clase abstracta Entidad (base de Cliente)
├── cliente.py          # Clase Cliente (hereda de Entidad)
├── servicio.py          # Clase abstracta Servicio + 3 subclases especializadas
├── reserva.py          # Clase Reserva (compone Cliente + Servicio)
├── excepciones.py      # Jerarquía de excepciones personalizadas
├── logger.py           # Configuración centralizada de logging
├── utilidades.py        # GestorFJ: fachada en memoria + generador de IDs
├── logs/
│      sistema.log      # Archivo de logs generado en tiempo de ejecución
└── README.md
```

### Diagrama de dependencias (simplificado)

```
excepciones.py  <---- (importado por todos los módulos de dominio)
logger.py       <---- (importado por todos los módulos que registran eventos)
entidades.py  --->  cliente.py
servicio.py  (independiente, jerarquía propia)
cliente.py + servicio.py  --->  reserva.py
cliente.py + servicio.py + reserva.py  --->  utilidades.py (GestorFJ)
utilidades.py + servicio.py + excepciones.py  --->  main.py
```

---

## 6. Conceptos de POO utilizados

| Concepto | Dónde se aplica |
|---|---|
| **Abstracción** | `Entidad` (entidades.py) y `Servicio` (servicio.py) son clases abstractas (`ABC`) con métodos `@abstractmethod`. |
| **Herencia** | `Cliente` hereda de `Entidad`. `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de `Servicio`. |
| **Polimorfismo** | `Reserva.procesar()` llama a `servicio.calcular_costo()` sin saber cuál subclase concreta recibe; cada una calcula el costo de forma distinta. |
| **Encapsulamiento** | Todos los atributos sensibles usan `@property` / `@x.setter` con validación (`cliente.py`, `servicio.py`, `reserva.py`). |
| **Sobrescritura de métodos** | `calcular_costo()` y `descripcion()` se sobrescriben en cada subclase de `Servicio`. |
| **Sobrecarga (simulada)** | `calcular_costo(impuesto=None, descuento=None)` admite distintas combinaciones de parámetros opcionales, simulando múltiples variantes del cálculo. |
| **Excepciones personalizadas** | `ClienteInvalidoError`, `ServicioNoDisponibleError`, `ReservaError`, `DuracionInvalidaError`, `CostoInvalidoError` (excepciones.py). |
| **Encadenamiento de excepciones** | `raise ... from ...` en `reserva.py` (operación de procesar con costo inválido) y en `main.py` (operación 11). |
| **try/except/else/finally** | Presentes en cada una de las 13 operaciones de `main.py`. |
| **Logging avanzado** | `logger.py` registra niveles `INFO`, `WARNING`, `ERROR` y `CRITICAL` en `logs/sistema.log`. |

---

## 7. Ejemplos de uso (extracto de la simulación)

```python
from utilidades import GestorFJ
from servicio import ReservaSala

gestor = GestorFJ()

cliente = gestor.registrar_cliente(
    nombre="Ana Torres",
    documento="1020304050",
    correo="ana.torres@example.com",
    telefono="+573001234567",
)

sala = ReservaSala(
    nombre="Sala de Juntas Principal",
    costo_base=150000,
    capacidad=12,
    aire_acondicionado=True,
)
gestor.registrar_servicio(sala)

reserva = gestor.crear_reserva(cliente, sala, duracion=3)
reserva.confirmar()
costo = reserva.procesar(impuesto=0.19, descuento=0.05)
print(f"Costo final: ${costo:,.2f}")
```

---

## 8. Salida esperada (resumen)

```
SISTEMA DE GESTIÓN SOFTWARE FJ — INICIO DE SIMULACIÓN

[Operación 01] Registrar cliente válido (Ana Torres)
  OK: Cliente #1 | Ana Torres | Doc: 1020304050 | ...
  -> Operación 1 finalizada.

[Operación 02] Registrar cliente inválido (correo mal formado)
  ERROR controlado: Correo electrónico inválido: 'carlos_correo_invalido'
  -> Operación 2 finalizada. El sistema sigue activo.

...

============================================================
RESUMEN DEL SISTEMA - SOFTWARE FJ
============================================================
Clientes registrados: 2
Servicios en catálogo: 3
Reservas creadas: 3
------------------------------------------------------------
Reserva #1 | Estado: PROCESADA | Cliente: Ana Torres | ...
============================================================

Simulación finalizada. Revise 'logs/sistema.log' para el detalle completo.
```

El archivo `logs/sistema.log` contendrá el detalle técnico completo de
cada evento, con marca de tiempo, nivel y módulo de origen, por ejemplo:

```
2026-07-06 22:10:18 | INFO     | SistemaFJ.__main__  | Iniciando operación 01: ...
2026-07-06 22:10:18 | WARNING  | SistemaFJ.__main__  | Registro de cliente rechazado: ...
2026-07-06 22:10:18 | ERROR    | SistemaFJ.__main__  | Costo inválido detectado: ...
```

---

## 9. Notas de diseño

- **Sin bases de datos:** toda la persistencia ocurre en las listas
  `clientes`, `servicios` y `reservas` de la clase `GestorFJ`
  (utilidades.py), que viven únicamente en memoria durante la
  ejecución del programa.
- **Estabilidad garantizada:** cada una de las 13 operaciones de
  `main.py` está aislada en su propio bloque `try/except/else/finally`,
  y además existe una salvaguarda global (`try/except Exception`) que
  captura cualquier error no previsto como `CRITICAL` sin dejar que el
  programa termine con un traceback crudo.
- **Extensibilidad:** agregar un nuevo tipo de servicio solo requiere
  crear una nueva subclase de `Servicio` e implementar
  `calcular_costo()` y `descripcion()` — no se modifica ningún otro
  módulo (principio abierto/cerrado).

---

## 10. Autoría

Proyecto desarrollado como actividad grupal (Anexo 3 — Fase 4) para el
curso de Programación, Ingeniería de Sistemas, ECBTI — UNAD.

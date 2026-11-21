# Sistema de gestión de servicios — Software FJ

**Fase 4: Componente práctico (Prácticas simuladas)**
**Curso:** Programación (213023)
**Grupo:** 213023_617
**Universidad Nacional Abierta y a Distancia (UNAD)**

## Integrantes

| Nombre | Código | Aporte principal | Usuario de GitHub |
|---|---|---|---|
| Luis Ernesto Bocanegra Valcero | 1121822429 | 1. Clase `Cliente` (validación y encapsulación).<br>2. Jerarquía de `Servicio` (clase abstracta + 3 servicios derivados con polimorfismo y sobrecarga).<br>3. Redacción de conclusiones y referencias del PDF. | @netico86 |
| Yeiber Bryan Cruz Cruz | 1121875462 | 1. Módulo `excepciones.py` (personalizadas).<br>2. Clase `Reserva` (lógica con try/except/else/finally y encadenamiento).<br>3. Configuración de logging y `main.py` con las simulaciones.<br>4. Redacción de la introducción y armado del PDF final. | @Imbryacruz |

> **Nota:** el equipo trabajó con dos integrantes, por acuerdo con el tutor del curso, ya que no se reportaron más estudiantes al grupo.

## Descripción

Este proyecto implementa un sistema para Software FJ que permite gestionar clientes, servicios y reservas. Incluye tres tipos de servicio: reserva de salas, alquiler de equipos y asesorías especializadas.

La aplicación está desarrollada en Python, sin bases de datos: toda la información se maneja con objetos y listas internas, y solo se usan archivos para el registro de eventos y errores (`logs/sistema.log`). El diseño aplica programación orientada a objetos y manejo avanzado de excepciones.

## Objetivos

**Objetivo general:** desarrollar una aplicación orientada a objetos para gestionar clientes, servicios y reservas de Software FJ, con una estructura modular y manejo robusto de errores.

**Objetivos específicos:**

- Organizar el código en módulos para facilitar su lectura y mantenimiento.
- Aplicar abstracción, encapsulación, herencia y polimorfismo.
- Implementar excepciones personalizadas y estructuras de manejo de errores.
- Simular al menos diez operaciones válidas e inválidas del sistema.

## Características

- **Abstracción:** clases abstractas `EntidadAbstracta` y `Servicio`.
- **Encapsulación:** atributos privados con `@property` y setters que validan los datos.
- **Herencia y polimorfismo:** `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` sobrescriben `calcular_costo()`, `describir()` y `obtener_detalle()`.
- **Sobrecarga de métodos:** `calcular_costo(unidades, descuento=0.0, impuesto=0.0)` con parámetros opcionales y `aplicar_ajuste_extra()` con `@singledispatchmethod` (según el tipo: `int` = porcentaje, `float` = fracción, `str` = nota).
- **Listas internas:** `GestorSoftwareFJ` administra las listas de clientes, servicios y reservas.
- **Excepciones:** jerarquía propia (`SoftwareFJError` y derivadas), bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- **Logs:** eventos y errores en `logs/sistema.log`; la aplicación continúa ante cualquier fallo.

## Requisitos

- Python 3.10 o superior.
- No requiere dependencias externas (solo biblioteca estándar).

## Estructura del proyecto

```text
fase4-componente-practico-grupo--213023_617-/
├── README.md
├── main.py                  # Punto de entrada: 18 simulaciones (válidas e inválidas)
├── src/
│   ├── __init__.py
│   ├── excepciones.py       # Excepciones personalizadas
│   ├── cliente.py     # EntidadAbstracta y Cliente (validaciones)
│   ├── servicios.py    # Servicio (abstracta) y 3 servicios derivados
│   ├── reservas.py     # Reserva: confirmar, cancelar y procesar
│   ├── gestor.py            # GestorSoftwareFJ: listas de clientes, servicios y reservas
│   └── logger.py            # Configuración de logging
└── logs/
    └── sistema.log          # Registro generado durante la ejecución
```

## Instalación y ejecución

Clona el repositorio y entra en la carpeta creada:

```bash
git clone https://github.com/netico86/fase4-componente-practico-grupo--213023_617-.git
cd fase4-componente-practico-grupo--213023_617-
```

Ejecuta el programa **desde la carpeta raíz** (donde está `main.py`):

```bash
python main.py
```

Si tu sistema usa el comando `python3`:

```bash
python3 main.py
```

La carpeta `logs/` se crea automáticamente y los registros se guardan en `logs/sistema.log` (el archivo se genera en cada ejecución y no se versiona en Git).

## Simulaciones incluidas

| # | Escenario | Resultado esperado |
|---|---|---|
| 1 | Registro de cliente válido | Éxito |
| 2 | Cliente con correo mal formado | Error controlado |
| 3 | Cliente menor de edad | Error controlado |
| 4 | Creación de tres servicios válidos | Éxito |
| 5 | Reserva completa: crear → confirmar → procesar | Éxito |
| 6 | Procesar una reserva sin confirmar | Error con encadenamiento |
| 7 | Cancelar una reserva pendiente | Éxito |
| 8 | Cancelar una reserva ya procesada | Error controlado |
| 9 | Confirmar una reserva ya procesada | Error controlado |
| 10 | Reservar un servicio no disponible | Error controlado |
| 11 | Duración de reserva inválida | Error controlado |
| 12 | Reserva sin cliente | Error controlado |
| 13 | Sobrecarga de `aplicar_ajuste_extra` (int, float, str) | Éxito |
| 14 | Descuento fuera de rango | Error controlado |
| 15 | Modalidad de asesoría inválida | Error controlado |
| 16 | Costos con descuento e IVA | Éxito |
| 17 | Cliente con correo ya registrado | Error controlado |
| 18 | Reserva con fecha en el pasado | Error controlado |

## Flujo de trabajo colaborativo

Cada integrante trabaja en una rama relacionada con su tarea, por ejemplo:

- `feature/clientes`
- `feature/servicios`
- `feature/reservas`
- `feature/excepciones`
- `feature/documentacion`

Al terminar un cambio:

1. Confirmar los cambios con un mensaje descriptivo.
2. Publicar la rama en GitHub.
3. Crear un Pull Request hacia la rama principal.
4. Revisar los cambios antes de aprobar y fusionar el Pull Request.

### Convención de commits

- `feat:` nueva funcionalidad.
- `fix:` corrección de errores.
- `docs:` cambios en la documentación.
- `test:` incorporación o ajuste de pruebas y simulaciones.
- `refactor:` reorganización del código sin cambiar su comportamiento.

## Referencias

- Van Rossum, G., & Drake Jr, F. L. (2024). *El tutorial de Python*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
- Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.
- Zambrano, J. P. (2025). *Introducción al uso de GitHub* [Objeto virtual de información]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75876
- Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress.

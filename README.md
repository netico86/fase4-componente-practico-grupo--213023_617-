# Sistema de gestión de servicios — Software FJ

**Fase 4: Componente práctico**  
**Curso:** Programación  
**Grupo:** 213023_617  
**Universidad Nacional Abierta y a Distancia (UNAD)**

## Integrantes

| Nombre | Código | Aporte principal | Usuario de GitHub |
|---|---|---|---|
| Luis Ernesto Bocanegra Valcero | 1121822429 | Líder del repositorio y desarrollo del problema 1 | [@netico86](https://github.com/netico86) |
| Yeiber Bryan Cruz Cruz | [Tu Código UNAD] | Validación estricta, encapsulación y excepciones de seguridad | [@Imbryacruz](https://github.com/Imbryacruz) |
| [Nombre del integrante 3] | [Código] | Desarrollo del problema 3 | [@usuario3](https://github.com/usuario3) |
| [Nombre del integrante 4] | [Código] | Desarrollo del problema 4 | [@usuario4](https://github.com/usuario4) |
| [Nombre del integrante 5] | [Código] | Desarrollo del problema 5 | [@usuario5](https://github.com/usuario5) |


## Descripción

Este proyecto implementa un sistema para **Software FJ** que permite gestionar clientes, servicios y reservas. Incluye servicios como la reserva de salas, el alquiler de equipos y las asesorías especializadas.

La aplicación está desarrollada en Python y organizada en módulos. El diseño aplica conceptos de programación orientada a objetos y manejo de excepciones. También registra eventos y errores mediante el módulo `logging`.

## Objetivos

### Objetivo general

Desarrollar una aplicación orientada a objetos para gestionar clientes, servicios y reservas de Software FJ, con una estructura modular y manejo de errores.

### Objetivos específicos

- Organizar el código en módulos para facilitar su lectura y mantenimiento.
- Aplicar abstracción, encapsulación, herencia y polimorfismo.
- Implementar excepciones personalizadas y estructuras de manejo de errores.
- Simular al menos diez operaciones válidas e inválidas del sistema.

## Características

- Gestión de clientes con validaciones.
- Definición de servicios mediante una clase abstracta y clases derivadas.
- Gestión de reservas.
- Manejo de excepciones personalizadas.
- Registro de eventos y errores en un archivo de log.

## Requisitos

- Python 3.10 o superior.
- No requiere instalar dependencias externas; utiliza módulos de la biblioteca estándar de Python.

## Estructura del proyecto

```text
software-fj-sistema/
├── README.md
├── main.py                  # Punto de entrada y simulaciones del sistema
├── src/
│   ├── __init__.py
│   ├── excepciones.py       # Excepciones personalizadas
│   ├── cliente.py           # Clase Cliente y validaciones
│   ├── servicios.py         # Clase abstracta Servicio y clases derivadas
│   └── reservas.py          # Clases y lógica para gestionar reservas
├── logs/
│   └── software_fj_logs.log # Registro generado durante la ejecución
└── docs/
    └── guia_uso.md          # Documentación adicional
```

## Instalación y ejecución

Clona el repositorio y entra en la carpeta creada:

```bash
git clone https://github.com/netico86/fase4-componente-practico-grupo-213023_617.git
cd fase4-componente-practico-grupo-213023_617
```

Ejecuta el programa:

```bash
python main.py
```

Si tu sistema usa el comando `python3`, puedes ejecutar:

```bash
python3 main.py
```

Los registros de ejecución se guardan en `logs/software_fj_logs.log`, de acuerdo con la configuración del programa.

## Flujo de trabajo colaborativo

Para organizar los aportes, cada integrante puede trabajar en una rama relacionada con su tarea. Por ejemplo:

```text
feature/clientes
feature/servicios
feature/reservas
feature/excepciones
feature/documentacion
```

Al terminar un cambio, se recomienda:

1. Confirmar los cambios con un mensaje descriptivo.
2. Publicar la rama en GitHub.
3. Crear un *Pull Request* hacia la rama principal.
4. Revisar los cambios antes de aprobar y fusionar el *Pull Request*.

### Convención de commits

- `feat:` nueva funcionalidad.
- `fix:` corrección de errores.
- `docs:` cambios en la documentación.
- `test:` incorporación o ajuste de pruebas y simulaciones.
- `refactor:` reorganización del código sin cambiar su comportamiento.

## Referencias

- Python Software Foundation. [El tutorial de Python: errores y excepciones](https://docs.python.org/es/3.12/tutorial/errors.html).
- Cuevas Álvarez, A. (2016). *Python 3: Curso práctico*. RA-MA Editorial.
- Reitz, K. (2023). [The Hitchhiker’s Guide to Python](https://docs.python-guide.org/).
- Chacon, S., y Straub, B. (2014). [*Pro Git* (2.ª ed.)](https://git-scm.com/book/es/v2).
- Zambrano, J. P. (2025). [Introducción al uso de GitHub [OVI]](https://repository.unad.edu.co/handle/10596/75876). Repositorio Institucional UNAD.





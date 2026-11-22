"""
Sistema Integral de Gestión — Software FJ
Módulo: logger

Configura el registro centralizado de eventos y errores en `logs/sistema.log`.
La carpeta `logs/` se crea automáticamente junto a `main.py`, sin importar
desde qué directorio se ejecute el programa.
"""
import logging
import os

# Carpeta logs/ en la raíz del proyecto (un nivel arriba de src/)
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_LOGS = os.path.join(RAIZ_PROYECTO, "logs")
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "sistema.log")

os.makedirs(CARPETA_LOGS, exist_ok=True)  # Crea logs/ si no existe

# Configuración del sistema de logging para trazabilidad
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    encoding="utf-8",
)


def registrar_evento(mensaje: str):
    """Registra un evento normal o una transacción exitosa del sistema."""
    logging.info(mensaje)


def registrar_error(error: Exception):
    """Registra una excepción capturada (con su traza y causa encadenada).

    Cada excepción se registra una sola vez aunque pase por varias capas
    (por ejemplo, Reserva y luego el programa principal).
    """
    if getattr(error, "_registrada", False):
        return
    try:
        error._registrada = True  # Marca para evitar duplicados en el log
    except AttributeError:
        pass  # Algunas excepciones integradas no admiten atributos nuevos
    logging.error(f"{type(error).__name__}: {error}", exc_info=error)

import logging
import os

# Crear la carpeta logs si no existe de forma automática
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar el sistema de logging centralizado para seguridad y trazabilidad
logging.basicConfig(
    filename='logs/sistema.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)

def registrar_evento(mensaje: str):
    """Registra un evento normal o transacción exitosa del sistema."""
    logging.info(mensaje)

def registrar_error(error: Exception):
    """Registra una excepción o error crítico capturado por seguridad."""
    logging.error(f"{type(error).__name__}: {str(error)}", exc_info=True)
    
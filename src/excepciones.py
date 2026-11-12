## Software Sistema Integral de Gestión de Clientes, Servicios y  Reservas

# src/excepciones.py

## Manejo de excepciones 
class SoftwareFJError(Exception):
    """Clase base para excepciones en el software FJ."""
    def __init__(self, mensaje = "Ocurrió un error en el software FJ."):
        self.mensaje = mensaje
        super().__init__(mensaje)
    def __str__(self):
        return f"SoftwareFJError: {self.mensaje}"   
    
## Excepción para datos inválidos

class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando se detecta un dato inválido en el sistema."""
def __init__(self, campo):
    mensaje = f"El dato proporcionado para el campo '{campo}' es inválido."
    super().__init__(mensaje)

## Excepción para datos faltantes
class DatoFaltanteError(SoftwareFJError):
    """Se lanza cuando se detecta un dato faltante en el sistema."""
    def __init__(self, campo):
        mensaje = f"El parámetro '{campo}' no fue proporcionado."
        super().__init__(mensaje)

## Para operaciones no permitidas   
class OperacionNoPermitidaError(SoftwareFJError): 
    """Se lanza cuando se intenta realizar una operación no permitida en el sistema."""
def __init__(self, operacion):
    mensaje = f"La operación '{operacion}' no está permitida en el sistema."
    super().__init__(mensaje)
    

## Para intentos de reserva incorrectos
class ReservaIncorrectaError(SoftwareFJError):
    """Se lanza cuando se detecta un intento de reserva incorrecto en el sistema."""
    def __init__(self, reserva):
        mensaje = f"El intento de reserva '{reserva}' es incorrecto."
        super().__init__(mensaje)

## Para servicios no disponibles
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta acceder a un servicio que no está activo o disponible en el sistema."""
    def __init__(self, servicio):
        mensaje = f"El servicio '{servicio}' no está disponible."
        super().__init__(mensaje)

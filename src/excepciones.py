"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ
Módulo: excepciones

Define la jerarquía de excepciones personalizadas del sistema. Todas heredan
de `SoftwareFJError`, de modo que el programa pueda capturar cualquier error
propio del dominio con un único `except SoftwareFJError`.
"""


class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del software FJ."""

    def __init__(self, mensaje="Ocurrió un error en el software FJ."):
        self.mensaje = mensaje          # Texto legible del error
        super().__init__(mensaje)       # Inicializa Exception con el mensaje

    def __str__(self):
        # Solo el mensaje: el logger ya antepone el nombre de la clase.
        return self.mensaje


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando se detecta un dato inválido en el sistema."""

    def __init__(self, campo, valor=None):
        self.campo = campo              # Nombre del campo con problema
        self.valor = valor              # Valor rechazado (para trazabilidad)
        mensaje = f"El dato proporcionado para el campo '{campo}' es inválido"
        if valor is not None:
            mensaje += f" (valor recibido: {valor!r})"
        super().__init__(mensaje + ".")


class DatoFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un dato o parámetro obligatorio."""

    def __init__(self, campo):
        self.campo = campo
        super().__init__(f"El parámetro '{campo}' no fue proporcionado.")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación no permitida en el estado actual."""

    def __init__(self, operacion):
        self.operacion = operacion
        super().__init__(
            f"La operación '{operacion}' no está permitida en el sistema."
        )


class ReservaIncorrectaError(SoftwareFJError):
    """Se lanza cuando se detecta un intento de reserva incorrecto."""

    def __init__(self, reserva):
        self.reserva = reserva
        super().__init__(f"El intento de reserva es incorrecto: {reserva}")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""

    def __init__(self, servicio):
        self.servicio = servicio
        super().__init__(f"El servicio '{servicio}' no está disponible.")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando hay un error en los cálculos de costos o tiempos."""

    def __init__(self, motivo):
        self.motivo = motivo
        super().__init__(f"Error de cálculo inconsistente: {motivo}")

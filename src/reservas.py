"""
Sistema de Gestión de Reservas — Software FJ
Módulo: Reservas
Descripción:
- Clase Reserva que integra Cliente, Servicio, duración y estado.
- Implementa confirmación, cancelación y procesamiento con manejo
  avanzado de excepciones (try/except/else/finally).
- Encadenamiento de excepciones para trazabilidad completa.
"""
from datetime import datetime
from src.cliente import Cliente
from src.servicios import Servicio
from src.excepciones import (
    DatoInvalidoError,
    ReservaIncorrectaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    DatoFaltanteError,
)
from src.logger import registrar_evento, registrar_error


class Reserva:
    """Clase que representa una reserva de un servicio por parte de un cliente."""

    _contador_id = 0

    def __init__(self, cliente, servicio, fecha_inicio, duracion):
        """Inicializa una nueva reserva con validaciones estrictas."""
        # Parámetros faltantes
        if cliente is None:
            raise DatoFaltanteError("cliente")
        if servicio is None:
            raise DatoFaltanteError("servicio")
        if fecha_inicio is None:
            raise DatoFaltanteError("fecha_inicio")
        if duracion is None:
            raise DatoFaltanteError("duracion")

        # Parámetros con tipo o valor inválido
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("cliente", cliente)
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("servicio", servicio)
        if not isinstance(fecha_inicio, datetime):
            raise DatoInvalidoError("fecha_inicio", fecha_inicio)
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, int)
            or duracion <= 0
        ):
            raise DatoInvalidoError("duracion", duracion)
        if fecha_inicio < datetime.now():
            raise ReservaIncorrectaError(
                f"la fecha de inicio ({fecha_inicio:%Y-%m-%d %H:%M}) ya pasó"
            )

        Reserva._contador_id += 1
        self._id_reserva = Reserva._contador_id
        self._cliente = cliente
        self._servicio = servicio
        self._fecha_inicio = fecha_inicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._costo_total = 0.0
        self._fecha_creacion = datetime.now()

        registrar_evento(f"Reserva #{self._id_reserva} creada para {cliente.nombre}.")

    # =========================== GETTERS ===========================
    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    @property
    def duracion(self):
        return self._duracion

    # =========================== MÉTODOS DE ESTADO ===========================

    def confirmar(self):
        """Confirma la reserva si está en estado Pendiente y el servicio está disponible."""
        try:
            if self._estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    f"confirmar (estado actual: {self._estado})"
                )
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(self._servicio.nombre)

            self._estado = "Confirmada"
            registrar_evento(f"Reserva #{self._id_reserva} confirmada.")
        except Exception as e:
            registrar_error(e)
            raise

    def cancelar(self):
        """Cancela la reserva si no ha sido procesada."""
        try:
            if self._estado == "Procesada":
                raise OperacionNoPermitidaError(
                    "cancelar (la reserva ya fue procesada)"
                )
            if self._estado == "Cancelada":
                raise OperacionNoPermitidaError(
                    "cancelar (la reserva ya estaba cancelada)"
                )

            self._estado = "Cancelada"
            registrar_evento(f"Reserva #{self._id_reserva} cancelada.")
        except Exception as e:
            registrar_error(e)
            raise

    def procesar(self):
        """
        Procesa la reserva calculando el costo final.
        Implementa try/except/else/finally y encadenamiento de excepciones.
        """
        resultado = None
        try:
            registrar_evento(
                f"Iniciando procesamiento de Reserva #{self._id_reserva}..."
            )

            # Validación de estado previo
            if self._estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    "procesar (la reserva debe estar Confirmada primero)"
                )

            # Cálculo del costo (puede lanzar CalculoInconsistenteError)
            self._costo_total = self._servicio.calcular_costo(self._duracion)

        except OperacionNoPermitidaError as e:
            # Encadenamiento de excepciones (requisito Nivel Alto)
            error_causa = ReservaIncorrectaError(
                f"No se pudo procesar la reserva #{self._id_reserva}"
            )
            error_causa.__cause__ = e  # Enlaza la causa para que el log muestre la cadena
            registrar_error(error_causa)
            raise error_causa from e

        except CalculoInconsistenteError as e:
            error_causa = ReservaIncorrectaError(
                f"Cálculo fallido en reserva #{self._id_reserva}"
            )
            error_causa.__cause__ = e  # Enlaza la causa para que el log muestre la cadena
            registrar_error(error_causa)
            raise error_causa from e

        except Exception as e:
            registrar_error(e)
            raise ReservaIncorrectaError(
                f"Error inesperado procesando reserva #{self._id_reserva}"
            ) from e

        else:
            # Se ejecuta SOLO si no hubo excepciones
            self._estado = "Procesada"
            resultado = (
                f"Reserva #{self._id_reserva} procesada exitosamente. "
                f"Costo total: ${self._costo_total:,.2f}"
            )
            registrar_evento(resultado)

        finally:
            # Se ejecuta SIEMPRE, independientemente del resultado
            registrar_evento(
                f"Finalizó procesamiento de Reserva #{self._id_reserva}. "
                f"Estado final: {self._estado}"
            )

        return resultado

    # =========================== REPRESENTACIÓN ===========================

    def obtener_info(self):
        """Retorna un diccionario con la información de la reserva."""
        return {
            "id_reserva": self._id_reserva,
            "cliente": self._cliente.obtener_info(),
            "servicio": self._servicio.obtener_detalle(),
            "fecha_inicio": self._fecha_inicio.strftime("%Y-%m-%d %H:%M")
            if isinstance(self._fecha_inicio, datetime)
            else str(self._fecha_inicio),
            "duracion": self._duracion,
            "estado": self._estado,
            "costo_total": self._costo_total,
            "fecha_creacion": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self):
        return (
            f"Reserva #{self._id_reserva} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Estado: {self._estado} | "
            f"Costo: ${self._costo_total:,.2f}"
        )
"""
Sistema Integral de Gestión — Software FJ
Módulo: Gestor

`GestorSoftwareFJ` administra las colecciones internas (listas) de clientes,
servicios y reservas. No usa base de datos: todo vive en memoria y solo los
eventos y errores se escriben en el archivo de logs.
"""
from src.cliente import Cliente
from src.reservas import Reserva
from src.servicios import Servicio
from src.excepciones import (
    DatoInvalidoError,
    OperacionNoPermitidaError,
    SoftwareFJError,
)
from src.logger import registrar_error, registrar_evento


class GestorSoftwareFJ:
    """Administra las listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    # =========================== CLIENTES ===========================

    def registrar_cliente(self, **datos) -> Cliente:
        """Crea un cliente validado y lo agrega a la lista.

        Lanza SoftwareFJError si los datos son inválidos o si el correo ya
        está registrado. Los errores se registran en el log antes de propagarse.
        """
        try:
            cliente = Cliente(**datos)  # Los setters validan cada dato
            if self.buscar_cliente_por_email(cliente.email) is not None:
                raise OperacionNoPermitidaError(
                    f"registrar cliente (el correo {cliente.email} ya existe)"
                )
        except TypeError as e:
            # Parámetros obligatorios ausentes o desconocidos en la llamada
            error = DatoInvalidoError("datos_cliente", str(e))
            registrar_error(error)
            raise error from e
        except SoftwareFJError as e:
            registrar_error(e)
            raise
        else:
            # Solo se agrega si no hubo ninguna excepción
            self._clientes.append(cliente)
            registrar_evento(f"Cliente registrado: {cliente}")
            return cliente

    def buscar_cliente_por_email(self, email: str):
        """Retorna el cliente con ese correo o None si no existe."""
        for cliente in self._clientes:
            if cliente.email.lower() == str(email).strip().lower():
                return cliente
        return None

    # =========================== SERVICIOS ===========================

    def agregar_servicio(self, servicio: Servicio) -> Servicio:
        """Agrega un servicio ya construido a la lista de servicios."""
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("servicio", servicio)
            if servicio in self._servicios:
                raise OperacionNoPermitidaError(
                    f"agregar servicio (el servicio {servicio.codigo} ya existe)"
                )
        except SoftwareFJError as e:
            registrar_error(e)
            raise
        else:
            self._servicios.append(servicio)
            registrar_evento(f"Servicio agregado: {servicio}")
            return servicio

    # =========================== RESERVAS ===========================

    def crear_reserva(self, cliente, servicio, fecha_inicio, duracion) -> Reserva:
        """Crea una reserva validada y la agrega a la lista de reservas."""
        try:
            reserva = Reserva(cliente, servicio, fecha_inicio, duracion)
        except SoftwareFJError as e:
            registrar_error(e)
            raise
        else:
            self._reservas.append(reserva)
            return reserva

    # =========================== CONSULTAS ===========================

    @property
    def clientes(self) -> list:
        return list(self._clientes)  # Copia: la lista interna queda encapsulada

    @property
    def servicios(self) -> list:
        return list(self._servicios)

    @property
    def reservas(self) -> list:
        return list(self._reservas)

    def reservas_por_estado(self, estado: str) -> list:
        """Filtra las reservas por estado (Pendiente, Confirmada, Procesada, Cancelada)."""
        return [r for r in self._reservas if r.estado == estado]

    def resumen(self) -> str:
        """Retorna un resumen en texto del contenido de las listas internas."""
        estados = ("Pendiente", "Confirmada", "Procesada", "Cancelada")
        por_estado = ", ".join(
            f"{e}: {len(self.reservas_por_estado(e))}" for e in estados
        )
        lineas = [
            f"Clientes registrados: {len(self._clientes)}",
            *(f"   - {c}" for c in self._clientes),
            f"Servicios disponibles en catálogo: {len(self._servicios)}",
            *(f"   - {s}" for s in self._servicios),
            f"Reservas: {len(self._reservas)} ({por_estado})",
            *(f"   - {r}" for r in self._reservas),
        ]
        return "\n".join(lineas)

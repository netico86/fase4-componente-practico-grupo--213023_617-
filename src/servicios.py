"""
===============================================================================
Sistema de Gestión de Servicios — Software FJ
Módulo: Servicios
Descripción:
    - Define la clase abstracta base `Servicio` con atributos encapsulados y
      validaciones mediante propiedades (@property / setters).
    - Implementa tres clases derivadas: `ReservaSala`, `AlquilerEquipo` y
      `AsesoriaEspecializada`, demostrando herencia, polimorfismo y sobrecarga
      de métodos (`@singledispatchmethod`) para ajustes y cálculos.
===============================================================================
"""

from abc import ABC, abstractmethod
from functools import singledispatchmethod
import unicodedata
from src.excepciones import DatoInvalidoError, DatoFaltanteError


def _normalizar_texto(texto: str) -> str:
    """Convierte a minúsculas y elimina tildes para comparaciones seguras."""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto.strip().lower())
        if unicodedata.category(c) != "Mn"
    )
    return sin_tildes


class Servicio(ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    _contador_codigo = 0

    def __init__(self, nombre: str, tarifa_base: float, disponible: bool = True):
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible

        Servicio._contador_codigo += 1
        self._codigo = f"SRV-{Servicio._contador_codigo:03d}"

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("nombre_servicio")
        limpio = valor.strip()
        if len(limpio) < 3 or len(limpio) > 80:
            raise DatoInvalidoError("nombre_servicio", valor)
        self._nombre = limpio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        if valor is None:
            raise DatoFaltanteError("tarifa_base")
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise DatoInvalidoError("tarifa_base", valor)
        self._tarifa_base = float(valor)

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("disponible", valor)
        self._disponible = valor

    @abstractmethod
    def calcular_costo(self, unidades: int, descuento: float = 0.0) -> float:
        """Calcula el costo total del servicio según unidades y descuento (0.0 a 1.0)."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción legible y específica del servicio."""
        pass

    @abstractmethod
    def obtener_detalle(self) -> dict:
        """Retorna un diccionario con la información estructurada del servicio."""
        pass

    def _validar_unidades_y_descuento(self, unidades: int, descuento: float) -> float:
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades <= 0:
            raise DatoInvalidoError("unidades", unidades)
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not (0.0 <= descuento < 1.0):
            raise DatoInvalidoError("descuento", descuento)
        return float(descuento)

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"[{self._codigo}] {self._nombre} (${self._tarifa_base:,.2f}) - {estado}"


class ReservaSala(Servicio):
    """Servicio derivado para reserva de salas (tarifa base por hora)."""

    def __init__(
        self,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        requiere_proyector: bool = False,
        disponible: bool = True,
    ):
        super().__init__(nombre, tarifa_base, disponible)
        self.capacidad = capacidad
        self.requiere_proyector = requiere_proyector

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError("capacidad", valor)
        self._capacidad = valor

    @property
    def requiere_proyector(self) -> bool:
        return self._requiere_proyector

    @requiere_proyector.setter
    def requiere_proyector(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("requiere_proyector", valor)
        self._requiere_proyector = valor

    def calcular_costo(self, unidades: int, descuento: float = 0.0) -> float:
        """Calcula el costo por cantidad de horas; añade 15% si requiere proyector."""
        desc = self._validar_unidades_y_descuento(unidades, descuento)
        recargo_proyector = 1.15 if self._requiere_proyector else 1.0
        subtotal = self.tarifa_base * unidades * recargo_proyector
        return round(subtotal * (1 - desc), 2)

    @singledispatchmethod
    def aplicar_ajuste_extra(self, ajuste):
        """Sobrecarga de método: aplica recargo porcentual (int/float) o registra nota (str)."""
        raise DatoInvalidoError("ajuste", ajuste)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: int) -> float:
        if isinstance(ajuste, bool) or ajuste < 0:
            raise DatoInvalidoError("ajuste", ajuste)
        return round(self.tarifa_base * (1 + float(ajuste)), 2)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: float) -> float:
        if ajuste < 0:
            raise DatoInvalidoError("ajuste", ajuste)
        return round(self.tarifa_base * (1 + ajuste), 2)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: str) -> str:
        texto = ajuste.strip()
        if not texto:
            raise DatoFaltanteError("ajuste")
        return f"[{self.codigo}] {self.nombre} - Nota de sala: {texto}"

    def describir(self) -> str:
        proyector = "con proyector" if self._requiere_proyector else "sin proyector"
        return (
            f"{self.nombre} (Capacidad: {self._capacidad} personas, {proyector}) "
            f"- Tarifa base: ${self.tarifa_base:,.2f}/hora"
        )

    def obtener_detalle(self) -> dict:
        return {
            "codigo": self.codigo,
            "tipo": "ReservaSala",
            "nombre": self.nombre,
            "tarifa_base": self.tarifa_base,
            "capacidad": self._capacidad,
            "requiere_proyector": self._requiere_proyector,
            "disponible": self.disponible,
        }


class AlquilerEquipo(Servicio):
    """Servicio derivado para alquiler de equipos tecnológicos (tarifa base por día)."""

    def __init__(
        self,
        nombre: str,
        tarifa_base: float,
        categoria_equipo: str,
        seguro_incluido: bool = True,
        disponible: bool = True,
    ):
        super().__init__(nombre, tarifa_base, disponible)
        self.categoria_equipo = categoria_equipo
        self.seguro_incluido = seguro_incluido

    @property
    def categoria_equipo(self) -> str:
        return self._categoria_equipo

    @categoria_equipo.setter
    def categoria_equipo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("categoria_equipo")
        self._categoria_equipo = valor.strip()

    @property
    def seguro_incluido(self) -> bool:
        return self._seguro_incluido

    @seguro_incluido.setter
    def seguro_incluido(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("seguro_incluido", valor)
        self._seguro_incluido = valor

    def calcular_costo(self, unidades: int, descuento: float = 0.0) -> float:
        """Calcula el costo por días de alquiler; suma un 10% si incluye seguro."""
        desc = self._validar_unidades_y_descuento(unidades, descuento)
        factor_seguro = 1.10 if self._seguro_incluido else 1.0
        subtotal = self.tarifa_base * unidades * factor_seguro
        return round(subtotal * (1 - desc), 2)

    @singledispatchmethod
    def aplicar_ajuste_extra(self, ajuste):
        """Sobrecarga de método: aplica recargo porcentual (int/float) o asigna accesorio (str)."""
        raise DatoInvalidoError("ajuste", ajuste)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: int) -> float:
        if isinstance(ajuste, bool) or ajuste < 0:
            raise DatoInvalidoError("ajuste", ajuste)
        return round(self.tarifa_base * (1 + float(ajuste)), 2)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: float) -> float:
        if ajuste < 0:
            raise DatoInvalidoError("ajuste", ajuste)
        return round(self.tarifa_base * (1 + ajuste), 2)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: str) -> str:
        accesorio = ajuste.strip()
        if not accesorio:
            raise DatoFaltanteError("accesorio")
        return f"[{self.codigo}] {self.nombre} ({self._categoria_equipo}) - Accesorio incluido: {accesorio}"

    def describir(self) -> str:
        seguro = "con seguro" if self._seguro_incluido else "sin seguro"
        return (
            f"{self.nombre} (Categoría: {self._categoria_equipo}, {seguro}) "
            f"- Tarifa base: ${self.tarifa_base:,.2f}/día"
        )

    def obtener_detalle(self) -> dict:
        return {
            "codigo": self.codigo,
            "tipo": "AlquilerEquipo",
            "nombre": self.nombre,
            "tarifa_base": self.tarifa_base,
            "categoria_equipo": self._categoria_equipo,
            "seguro_incluido": self._seguro_incluido,
            "disponible": self.disponible,
        }


class AsesoriaEspecializada(Servicio):
    """Servicio derivado para asesorías técnicas (tarifa base por sesión).

    Modalidades aceptadas: 'remota', 'presencial' o 'hibrida' / 'híbrida'
    (se normalizan automáticamente a 'remota', 'presencial' o 'hibrida').
    """

    MODALIDADES_VALIDAS = ("remota", "presencial", "hibrida")

    def __init__(
        self,
        nombre: str,
        tarifa_base: float,
        especialidad: str,
        modalidad: str = "remota",
        disponible: bool = True,
    ):
        super().__init__(nombre, tarifa_base, disponible)
        self.especialidad = especialidad
        self.modalidad = modalidad

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("especialidad")
        self._especialidad = valor.strip()

    @property
    def modalidad(self) -> str:
        return self._modalidad

    @modalidad.setter
    def modalidad(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("modalidad")
        normalizada = _normalizar_texto(valor)
        if normalizada not in self.MODALIDADES_VALIDAS:
            raise DatoInvalidoError("modalidad", valor)
        self._modalidad = normalizada

    def calcular_costo(self, unidades: int, descuento: float = 0.0) -> float:
        """Calcula el costo por número de sesiones; aplica 1.20x si es presencial."""
        desc = self._validar_unidades_y_descuento(unidades, descuento)
        multiplicador_modalidad = 1.20 if self._modalidad == "presencial" else 1.0
        subtotal = self.tarifa_base * unidades * multiplicador_modalidad
        return round(subtotal * (1 - desc), 2)

    @singledispatchmethod
    def aplicar_ajuste_extra(self, ajuste):
        """Sobrecarga de método: aplica recargo porcentual (int/float) o nivel de certificación (str)."""
        raise DatoInvalidoError("ajuste", ajuste)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: int) -> float:
        if isinstance(ajuste, bool) or ajuste < 0:
            raise DatoInvalidoError("ajuste", ajuste)
        return round(self.tarifa_base * (1 + float(ajuste)), 2)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: float) -> float:
        if ajuste < 0:
            raise DatoInvalidoError("ajuste", ajuste)
        return round(self.tarifa_base * (1 + ajuste), 2)

    @aplicar_ajuste_extra.register
    def _(self, ajuste: str) -> str:
        certificacion = ajuste.strip()
        if not certificacion:
            raise DatoFaltanteError("certificacion")
        return f"[{self.codigo}] {self.nombre} ({self._especialidad}) - Certificación del asesor: {certificacion}"

    def describir(self) -> str:
        return (
            f"{self.nombre} (Especialidad: {self._especialidad}, modalidad: {self._modalidad}) "
            f"- Tarifa base: ${self.tarifa_base:,.2f}/sesión"
        )

    def obtener_detalle(self) -> dict:
        return {
            "codigo": self.codigo,
            "tipo": "AsesoriaEspecializada",
            "nombre": self.nombre,
            "tarifa_base": self.tarifa_base,
            "especialidad": self._especialidad,
            "modalidad": self._modalidad,
            "disponible": self.disponible,
        }

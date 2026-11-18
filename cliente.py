"""
===============================================================================
Sistema de Gestión de Servicios - Software FJ
Módulo: Cliente
Descripción: 
    - Implementa el modelo de cliente para el sistema de reservas de equipos.
    - Utiliza propiedades (@property y setters) para validar estrictamente 
      el ingreso de datos (nombres, correos, teléfonos y fechas de nacimiento).
    - Emplea expresiones regulares (módulo re) para asegurar el formato correcto 
      de los correos electrónicos.
    - Asigna un id_cliente autoincremental único administrado desde la clase.
===============================================================================
"""

import re
from datetime import datetime, date
from abc import ABC, abstractmethod
from src.excepciones import DatoInvalidoError, DatoFaltanteError

class EntidadAbstracta(ABC):
    """Clase abstracta base para todas las entidades del sistema Software FJ. 
    Define la estructura y los métodos que deben implementar las entidades concretas."""
    
    @abstractmethod
    def validar(self):
        """Valida que la entidad cumpla con los requisitos establecidos."""
        pass

    @abstractmethod
    def obtener_info(self):
        """Obtiene la información de la entidad y la valida."""
        pass


class Cliente(EntidadAbstracta):
    """Clase que representa a un cliente de la empresa de reservas de equipos tecnológicos."""

    # Atributo de clase para auto-incrementar el id_cliente
    _contador_id = 0

    def __init__(self, nombre, apellidos, email, telefono,
                 direccion=None, telefono_emergencia=None, fecha_nacimiento=None):
        """Inicializa un nuevo cliente con los datos proporcionados."""
        # Uso de setters para aplicar validaciones antes de asignar los valores
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.telefono_emergencia = telefono_emergencia
        self.fecha_nacimiento = fecha_nacimiento

        # Creación de un id_cliente único para cada instancia de Cliente
        Cliente._contador_id += 1
        self._id_cliente = Cliente._contador_id
        self._fecha_registro = datetime.now()

    # =========================== GETTERS Y SETTERS ===========================

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("nombre")
        valor_limpio = valor.strip()
        if not valor_limpio.replace(" ", "").isalpha() or not (2 <= len(valor_limpio) <= 50):
            raise DatoInvalidoError("nombre", valor)
        self._nombre = valor_limpio

    @property
    def apellidos(self):
        return self._apellidos

    @apellidos.setter
    def apellidos(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("apellidos")
        valor_limpio = valor.strip()
        if not valor_limpio.replace(" ", "").isalpha() or not (2 <= len(valor_limpio) <= 50):
            raise DatoInvalidoError("apellidos", valor)
        self._apellidos = valor_limpio

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("email")    
        valor_limpio = valor.strip()
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", valor_limpio):
            raise DatoInvalidoError("email", valor)
        self._email = valor_limpio

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoFaltanteError("telefono")
        valor_limpio = valor.strip()
        if not valor_limpio.isdigit() or len(valor_limpio) != 10:
            raise DatoInvalidoError("telefono", valor)
        self._telefono = valor_limpio

    @property
    def direccion(self):
        return self._direccion                                                                          

    @direccion.setter
    def direccion(self, valor):
        if valor is None:
            self._direccion = None
            return
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("direccion", valor)
        valor_limpio = valor.strip()
        if not (5 <= len(valor_limpio) <= 100):
            raise DatoInvalidoError("direccion", valor)
        self._direccion = valor_limpio
   
    @property
    def telefono_emergencia(self):
        return self._telefono_emergencia

    @telefono_emergencia.setter
    def telefono_emergencia(self, valor):
        if valor is None:
            self._telefono_emergencia = None
            return
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("telefono_emergencia", valor)
        valor_limpio = valor.strip()
        if not valor_limpio.isdigit() or len(valor_limpio) != 10:
            raise DatoInvalidoError("telefono_emergencia", valor)
        self._telefono_emergencia = valor_limpio

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, valor):
        if valor is None:
            self._fecha_nacimiento = None
            return

        if isinstance(valor, str):
            try:
                valor = datetime.strptime(valor.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise DatoInvalidoError("fecha_nacimiento", valor)
        elif isinstance(valor, datetime):
            valor = valor.date()
        elif not isinstance(valor, date):
            raise DatoInvalidoError("fecha_nacimiento", valor)

        hoy = date.today()
        if valor > hoy:
            raise DatoInvalidoError("fecha_nacimiento", valor)

        edad = hoy.year - valor.year - ((hoy.month, hoy.day) < (valor.month, valor.day))
        if edad < 18 or edad > 120:
            raise DatoInvalidoError("fecha_nacimiento", valor)

        self._fecha_nacimiento = valor

    # =========================== MÉTODOS ABSTRACTOS ===========================

    def validar(self):
        """Valida todos los atributos del cliente."""
        self.nombre = self._nombre
        self.apellidos = self._apellidos
        self.email = self._email
        self.telefono = self._telefono
        self.direccion = self._direccion
        self.telefono_emergencia = self._telefono_emergencia
        self.fecha_nacimiento = self._fecha_nacimiento
        return True

    def obtener_info(self):
        """Obtiene un diccionario con la información del cliente."""
        return {
            "id": self._id_cliente,
            "nombre": self._nombre,
            "apellidos": self._apellidos,
            "email": self._email, 
            "telefono": self._telefono,
            "direccion": self._direccion,
            "telefono_emergencia": self._telefono_emergencia,
            "fecha_nacimiento": self._fecha_nacimiento.strftime("%Y-%m-%d") if self._fecha_nacimiento else None,
            "fecha_registro": self._fecha_registro.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self):
        return f"Cliente(id={self._id_cliente}, nombre={self._nombre}, apellidos={self._apellidos})"

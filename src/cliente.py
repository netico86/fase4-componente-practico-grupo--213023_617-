import logging
from src.excepciones import DatoInvalidoError, DatoFaltanteError

class Cliente:
    def __init__(self, cedula: str, nombre: str, correo: str):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo

    @property
    def cedula(self) -> str:
        return self.__cedula

    @cedula.setter
    def cedula(self, valor: str):
        if not valor or not str(valor).strip():
            raise DatoFaltanteError("cedula")
        if not str(valor).isdigit():
            raise DatoInvalidoError("cedula")
        self.__cedula = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise DatoFaltanteError("nombre")
        self.__nombre = valor

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor:
            raise DatoInvalidoError("correo")
        self.__correo = valor
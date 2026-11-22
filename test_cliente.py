
import unittest

from src.cliente import Cliente
from src.excepciones import DatoInvalidoError, DatoFaltanteError


class TestCliente(unittest.TestCase):

    def crear_cliente(self, **cambios):
        datos = {
            "nombre": "Carlos",
            "apellidos": "Ramirez",
            "email": "carlos@example.com",
            "telefono": "3001234567"
        }
        datos.update(cambios)
        return Cliente(**datos)

    def test_01_cliente_valido(self):
        cliente = self.crear_cliente()
        self.assertTrue(cliente.validar())

    def test_02_nombre_vacio(self):
        with self.assertRaises(DatoFaltanteError):
            self.crear_cliente(nombre="")

    def test_03_nombre_con_numeros(self):
        with self.assertRaises(DatoInvalidoError):
            self.crear_cliente(nombre="Carlos123")

    def test_04_apellidos_vacios(self):
        with self.assertRaises(DatoFaltanteError):
            self.crear_cliente(apellidos="")

    def test_05_correo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            self.crear_cliente(email="correo_incorrecto")

    def test_06_telefono_corto(self):
        with self.assertRaises(DatoInvalidoError):
            self.crear_cliente(telefono="12345")

    def test_07_telefono_con_letras(self):
        with self.assertRaises(DatoInvalidoError):
            self.crear_cliente(telefono="300ABC4567")

    def test_08_fecha_futura(self):
        with self.assertRaises(DatoInvalidoError):
            self.crear_cliente(fecha_nacimiento="2999-01-01")

    def test_09_direccion_corta(self):
        with self.assertRaises(DatoInvalidoError):
            self.crear_cliente(direccion="AB")

    def test_10_identificadores_unicos(self):
        cliente1 = self.crear_cliente()
        cliente2 = self.crear_cliente()

        self.assertNotEqual(
            cliente1.obtener_info()["id"],
            cliente2.obtener_info()["id"]
        )

    def test_11_datos_opcionales(self):
        cliente = self.crear_cliente()
        informacion = cliente.obtener_info()

        self.assertIsNone(informacion["direccion"])
        self.assertIsNone(informacion["telefono_emergencia"])

    def test_12_actualizacion_correo(self):
        cliente = self.crear_cliente()
        cliente.email = "nuevo@example.com"

        self.assertEqual(cliente.email, "nuevo@example.com")


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ
Módulo principal: Simulaciones

Ejecuta 18 simulaciones (válidas e inválidas) que demuestran la robustez del
sistema: cada simulación es independiente y, si algo falla, el error se
captura, se registra en `logs/sistema.log` y el programa continúa.

Uso (desde la carpeta raíz del proyecto):
    python main.py
"""
import sys
from datetime import datetime, timedelta

# Evita UnicodeEncodeError en consolas que no usan UTF-8 (p. ej. Windows):
# los caracteres no representables se reemplazan en lugar de detener el programa.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.reservas import Reserva
from src.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from src.excepciones import SoftwareFJError
from src.gestor import GestorSoftwareFJ
from src.logger import registrar_error, registrar_evento


def imprimir_separador(titulo: str):
    """Imprime un encabezado visual para cada simulación."""
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def ok(mensaje: str):
    print(f"[OK] {mensaje}")


def error_esperado(e: Exception):
    """Muestra y registra un error que la simulación esperaba provocar."""
    print(f"[OK] Error capturado correctamente: {e}")
    registrar_error(e)


def error_inesperado(e: Exception):
    """Muestra y registra un error que no debía ocurrir."""
    print(f"[ERROR] {e}")
    registrar_error(e)


# =============================================================================
# SIMULACIONES (cada una recibe el gestor y un contexto compartido `ctx`)
# =============================================================================

def sim_01_cliente_valido(gestor, ctx):
    imprimir_separador("SIMULACIÓN 1: Registro de cliente válido")
    try:
        ctx["cliente1"] = gestor.registrar_cliente(
            nombre="Luis",
            apellidos="Bocanegra",
            email="luis.bocanegra@unad.edu.co",
            telefono="3001234567",
            direccion="Calle 123 #45-67, Bogotá",
            telefono_emergencia="3109876543",
            fecha_nacimiento="1995-03-15",
        )
    except SoftwareFJError as e:
        error_inesperado(e)
    else:
        ok(f"Cliente creado: {ctx['cliente1']}")
        registrar_evento(f"Simulación 1 exitosa: {ctx['cliente1']}")


def sim_02_email_invalido(gestor, ctx):
    imprimir_separador("SIMULACIÓN 2: Cliente inválido (email incorrecto)")
    try:
        gestor.registrar_cliente(
            nombre="Yeiber",
            apellidos="Cruz",
            email="yeiber-cruz.com",  # Falta el @
            telefono="3001234567",
            fecha_nacimiento="1998-07-20",
        )
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_03_menor_de_edad(gestor, ctx):
    imprimir_separador("SIMULACIÓN 3: Cliente inválido (menor de edad)")
    try:
        gestor.registrar_cliente(
            nombre="Pedro",
            apellidos="Perez",
            email="pedro@test.com",
            telefono="3001234567",
            fecha_nacimiento="2015-01-01",  # Menor de 18
        )
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_04_servicios_validos(gestor, ctx):
    imprimir_separador("SIMULACIÓN 4: Creación de servicios válidos")
    try:
        ctx["sala1"] = gestor.agregar_servicio(
            ReservaSala(
                nombre="Sala de Juntas A",
                tarifa_base=50000,
                capacidad=10,
                requiere_proyector=True,
            )
        )
        ctx["equipo1"] = gestor.agregar_servicio(
            AlquilerEquipo(
                nombre="Laptop Dell XPS",
                tarifa_base=80000,
                categoria_equipo="Computador",
                seguro_incluido=True,
            )
        )
        ctx["asesoria1"] = gestor.agregar_servicio(
            AsesoriaEspecializada(
                nombre="Asesoría en Python",
                tarifa_base=120000,
                especialidad="Programación",
                modalidad="remota",
            )
        )
    except SoftwareFJError as e:
        error_inesperado(e)
    else:
        # Polimorfismo: mismo método describir(), resultado distinto por clase
        for servicio in gestor.servicios:
            ok(servicio.describir())
        registrar_evento("Simulación 4: 3 servicios creados exitosamente")


def sim_05_reserva_valida(gestor, ctx):
    imprimir_separador("SIMULACIÓN 5: Reserva válida (flujo completo)")
    try:
        fecha = datetime.now() + timedelta(days=5)
        reserva = gestor.crear_reserva(ctx.get("cliente1"), ctx.get("sala1"), fecha, 3)
        ctx["reserva1"] = reserva
        reserva.confirmar()
        resultado = reserva.procesar()
    except SoftwareFJError as e:
        error_inesperado(e)
    else:
        ok(resultado)
        print(f"     Estado final: {reserva.estado}")
        print(f"     Costo total: ${reserva.costo_total:,.2f}")
        registrar_evento(f"Simulación 5 exitosa: {reserva}")


def sim_06_procesar_sin_confirmar(gestor, ctx):
    imprimir_separador("SIMULACIÓN 6: Procesar reserva sin confirmar")
    try:
        fecha = datetime.now() + timedelta(days=7)
        ctx["reserva2"] = gestor.crear_reserva(
            ctx.get("cliente1"), ctx.get("equipo1"), fecha, 2
        )
        resultado = ctx["reserva2"].procesar()  # Sin confirmar: debe fallar
        print(f"[ERROR] No debería llegar aquí: {resultado}")
    except SoftwareFJError as e:
        error_esperado(e)
        # Encadenamiento: el error original queda como causa (__cause__)
        if e.__cause__ is not None:
            print(f"     Causa original encadenada: {e.__cause__}")


def sim_07_cancelar_pendiente(gestor, ctx):
    imprimir_separador("SIMULACIÓN 7: Cancelar reserva pendiente")
    try:
        ctx["reserva2"].cancelar()
    except (SoftwareFJError, AttributeError, KeyError) as e:
        error_inesperado(e)
    else:
        ok(f"Reserva cancelada. Estado: {ctx['reserva2'].estado}")
        registrar_evento(f"Simulación 7: {ctx['reserva2']}")


def sim_08_cancelar_procesada(gestor, ctx):
    imprimir_separador("SIMULACIÓN 8: Cancelar reserva ya procesada")
    try:
        ctx["reserva1"].cancelar()  # Ya fue procesada en la simulación 5
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_09_confirmar_confirmada(gestor, ctx):
    imprimir_separador("SIMULACIÓN 9: Confirmar reserva ya procesada")
    try:
        ctx["reserva1"].confirmar()  # Ya no está Pendiente
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_10_servicio_no_disponible(gestor, ctx):
    imprimir_separador("SIMULACIÓN 10: Servicio no disponible")
    sala = ctx.get("sala1")
    try:
        sala.disponible = False  # Desactivamos el servicio
        fecha = datetime.now() + timedelta(days=10)
        reserva = gestor.crear_reserva(ctx.get("cliente1"), sala, fecha, 2)
        reserva.confirmar()
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)
    finally:
        if sala is not None:
            sala.disponible = True  # Siempre restauramos el servicio


def sim_11_duracion_invalida(gestor, ctx):
    imprimir_separador("SIMULACIÓN 11: Duración inválida")
    try:
        fecha = datetime.now() + timedelta(days=3)
        gestor.crear_reserva(ctx.get("cliente1"), ctx.get("equipo1"), fecha, 0)
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_12_cliente_nulo(gestor, ctx):
    imprimir_separador("SIMULACIÓN 12: Cliente nulo en reserva")
    try:
        fecha = datetime.now() + timedelta(days=4)
        gestor.crear_reserva(None, ctx.get("equipo1"), fecha, 2)
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_13_sobrecarga_ajustes(gestor, ctx):
    imprimir_separador("SIMULACIÓN 13: Sobrecarga de métodos (ajustes extra)")
    try:
        # int -> porcentaje entero; float -> fracción; str -> nota/accesorio
        ajuste_int = ctx["sala1"].aplicar_ajuste_extra(10)
        ok(f"Ajuste int (10 %) sobre sala: ${ajuste_int:,.2f}")
        ajuste_float = ctx["equipo1"].aplicar_ajuste_extra(0.15)
        ok(f"Ajuste float (15 %) sobre equipo: ${ajuste_float:,.2f}")
        ajuste_str = ctx["asesoria1"].aplicar_ajuste_extra("Certificado AWS")
        ok(f"Ajuste str: {ajuste_str}")
    except (SoftwareFJError, KeyError) as e:
        error_inesperado(e)
    else:
        registrar_evento("Simulación 13: sobrecarga probada exitosamente")


def sim_14_descuento_invalido(gestor, ctx):
    imprimir_separador("SIMULACIÓN 14: Descuento inválido")
    try:
        costo = ctx["sala1"].calcular_costo(2, descuento=1.5)
        print(f"[ERROR] No debería llegar aquí: ${costo}")
    except SoftwareFJError as e:
        error_esperado(e)
    except (KeyError, AttributeError) as e:
        error_inesperado(e)


def sim_15_modalidad_invalida(gestor, ctx):
    imprimir_separador("SIMULACIÓN 15: Modalidad inválida en asesoría")
    try:
        AsesoriaEspecializada(
            nombre="Asesoría Java",
            tarifa_base=100000,
            especialidad="Backend",
            modalidad="telefonica",  # No válida
        )
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_16_costos_con_descuento_e_impuesto(gestor, ctx):
    imprimir_separador("SIMULACIÓN 16: Cálculo de costos con descuento e IVA")
    try:
        sala = ctx["sala1"]
        ok(f"Solo unidades (2 h):            ${sala.calcular_costo(2):,.2f}")
        ok(f"Con 10 % de descuento:          ${sala.calcular_costo(2, 0.10):,.2f}")
        ok(
            "Con 10 % de descuento y 19 % IVA: "
            f"${sala.calcular_costo(2, descuento=0.10, impuesto=0.19):,.2f}"
        )
    except (SoftwareFJError, KeyError) as e:
        error_inesperado(e)
    else:
        registrar_evento("Simulación 16: variantes de calcular_costo probadas")


def sim_17_correo_duplicado(gestor, ctx):
    imprimir_separador("SIMULACIÓN 17: Cliente con correo ya registrado")
    try:
        gestor.registrar_cliente(
            nombre="Luisa",
            apellidos="Gomez",
            email="luis.bocanegra@unad.edu.co",  # Ya usado en la simulación 1
            telefono="3011112222",
        )
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


def sim_18_fecha_en_el_pasado(gestor, ctx):
    imprimir_separador("SIMULACIÓN 18: Reserva con fecha en el pasado")
    try:
        ayer = datetime.now() - timedelta(days=1)
        gestor.crear_reserva(ctx.get("cliente1"), ctx.get("asesoria1"), ayer, 1)
        print("[ERROR] No debería llegar aquí")
    except SoftwareFJError as e:
        error_esperado(e)


SIMULACIONES = [
    sim_01_cliente_valido,
    sim_02_email_invalido,
    sim_03_menor_de_edad,
    sim_04_servicios_validos,
    sim_05_reserva_valida,
    sim_06_procesar_sin_confirmar,
    sim_07_cancelar_pendiente,
    sim_08_cancelar_procesada,
    sim_09_confirmar_confirmada,
    sim_10_servicio_no_disponible,
    sim_11_duracion_invalida,
    sim_12_cliente_nulo,
    sim_13_sobrecarga_ajustes,
    sim_14_descuento_invalido,
    sim_15_modalidad_invalida,
    sim_16_costos_con_descuento_e_impuesto,
    sim_17_correo_duplicado,
    sim_18_fecha_en_el_pasado,
]


def ejecutar_simulaciones():
    """Ejecuta todas las simulaciones; un fallo en una no detiene las demás."""
    gestor = GestorSoftwareFJ()  # Listas internas de clientes, servicios y reservas
    ctx = {}                     # Objetos compartidos entre simulaciones

    for simulacion in SIMULACIONES:
        try:
            simulacion(gestor, ctx)
        except Exception as e:  # Red de seguridad: ningún error detiene el sistema
            print(f"[ERROR] Fallo no previsto en {simulacion.__name__}: {e}")
            registrar_error(e)
        finally:
            # Se ejecuta siempre, haya o no error
            registrar_evento(f"Finalizó {simulacion.__name__}")

    imprimir_separador("RESUMEN DE LAS LISTAS INTERNAS DEL GESTOR")
    print(gestor.resumen())

    print("\n" + "=" * 60)
    print(f"  {len(SIMULACIONES)} SIMULACIONES COMPLETADAS")
    print("  El sistema se mantuvo estable durante toda la ejecución")
    print("=" * 60)
    print("\nRevisa el archivo 'logs/sistema.log' para ver el registro completo.")


if __name__ == "__main__":
    # Bloque maestro: garantiza que la aplicación NUNCA se detenga
    try:
        registrar_evento("=== INICIO DE SIMULACIONES SOFTWARE FJ ===")
        ejecutar_simulaciones()
        registrar_evento("=== FIN DE SIMULACIONES SOFTWARE FJ ===")
    except Exception as e:
        registrar_error(e)
        print(f"\n[ERROR CRÍTICO] {e}")
        print("El sistema sigue activo gracias al manejo de excepciones.")


from datetime import date, datetime, timedelta
from collections import defaultdict


def calcular_total_venta(cantidad, precio_unitario):
    """Calcula el valor total de una venta."""
    return float(cantidad) * float(precio_unitario)


def calcular_total_ventas(ventas):
    """Suma los valores de una lista de ventas."""
    return sum(float(venta.get("total", 0)) for venta in ventas)


def calcular_promedio_ventas(ventas):
    """Calcula el promedio de ventas."""
    if not ventas:
        return 0

    return calcular_total_ventas(ventas) / len(ventas)


def calcular_porcentaje(parte, total):
    """Calcula qué porcentaje representa una cantidad respecto a otra."""
    if total == 0:
        return 0

    return (float(parte) / float(total)) * 100


def calcular_cumplimiento_meta(ventas, meta):
    """Calcula el porcentaje de cumplimiento de una meta."""
    if meta <= 0:
        return 0

    return calcular_porcentaje(ventas, meta)


def calcular_faltante_meta(ventas, meta):
    """Calcula cuánto falta para alcanzar una meta."""
    return max(float(meta) - float(ventas), 0)


def calcular_excedente_meta(ventas, meta):
    """Calcula cuánto se superó una meta."""
    return max(float(ventas) - float(meta), 0)


def calcular_ventas_por_sucursal(ventas):
    """Agrupa el total vendido por sucursal."""
    resultados = defaultdict(float)

    for venta in ventas:
        sucursal = venta.get("sucursal", "Sin sucursal")
        resultados[sucursal] += float(venta.get("total", 0))

    return dict(resultados)


def calcular_ventas_por_fecha(ventas):
    """Agrupa el total vendido por fecha."""
    resultados = defaultdict(float)

    for venta in ventas:
        fecha = str(venta.get("fecha", "Sin fecha"))
        resultados[fecha] += float(venta.get("total", 0))

    return dict(sorted(resultados.items()))


def calcular_ventas_por_periodo(ventas, fecha_inicio, fecha_fin):
    """Filtra y suma las ventas dentro de un periodo."""
    inicio = convertir_a_fecha(fecha_inicio)
    fin = convertir_a_fecha(fecha_fin)

    if inicio is None or fin is None:
        raise ValueError("Las fechas del periodo no son válidas.")

    if inicio > fin:
        raise ValueError("La fecha inicial no puede ser posterior a la final.")

    ventas_periodo = []

    for venta in ventas:
        fecha_venta = convertir_a_fecha(venta.get("fecha"))

        if fecha_venta and inicio <= fecha_venta <= fin:
            ventas_periodo.append(venta)

    return {
        "cantidad_ventas": len(ventas_periodo),
        "total_ventas": calcular_total_ventas(ventas_periodo),
        "promedio": calcular_promedio_ventas(ventas_periodo),
        "detalle": ventas_periodo
    }


def convertir_a_fecha(valor):
    """Convierte diferentes formatos de fecha a date."""
    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    if not valor:
        return None

    formatos = ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d")

    for formato in formatos:
        try:
            return datetime.strptime(str(valor), formato).date()
        except ValueError:
            continue

    return None


def calcular_variacion(valor_actual, valor_anterior):
    """Calcula la variación porcentual entre dos valores."""
    if valor_anterior == 0:
        return 100 if valor_actual > 0 else 0

    return (
        (float(valor_actual) - float(valor_anterior))
        / float(valor_anterior)
    ) * 100


def obtener_estado_meta(ventas, meta):
    """Determina el estado de cumplimiento de una meta."""
    ventas = float(ventas)
    meta = float(meta)

    if meta <= 0:
        return "Meta no definida"

    if ventas >= meta:
        return "Meta alcanzada"

    if ventas >= meta * 0.75:
        return "Cerca de alcanzar la meta"

    return "Meta pendiente"


from datetime import datetime


# ==========================================
# VALIDACIONES DEL SISTEMA
# ==========================================

def convertir_valor_monetario(valor):

    if isinstance(valor, (int, float)):
        resultado = float(valor)

    else:
        texto = str(valor).strip().upper()

        texto = texto.replace("$", "")
        texto = texto.replace("COP", "")
        texto = texto.replace(" ", "")

        if not texto:
            raise ValueError("El valor monetario esta vacio.")

        if "," in texto and "." in texto:

            if texto.rfind(",") > texto.rfind("."):
                texto = texto.replace(".", "")
                texto = texto.replace(",", ".")
            else:
                texto = texto.replace(",", "")

        elif "," in texto:

            partes = texto.split(",")

            if len(partes) == 2 and len(partes[1]) in (1, 2):
                texto = texto.replace(",", ".")
            else:
                texto = texto.replace(",", "")

        elif "." in texto:

            partes = texto.split(".")

            if len(partes) > 2:
                texto = texto.replace(".", "")

            elif len(partes) == 2 and len(partes[1]) == 3:
                texto = texto.replace(".", "")

        try:
            resultado = float(texto)

        except ValueError:
            raise ValueError(
                "Formato monetario incorrecto. "
                "Ejemplo: 500000 o 500.000"
            )

    if resultado <= 0:
        raise ValueError("El valor debe ser mayor que cero.")

    return resultado


def validar_fecha(fecha):

    try:
        datetime.strptime(str(fecha), "%Y-%m-%d")
        return True

    except (ValueError, TypeError):
        return False


def convertir_fecha(fecha):

    try:
        return datetime.strptime(
            str(fecha),
            "%Y-%m-%d"
        ).date()

    except (ValueError, TypeError):
        raise ValueError(
            "La fecha debe tener formato AAAA-MM-DD."
        )


def validar_rango_fechas(fecha_inicio, fecha_fin):

    inicio = convertir_fecha(fecha_inicio)
    fin = convertir_fecha(fecha_fin)

    if inicio > fin:
        raise ValueError(
            "La fecha inicial no puede ser posterior a la final."
        )

    return True


def validar_nombre(nombre):

    nombre = str(nombre).strip()

    if not nombre:
        raise ValueError("El nombre es obligatorio.")

    if len(nombre) < 2:
        raise ValueError("El nombre debe tener al menos dos caracteres.")

    return nombre


def validar_periodo(periodo):

    try:
        datetime.strptime(periodo, "%Y-W%W")
        return True

    except (ValueError, TypeError):
        raise ValueError("El periodo semanal no es valido.")


def validar_identificador(identificador):

    try:
        identificador = int(identificador)

        if identificador <= 0:
            raise ValueError()

        return identificador

    except (ValueError, TypeError):
        raise ValueError("El identificador no es valido.")

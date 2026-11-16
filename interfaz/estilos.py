
import customtkinter as ctk


# ==========================================
# CONFIGURACION GENERAL
# ==========================================

TEMA = "dark"
MODO_COLOR = "dark"

ctk.set_appearance_mode(MODO_COLOR)
ctk.set_default_color_theme("dark-blue")


# ==========================================
# PALETA DE COLORES: NEGRO Y DORADO
# ==========================================

COLORES = {
    "fondo": "#101114",
    "fondo_secundario": "#181A1F",
    "panel": "#202229",
    "panel_hover": "#292C34",

    "dorado": "#D4AF37",
    "dorado_claro": "#F1D77A",
    "dorado_oscuro": "#A88720",

    "blanco": "#FFFFFF",
    "texto": "#E8E8E8",
    "texto_secundario": "#A5A5A5",

    "verde": "#27AE60",
    "verde_claro": "#D5F5E3",

    "rojo": "#E74C3C",
    "rojo_claro": "#FADBD8",

    "azul": "#3498DB",
    "azul_claro": "#D6EAF8",

    "borde": "#383B44",
    "entrada": "#292C34",
}


# ==========================================
# TIPOGRAFIA
# ==========================================

FUENTES = {
    "titulo": ("Segoe UI", 25, "bold"),
    "subtitulo": ("Segoe UI", 17, "bold"),
    "seccion": ("Segoe UI", 15, "bold"),
    "normal": ("Segoe UI", 12),
    "pequena": ("Segoe UI", 10),
    "boton": ("Segoe UI", 12, "bold"),
    "indicador": ("Segoe UI", 23, "bold"),
}


# ==========================================
# DIMENSIONES
# ==========================================

ANCHO_VENTANA = 1280
ALTO_VENTANA = 760

ANCHO_MENU = 235
ALTO_CABECERA = 75


# ==========================================
# FUNCIONES DE ESTILO
# ==========================================

def configurar_ventana(ventana):
    """Configura la apariencia de la ventana principal."""
    ventana.configure(fg_color=COLORES["fondo"])
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.minsize(1050, 650)


def estilo_boton_principal():
    """Devuelve los parámetros para un botón principal."""
    return {
        "fg_color": COLORES["dorado"],
        "hover_color": COLORES["dorado_oscuro"],
        "text_color": "#111111",
        "font": FUENTES["boton"],
        "corner_radius": 8,
        "height": 40,
    }


def estilo_boton_secundario():
    """Devuelve los parámetros para un botón secundario."""
    return {
        "fg_color": COLORES["panel"],
        "hover_color": COLORES["panel_hover"],
        "text_color": COLORES["texto"],
        "font": FUENTES["normal"],
        "border_width": 1,
        "border_color": COLORES["borde"],
        "corner_radius": 8,
        "height": 40,
    }


def estilo_entrada():
    """Devuelve los parámetros para campos de texto."""
    return {
        "fg_color": COLORES["entrada"],
        "border_color": COLORES["borde"],
        "text_color": COLORES["blanco"],
        "placeholder_text_color": COLORES["texto_secundario"],
        "corner_radius": 7,
        "height": 38,
        "font": FUENTES["normal"],
    }


def estilo_tarjeta():
    """Devuelve los parámetros para tarjetas del panel."""
    return {
        "fg_color": COLORES["panel"],
        "corner_radius": 12,
        "border_width": 1,
        "border_color": COLORES["borde"],
    }


def estilo_titulo():
    """Devuelve los parámetros para títulos."""
    return {
        "font": FUENTES["titulo"],
        "text_color": COLORES["dorado"],
    }


def estilo_texto():
    """Devuelve los parámetros para textos normales."""
    return {
        "font": FUENTES["normal"],
        "text_color": COLORES["texto"],
    }

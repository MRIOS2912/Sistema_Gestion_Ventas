
import customtkinter as ctk

from interfaz.estilos import COLORES, FUENTES


class Tarjeta(ctk.CTkFrame):
    """Tarjeta reutilizable para mostrar información."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORES["panel"],
            corner_radius=12,
            border_width=1,
            border_color=COLORES["borde"],
            **kwargs
        )


class TituloSeccion(ctk.CTkLabel):
    """Título reutilizable para las secciones."""

    def __init__(self, master, texto, **kwargs):
        super().__init__(
            master,
            text=texto,
            font=FUENTES["subtitulo"],
            text_color=COLORES["dorado"],
            anchor="w",
            **kwargs
        )


class BotonPrincipal(ctk.CTkButton):
    """Botón principal con estilo dorado."""

    def __init__(self, master, texto, comando=None, **kwargs):
        super().__init__(
            master,
            text=texto,
            command=comando,
            fg_color=COLORES["dorado"],
            hover_color=COLORES["dorado_oscuro"],
            text_color="#111111",
            font=FUENTES["boton"],
            corner_radius=8,
            height=40,
            **kwargs
        )


class BotonSecundario(ctk.CTkButton):
    """Botón secundario con estilo oscuro."""

    def __init__(self, master, texto, comando=None, **kwargs):
        super().__init__(
            master,
            text=texto,
            command=comando,
            fg_color=COLORES["panel"],
            hover_color=COLORES["panel_hover"],
            text_color=kwargs.pop("text_color", COLORES["texto"]),
            font=FUENTES["normal"],
            border_width=1,
            border_color=COLORES["borde"],
            corner_radius=8,
            height=38,
            **kwargs
        )


class CampoTexto(ctk.CTkEntry):
    """Campo de entrada reutilizable."""

    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            fg_color=COLORES["entrada"],
            border_color=COLORES["borde"],
            text_color=COLORES["blanco"],
            placeholder_text_color=COLORES["texto_secundario"],
            corner_radius=7,
            height=38,
            font=FUENTES["normal"],
            **kwargs
        )


class Indicador(ctk.CTkFrame):
    """Tarjeta para mostrar indicadores del dashboard."""

    def __init__(
        self,
        master,
        titulo,
        valor="0",
        descripcion="",
        color_valor=None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=COLORES["panel"],
            corner_radius=12,
            border_width=1,
            border_color=COLORES["borde"],
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)

        self.etiqueta_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"],
            anchor="w"
        )
        self.etiqueta_titulo.grid(
            row=0, column=0, padx=18, pady=(16, 5), sticky="ew"
        )

        self.etiqueta_valor = ctk.CTkLabel(
            self,
            text=valor,
            font=FUENTES["indicador"],
            text_color=color_valor or COLORES["dorado"],
            anchor="w"
        )
        self.etiqueta_valor.grid(
            row=1, column=0, padx=18, pady=4, sticky="ew"
        )

        self.etiqueta_descripcion = ctk.CTkLabel(
            self,
            text=descripcion,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"],
            anchor="w"
        )
        self.etiqueta_descripcion.grid(
            row=2, column=0, padx=18, pady=(4, 16), sticky="ew"
        )

    def actualizar_valor(self, valor):
        """Actualiza el valor del indicador."""
        self.etiqueta_valor.configure(text=valor)

    def actualizar_descripcion(self, descripcion):
        """Actualiza la descripción del indicador."""
        self.etiqueta_descripcion.configure(text=descripcion)


class EtiquetaCampo(ctk.CTkLabel):
    """Etiqueta para formularios."""

    def __init__(self, master, texto, **kwargs):
        super().__init__(
            master,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color=COLORES["texto"],
            anchor="w",
            **kwargs
        )


class Separador(ctk.CTkFrame):
    """Línea divisoria horizontal."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            height=1,
            fg_color=COLORES["borde"],
            **kwargs
        )
        self.pack_propagate(False)

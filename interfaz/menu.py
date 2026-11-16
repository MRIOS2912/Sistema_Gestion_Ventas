
import customtkinter as ctk

from interfaz.estilos import COLORES, FUENTES


class MenuLateral(ctk.CTkFrame):
    """Menú lateral de navegación del sistema."""

    def __init__(self, master, navegar, **kwargs):
        super().__init__(
            master,
            width=235,
            fg_color=COLORES["fondo_secundario"],
            corner_radius=0,
            **kwargs
        )

        self.navegar = navegar
        self.botones = {}
        self.boton_activo = None

        self.grid_propagate(False)
        self.crear_encabezado()
        self.crear_opciones()
        self.crear_pie()

    def crear_encabezado(self):
        """Crea el encabezado del menú."""

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        encabezado.pack(
            fill="x",
            padx=18,
            pady=(28, 25)
        )

        ctk.CTkLabel(
            encabezado,
            text="SISTEMA",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORES["dorado"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="GESTIÓN DE VENTAS",
            font=("Segoe UI", 12, "bold"),
            text_color=COLORES["blanco"]
        ).pack(anchor="w", pady=(3, 0))

        ctk.CTkFrame(
            self,
            height=2,
            fg_color=COLORES["dorado"]
        ).pack(fill="x", padx=18, pady=(0, 20))

    def crear_opciones(self):
        """Crea los botones de navegación."""

        opciones = [
            ("Inicio", "Inicio"),
            ("Sucursales", "Sucursales"),
            ("Registrar ventas", "Ventas"),
            ("Consultas y cálculos", "Consultas"),
            ("Control de metas", "Metas"),
            ("Reportes", "Reportes"),
        ]

        contenedor = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        contenedor.pack(fill="x", padx=12)

        for texto, seccion in opciones:
            boton = ctk.CTkButton(
                contenedor,
                text=texto,
                anchor="w",
                height=43,
                corner_radius=8,
                fg_color="transparent",
                hover_color=COLORES["panel_hover"],
                text_color=COLORES["texto"],
                font=FUENTES["normal"],
                command=lambda pagina=seccion: self.seleccionar(pagina)
            )

            boton.pack(fill="x", pady=4)
            self.botones[seccion] = boton

    def seleccionar(self, seccion):
        """Actualiza el botón activo y abre la sección seleccionada."""

        if self.boton_activo in self.botones:
            self.botones[self.boton_activo].configure(
                fg_color="transparent",
                text_color=COLORES["texto"]
            )

        if seccion in self.botones:
            self.botones[seccion].configure(
                fg_color=COLORES["dorado"],
                text_color="#111111"
            )
            self.boton_activo = seccion

        self.navegar(seccion)

    def marcar_activo(self, seccion):
        """Permite marcar una sección desde la ventana principal."""

        if self.boton_activo in self.botones:
            self.botones[self.boton_activo].configure(
                fg_color="transparent",
                text_color=COLORES["texto"]
            )

        if seccion in self.botones:
            self.botones[seccion].configure(
                fg_color=COLORES["dorado"],
                text_color="#111111"
            )
            self.boton_activo = seccion

    def crear_pie(self):
        """Crea el pie del menú."""

        pie = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        pie.pack(side="bottom", fill="x", padx=18, pady=20)

        ctk.CTkFrame(
            pie,
            height=1,
            fg_color=COLORES["borde"]
        ).pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            pie,
            text="Gestión de Ventas",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            pie,
            text="Versión 1.0",
            font=FUENTES["pequena"],
            text_color=COLORES["dorado"]
        ).pack(anchor="w", pady=(3, 0))

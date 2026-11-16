import customtkinter as ctk
import sys
from pathlib import Path
from tkinter import messagebox
from datetime import date

from database import conectar, inicializar_base_datos

from interfaz.estilos import (
    COLORES,
    FUENTES,
    configurar_ventana
)

from interfaz.menu import MenuLateral

from interfaz.componentes import (
    Tarjeta,
    TituloSeccion,
    BotonSecundario
)

from modulos.sucursales import SucursalesFrame
from modulos.ventas import VentasFrame
from modulos.consultas import ConsultasFrame
from modulos.metas import MetasFrame
from modulos.reportes import ReportesFrame


def obtener_ruta_icono():
    """Localiza el icono dorado al ejecutar Python o el EXE."""

    nombre_icono = "icono_barras_solo_dorado.ico"

    if getattr(sys, "frozen", False):
        carpeta_aplicacion = Path(sys.executable).resolve().parent

        # PyInstaller 6 puede guardar los archivos adicionales
        # dentro de la carpeta _internal.
        carpetas_posibles = [
            Path(getattr(sys, "_MEIPASS", carpeta_aplicacion)),
            carpeta_aplicacion,
            carpeta_aplicacion / "_internal",
        ]

    else:
        carpeta_aplicacion = Path(__file__).resolve().parent
        carpetas_posibles = [carpeta_aplicacion]

    for carpeta in carpetas_posibles:
        ruta = carpeta / nombre_icono

        if ruta.is_file():
            return ruta

    return carpetas_posibles[0] / nombre_icono


class SistemaGestionVentas(ctk.CTk):
    """Ventana principal del sistema de gestión de ventas."""

    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión de Ventas")

        # Icono dorado de barras ascendentes en la ventana.
        ruta_icono = obtener_ruta_icono()

        if ruta_icono.is_file():
            try:
                self.iconbitmap(default=str(ruta_icono))
            except Exception as error:
                print(
                    f"No se pudo cargar el icono de la ventana: {error}"
                )

        configurar_ventana(self)

        self.pantalla_actual = None
        self.seccion_actual = None

        self.crear_estructura()
        self.mostrar_seccion("Inicio")

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

    def crear_estructura(self):
        """Organiza el menú lateral y el área de contenido."""

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu = MenuLateral(
            self,
            navegar=self.mostrar_seccion
        )

        self.menu.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.area_principal = ctk.CTkFrame(
            self,
            fg_color=COLORES["fondo"],
            corner_radius=0
        )

        self.area_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.area_principal.grid_columnconfigure(
            0,
            weight=1
        )

        self.area_principal.grid_rowconfigure(
            1,
            weight=1
        )

        self.crear_cabecera()

        self.contenedor_pantallas = ctk.CTkFrame(
            self.area_principal,
            fg_color=COLORES["fondo"],
            corner_radius=0
        )

        self.contenedor_pantallas.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.contenedor_pantallas.grid_columnconfigure(
            0,
            weight=1
        )

        self.contenedor_pantallas.grid_rowconfigure(
            0,
            weight=1
        )

    def crear_cabecera(self):
        """Crea la cabecera superior de la aplicación."""

        cabecera = ctk.CTkFrame(
            self.area_principal,
            height=75,
            fg_color=COLORES["fondo_secundario"],
            corner_radius=0
        )

        cabecera.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        cabecera.grid_columnconfigure(
            0,
            weight=1
        )

        self.titulo_cabecera = ctk.CTkLabel(
            cabecera,
            text="Inicio",
            font=("Segoe UI", 19, "bold"),
            text_color=COLORES["blanco"]
        )

        self.titulo_cabecera.grid(
            row=0,
            column=0,
            padx=25,
            pady=20,
            sticky="w"
        )

        ctk.CTkLabel(
            cabecera,
            text="SISTEMA DE GESTIÓN",
            font=("Segoe UI", 10, "bold"),
            text_color=COLORES["dorado"]
        ).grid(
            row=0,
            column=1,
            padx=25,
            pady=20
        )

    def limpiar_pantalla(self):
        """Elimina la pantalla anterior."""

        if self.pantalla_actual is not None:
            self.pantalla_actual.destroy()
            self.pantalla_actual = None

    def mostrar_seccion(self, seccion):
        """Abre la pantalla seleccionada en el menú."""

        self.limpiar_pantalla()

        self.seccion_actual = seccion

        self.titulo_cabecera.configure(
            text=seccion
        )

        if seccion == "Inicio":
            pantalla = InicioFrame(
                self.contenedor_pantallas
            )

        elif seccion == "Sucursales":
            pantalla = SucursalesFrame(
                self.contenedor_pantallas
            )

        elif seccion == "Ventas":
            pantalla = VentasFrame(
                self.contenedor_pantallas
            )

        elif seccion == "Consultas":
            pantalla = ConsultasFrame(
                self.contenedor_pantallas
            )

        elif seccion == "Metas":
            pantalla = MetasFrame(
                self.contenedor_pantallas
            )

        elif seccion == "Reportes":
            pantalla = ReportesFrame(
                self.contenedor_pantallas
            )

        else:
            messagebox.showwarning(
                "Sección no disponible",
                "La sección seleccionada no existe."
            )
            return

        pantalla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.pantalla_actual = pantalla

        self.menu.marcar_activo(seccion)

    def cerrar_aplicacion(self):
        """Solicita confirmación antes de cerrar."""

        confirmar = messagebox.askyesno(
            "Cerrar aplicación",
            "¿Deseas salir del Sistema de Gestión de Ventas?"
        )

        if confirmar:
            self.destroy()


class InicioFrame(ctk.CTkFrame):
    """Panel principal con indicadores generales."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORES["fondo"],
            **kwargs
        )

        self.crear_interfaz()
        self.actualizar_indicadores()

    def crear_interfaz(self):
        """Construye el panel de inicio."""

        self.grid_columnconfigure(
            0,
            weight=1
        )

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        encabezado.grid(
            row=0,
            column=0,
            padx=30,
            pady=(30, 10),
            sticky="ew"
        )

        TituloSeccion(
            encabezado,
            "Panel de control"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Resumen general de la actividad comercial.",
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        self.contenedor_indicadores = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.contenedor_indicadores.grid(
            row=1,
            column=0,
            padx=25,
            pady=20,
            sticky="ew"
        )

        self.contenedor_indicadores.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.tarjeta_sucursales = self.crear_indicador(
            self.contenedor_indicadores,
            "Sucursales activas",
            "0",
            "Establecimientos registrados"
        )

        self.tarjeta_sucursales.grid(
            row=0,
            column=0,
            padx=7,
            sticky="ew"
        )

        self.tarjeta_ventas = self.crear_indicador(
            self.contenedor_indicadores,
            "Ventas registradas",
            "0",
            "Operaciones almacenadas"
        )

        self.tarjeta_ventas.grid(
            row=0,
            column=1,
            padx=7,
            sticky="ew"
        )

        self.tarjeta_total = self.crear_indicador(
            self.contenedor_indicadores,
            "Total vendido",
            "$0",
            "Acumulado general"
        )

        self.tarjeta_total.grid(
            row=0,
            column=2,
            padx=7,
            sticky="ew"
        )

        self.tarjeta_promedio = self.crear_indicador(
            self.contenedor_indicadores,
            "Promedio por venta",
            "$0",
            "Valor promedio de las operaciones"
        )

        self.tarjeta_promedio.grid(
            row=1,
            column=0,
            padx=7,
            pady=12,
            sticky="ew"
        )

        self.tarjeta_metas = self.crear_indicador(
            self.contenedor_indicadores,
            "Metas configuradas",
            "0",
            "Objetivos registrados"
        )

        self.tarjeta_metas.grid(
            row=1,
            column=1,
            padx=7,
            pady=12,
            sticky="ew"
        )

        self.tarjeta_mes = self.crear_indicador(
            self.contenedor_indicadores,
            "Ventas del mes",
            "$0",
            "Acumulado mensual"
        )

        self.tarjeta_mes.grid(
            row=1,
            column=2,
            padx=7,
            pady=12,
            sticky="ew"
        )

        tarjeta_bienvenida = Tarjeta(self)

        tarjeta_bienvenida.grid(
            row=2,
            column=0,
            padx=32,
            pady=(15, 20),
            sticky="ew"
        )

        ctk.CTkLabel(
            tarjeta_bienvenida,
            text="Bienvenido al Sistema de Gestión de Ventas",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORES["dorado"]
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 8)
        )

        ctk.CTkLabel(
            tarjeta_bienvenida,
            text=(
                "Administra tus sucursales, registra operaciones, "
                "controla metas y consulta los resultados comerciales "
                "desde un solo lugar."
            ),
            font=FUENTES["normal"],
            text_color=COLORES["texto"],
            wraplength=750,
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 22)
        )

        BotonSecundario(
            tarjeta_bienvenida,
            "Actualizar indicadores",
            self.actualizar_indicadores
        ).pack(
            anchor="e",
            padx=22,
            pady=(0, 18)
        )

    def crear_indicador(
        self,
        master,
        titulo,
        valor,
        descripcion
    ):
        """Crea una tarjeta de indicador."""

        tarjeta = Tarjeta(master)

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(
            anchor="w",
            padx=16,
            pady=(16, 5)
        )

        etiqueta_valor = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Segoe UI", 22, "bold"),
            text_color=COLORES["dorado"]
        )

        etiqueta_valor.pack(
            anchor="w",
            padx=16,
            pady=3
        )

        ctk.CTkLabel(
            tarjeta,
            text=descripcion,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"]
        ).pack(
            anchor="w",
            padx=16,
            pady=(3, 16)
        )

        tarjeta.etiqueta_valor = etiqueta_valor

        return tarjeta

    def actualizar_indicadores(self):
        """Consulta la base de datos y actualiza el panel."""

        try:
            mes_actual = date.today().strftime("%Y-%m")

            with conectar() as conexion:

                sucursales = conexion.execute("""
                    SELECT COUNT(*)
                    FROM sucursales
                    WHERE estado = 'Activa'
                """).fetchone()[0]

                cantidad_ventas = conexion.execute("""
                    SELECT COUNT(*)
                    FROM ventas
                """).fetchone()[0]

                total_general = conexion.execute("""
                    SELECT COALESCE(SUM(total), 0)
                    FROM ventas
                """).fetchone()[0]

                total_mes = conexion.execute("""
                    SELECT COALESCE(SUM(total), 0)
                    FROM ventas
                    WHERE strftime('%Y-%m', fecha) = ?
                """, (mes_actual,)).fetchone()[0]

                metas = conexion.execute("""
                    SELECT COUNT(*)
                    FROM metas
                """).fetchone()[0]

            promedio = (
                float(total_general) / cantidad_ventas
                if cantidad_ventas else 0
            )

            self.tarjeta_sucursales.etiqueta_valor.configure(
                text=str(sucursales)
            )

            self.tarjeta_ventas.etiqueta_valor.configure(
                text=str(cantidad_ventas)
            )

            self.tarjeta_total.etiqueta_valor.configure(
                text=f"${float(total_general):,.0f}"
            )

            self.tarjeta_promedio.etiqueta_valor.configure(
                text=f"${promedio:,.0f}"
            )

            self.tarjeta_metas.etiqueta_valor.configure(
                text=str(metas)
            )

            self.tarjeta_mes.etiqueta_valor.configure(
                text=f"${float(total_mes):,.0f}"
            )

        except Exception as error:
            messagebox.showerror(
                "Error de indicadores",
                f"No fue posible actualizar el panel.\n\n{error}"
            )


def iniciar_aplicacion():
    """Inicializa la base de datos y ejecuta la aplicación."""

    try:
        inicializar_base_datos()

        aplicacion = SistemaGestionVentas()
        aplicacion.mainloop()

    except Exception as error:
        messagebox.showerror(
            "Error al iniciar",
            f"No fue posible iniciar el sistema.\n\n{error}"
        )


if __name__ == "__main__":
    iniciar_aplicacion()

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import conectar
from interfaz.estilos import COLORES, FUENTES
from interfaz.componentes import (
    Tarjeta,
    BotonPrincipal,
    BotonSecundario,
    CampoTexto,
    EtiquetaCampo,
    TituloSeccion
)
from servicios.validaciones import convertir_valor_monetario


class ConsultasFrame(ctk.CTkFrame):
    """Módulo de consultas y análisis de ventas."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORES["fondo"],
            **kwargs
        )

        self.sucursales = {}
        self.resultados = []
        self.canvas_grafica = None

        self.crear_interfaz()
        self.cargar_sucursales()
        self.consultar_ventas()

    def crear_interfaz(self):
        """Construye la pantalla de consultas."""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        encabezado.grid(
            row=0,
            column=0,
            padx=25,
            pady=(20, 10),
            sticky="ew"
        )

        TituloSeccion(
            encabezado,
            "Consultas y análisis"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Filtra, consulta y analiza el comportamiento de las ventas.",
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w", pady=(5, 0))

        self.crear_filtros()
        self.crear_resultados()

    def crear_filtros(self):
        """Crea los filtros de consulta."""

        tarjeta = Tarjeta(self)
        tarjeta.grid(
            row=1,
            column=0,
            padx=25,
            pady=10,
            sticky="ew"
        )

        tarjeta.grid_columnconfigure((0, 1, 2), weight=1)

        TituloSeccion(
            tarjeta,
            "Filtros de búsqueda"
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            padx=18,
            pady=(15, 12),
            sticky="w"
        )

        EtiquetaCampo(
            tarjeta,
            "Sucursal"
        ).grid(
            row=1,
            column=0,
            padx=18,
            sticky="w"
        )

        self.combo_sucursal = ctk.CTkComboBox(
            tarjeta,
            values=["Todas las sucursales"],
            state="readonly",
            height=38,
            fg_color=COLORES["entrada"],
            border_color=COLORES["borde"],
            button_color=COLORES["dorado"],
            button_hover_color=COLORES["dorado_oscuro"],
            text_color=COLORES["blanco"],
            font=FUENTES["normal"]
        )
        self.combo_sucursal.grid(
            row=2,
            column=0,
            padx=18,
            pady=(5, 12),
            sticky="ew"
        )
        self.combo_sucursal.set("Todas las sucursales")

        EtiquetaCampo(
            tarjeta,
            "Fecha inicial"
        ).grid(
            row=1,
            column=1,
            padx=18,
            sticky="w"
        )

        self.fecha_inicio = CampoTexto(
            tarjeta,
            "AAAA-MM-DD"
        )
        self.fecha_inicio.insert(
            0,
            date.today().replace(day=1).isoformat()
        )
        self.fecha_inicio.grid(
            row=2,
            column=1,
            padx=18,
            pady=(5, 12),
            sticky="ew"
        )

        EtiquetaCampo(
            tarjeta,
            "Fecha final"
        ).grid(
            row=1,
            column=2,
            padx=18,
            sticky="w"
        )

        self.fecha_fin = CampoTexto(
            tarjeta,
            "AAAA-MM-DD"
        )
        self.fecha_fin.insert(
            0,
            date.today().isoformat()
        )
        self.fecha_fin.grid(
            row=2,
            column=2,
            padx=18,
            pady=(5, 12),
            sticky="ew"
        )

        acciones = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )
        acciones.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=18,
            pady=(0, 15),
            sticky="e"
        )

        BotonSecundario(
            acciones,
            "Limpiar filtros",
            self.limpiar_filtros
        ).pack(side="left", padx=5)

        BotonPrincipal(
            acciones,
            "Consultar",
            self.consultar_ventas
        ).pack(side="left", padx=5)

    def crear_resultados(self):
        """Crea el espacio para indicadores, tabla y gráfica."""

        contenedor = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        contenedor.grid(
            row=2,
            column=0,
            padx=25,
            pady=(10, 20),
            sticky="nsew"
        )

        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_rowconfigure(2, weight=1)

        self.tarjetas_indicadores = ctk.CTkFrame(
            contenedor,
            fg_color="transparent"
        )
        self.tarjetas_indicadores.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        self.tarjetas_indicadores.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.indicador_total = self.crear_indicador(
            self.tarjetas_indicadores,
            "Total vendido",
            "$0"
        )
        self.indicador_total.grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="ew"
        )

        self.indicador_cantidad = self.crear_indicador(
            self.tarjetas_indicadores,
            "Número de ventas",
            "0"
        )
        self.indicador_cantidad.grid(
            row=0,
            column=1,
            padx=6,
            sticky="ew"
        )

        self.indicador_promedio = self.crear_indicador(
            self.tarjetas_indicadores,
            "Promedio por venta",
            "$0"
        )
        self.indicador_promedio.grid(
            row=0,
            column=2,
            padx=(6, 0),
            sticky="ew"
        )

        TituloSeccion(
            contenedor,
            "Resultados por sucursal"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 10)
        )

        self.contenedor_resultados = ctk.CTkScrollableFrame(
            contenedor,
            fg_color=COLORES["fondo_secundario"],
            corner_radius=10
        )
        self.contenedor_resultados.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

    def crear_indicador(self, master, titulo, valor):
        """Construye una tarjeta de indicador."""

        tarjeta = Tarjeta(master)

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"]
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 5)
        )

        etiqueta = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Segoe UI", 18, "bold"),
            text_color=COLORES["dorado"]
        )
        etiqueta.pack(
            anchor="w",
            padx=12,
            pady=(0, 12)
        )

        tarjeta.etiqueta_valor = etiqueta
        return tarjeta

    def cargar_sucursales(self):
        """Carga todas las sucursales disponibles."""

        try:
            with conectar() as conexion:
                registros = conexion.execute("""
                    SELECT id, nombre
                    FROM sucursales
                    ORDER BY nombre
                """).fetchall()

            self.sucursales = {
                registro["nombre"]: registro["id"]
                for registro in registros
            }

            opciones = ["Todas las sucursales"] + list(
                self.sucursales.keys()
            )

            self.combo_sucursal.configure(values=opciones)
            self.combo_sucursal.set("Todas las sucursales")

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar las sucursales.\n\n{error}"
            )

    def consultar_ventas(self):
        """Consulta las ventas según los filtros seleccionados."""

        inicio_texto = self.fecha_inicio.get().strip()
        fin_texto = self.fecha_fin.get().strip()
        nombre_sucursal = self.combo_sucursal.get()

        try:
            inicio = date.fromisoformat(inicio_texto)
            fin = date.fromisoformat(fin_texto)

            if inicio > fin:
                messagebox.showwarning(
                    "Periodo incorrecto",
                    "La fecha inicial no puede ser posterior a la fecha final."
                )
                return

            consulta = """
                SELECT
                    ventas.id,
                    ventas.fecha,
                    ventas.concepto,
                    ventas.cantidad,
                    ventas.precio_unitario,
                    ventas.total,
                    sucursales.nombre AS sucursal
                FROM ventas
                INNER JOIN sucursales
                    ON ventas.sucursal_id = sucursales.id
                WHERE ventas.fecha BETWEEN ? AND ?
            """

            parametros = [inicio.isoformat(), fin.isoformat()]

            if nombre_sucursal in self.sucursales:
                consulta += " AND ventas.sucursal_id = ?"
                parametros.append(self.sucursales[nombre_sucursal])

            consulta += " ORDER BY ventas.fecha DESC, ventas.id DESC"

            with conectar() as conexion:
                self.resultados = conexion.execute(
                    consulta,
                    parametros
                ).fetchall()

            self.actualizar_indicadores()
            self.mostrar_resultados()
            self.mostrar_grafica()

        except ValueError:
            messagebox.showwarning(
                "Fecha incorrecta",
                "Introduce las fechas con el formato AAAA-MM-DD."
            )

        except Exception as error:
            messagebox.showerror(
                "Error de consulta",
                f"No fue posible consultar las ventas.\n\n{error}"
            )

    def actualizar_indicadores(self):
        """Actualiza los indicadores generales."""

        cantidad = len(self.resultados)
        total = sum(float(v["total"]) for v in self.resultados)
        promedio = total / cantidad if cantidad else 0

        self.indicador_total.etiqueta_valor.configure(
            text=f"${total:,.0f}"
        )

        self.indicador_cantidad.etiqueta_valor.configure(
            text=str(cantidad)
        )

        self.indicador_promedio.etiqueta_valor.configure(
            text=f"${promedio:,.0f}"
        )

    def mostrar_resultados(self):
        """Muestra los registros encontrados."""

        for widget in self.contenedor_resultados.winfo_children():
            widget.destroy()

        if not self.resultados:
            ctk.CTkLabel(
                self.contenedor_resultados,
                text="No se encontraron ventas para el periodo seleccionado.",
                font=FUENTES["normal"],
                text_color=COLORES["texto_secundario"]
            ).pack(pady=25)
            return

        resumen = {}

        for venta in self.resultados:
            sucursal = venta["sucursal"]
            resumen[sucursal] = resumen.get(sucursal, 0) + float(
                venta["total"]
            )

        for sucursal, total in sorted(resumen.items()):
            tarjeta = Tarjeta(self.contenedor_resultados)
            tarjeta.pack(
                fill="x",
                padx=8,
                pady=6
            )

            ctk.CTkLabel(
                tarjeta,
                text=sucursal,
                font=("Segoe UI", 14, "bold"),
                text_color=COLORES["texto"]
            ).pack(
                side="left",
                padx=15,
                pady=12
            )

            ctk.CTkLabel(
                tarjeta,
                text=f"${total:,.0f} COP",
                font=("Segoe UI", 14, "bold"),
                text_color=COLORES["dorado"]
            ).pack(
                side="right",
                padx=15,
                pady=12
            )

        BotonSecundario(
            self.contenedor_resultados,
            "Ver gráfica ampliada",
            self.mostrar_grafica_ventana
        ).pack(
            anchor="e",
            padx=8,
            pady=10
        )

    def mostrar_grafica(self):
        """Genera una gráfica de ventas por sucursal."""

        if self.canvas_grafica is not None:
            self.canvas_grafica.get_tk_widget().destroy()
            self.canvas_grafica = None

        resumen = {}

        for venta in self.resultados:
            sucursal = venta["sucursal"]
            resumen[sucursal] = resumen.get(sucursal, 0) + float(
                venta["total"]
            )

        if not resumen:
            return

        figura, eje = plt.subplots(figsize=(8, 3.5))

        nombres = list(resumen.keys())
        valores = list(resumen.values())

        eje.barh(
            nombres,
            valores,
            color="#D4AF37"
        )

        eje.set_title(
            "Ventas por sucursal",
            color="white"
        )
        eje.set_xlabel(
            "Valor vendido (COP)",
            color="white"
        )

        eje.tick_params(colors="white")
        eje.set_facecolor("#202229")
        figura.patch.set_facecolor("#202229")

        figura.tight_layout()

        self.canvas_grafica = FigureCanvasTkAgg(
            figura,
            master=self.contenedor_resultados
        )

        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        plt.close(figura)

    def mostrar_grafica_ventana(self):
        """Abre una ventana independiente con la gráfica."""

        resumen = {}

        for venta in self.resultados:
            sucursal = venta["sucursal"]
            resumen[sucursal] = resumen.get(sucursal, 0) + float(
                venta["total"]
            )

        if not resumen:
            messagebox.showinfo(
                "Sin información",
                "No hay datos para generar una gráfica."
            )
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Análisis de ventas por sucursal")
        ventana.geometry("850x500")
        ventana.configure(fg_color=COLORES["fondo"])

        figura, eje = plt.subplots(figsize=(9, 4.5))

        eje.barh(
            list(resumen.keys()),
            list(resumen.values()),
            color="#D4AF37"
        )

        eje.set_title(
            "Ventas por sucursal",
            color="white"
        )
        eje.set_xlabel(
            "Valor vendido (COP)",
            color="white"
        )
        eje.tick_params(colors="white")
        eje.set_facecolor("#202229")
        figura.patch.set_facecolor("#202229")
        figura.tight_layout()

        canvas = FigureCanvasTkAgg(
            figura,
            master=ventana
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        plt.close(figura)

    def limpiar_filtros(self):
        """Restablece los filtros de consulta."""

        self.combo_sucursal.set("Todas las sucursales")

        self.fecha_inicio.delete(0, "end")
        self.fecha_inicio.insert(
            0,
            date.today().replace(day=1).isoformat()
        )

        self.fecha_fin.delete(0, "end")
        self.fecha_fin.insert(
            0,
            date.today().isoformat()
        )

        self.consultar_ventas()

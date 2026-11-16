
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from tkinter import filedialog

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


class ReportesFrame(ctk.CTkFrame):
    """Módulo para consultar y exportar reportes de ventas."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORES["fondo"],
            **kwargs
        )

        self.resultados = []

        self.crear_interfaz()
        self.consultar_reporte()

    def crear_interfaz(self):
        """Construye la pantalla de reportes."""

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
            pady=(14, 6),
            sticky="ew"
        )

        TituloSeccion(
            encabezado,
            "Reportes de ventas"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Consulta los resultados y genera archivos para tus informes.",
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w", pady=(5, 0))

        self.crear_filtros()
        self.crear_area_resultados()

    def crear_filtros(self):
        """Crea los filtros para generar reportes."""

        tarjeta = Tarjeta(self)
        tarjeta.grid(
            row=1,
            column=0,
            padx=25,
            pady=6,
            sticky="ew"
        )

        tarjeta.grid_columnconfigure((0, 1), weight=1)

        TituloSeccion(
            tarjeta,
            "Periodo del reporte"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=18,
            pady=(15, 12),
            sticky="w"
        )

        EtiquetaCampo(
            tarjeta,
            "Fecha inicial"
        ).grid(
            row=1,
            column=0,
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
            column=0,
            padx=18,
            pady=(5, 12),
            sticky="ew"
        )

        EtiquetaCampo(
            tarjeta,
            "Fecha final"
        ).grid(
            row=1,
            column=1,
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
            column=1,
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
            columnspan=2,
            padx=18,
            pady=(0, 15),
            sticky="e"
        )

        BotonSecundario(
            acciones,
            "Consultar",
            self.consultar_reporte
        ).pack(side="left", padx=5)

        BotonPrincipal(
            acciones,
            "Exportar a Excel",
            self.exportar_excel
        ).pack(side="left", padx=5)

    def crear_area_resultados(self):
        """Prepara los indicadores y la lista de resultados."""

        contenedor = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        contenedor.grid(
            row=2,
            column=0,
            padx=25,
            pady=(6, 14),
            sticky="nsew"
        )

        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_rowconfigure(2, weight=1)

        self.tarjeta_resumen = Tarjeta(contenedor)
        self.tarjeta_resumen.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        self.etiqueta_cantidad = ctk.CTkLabel(
            self.tarjeta_resumen,
            text="Productos registrados: 0",
            font=FUENTES["normal"],
            text_color=COLORES["texto"]
        )
        self.etiqueta_cantidad.pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        self.etiqueta_total = ctk.CTkLabel(
            self.tarjeta_resumen,
            text="Total vendido: $0 COP",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORES["dorado"]
        )
        self.etiqueta_total.pack(
            anchor="w",
            padx=18,
            pady=5
        )

        self.etiqueta_promedio = ctk.CTkLabel(
            self.tarjeta_resumen,
            text="Promedio por venta: $0 COP",
            font=FUENTES["normal"],
            text_color=COLORES["texto"]
        )
        self.etiqueta_promedio.pack(
            anchor="w",
            padx=18,
            pady=(5, 15)
        )

        TituloSeccion(
            contenedor,
            "Detalle del reporte"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 10)
        )

        self.lista_resultados = ctk.CTkScrollableFrame(
            contenedor,
            fg_color=COLORES["fondo_secundario"],
            corner_radius=10
        )
        self.lista_resultados.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

    def consultar_reporte(self):
        """Consulta las ventas del periodo seleccionado."""

        inicio_texto = self.fecha_inicio.get().strip()
        fin_texto = self.fecha_fin.get().strip()

        try:
            fecha_inicio = date.fromisoformat(inicio_texto)
            fecha_fin = date.fromisoformat(fin_texto)

            if fecha_inicio > fecha_fin:
                messagebox.showwarning(
                    "Periodo incorrecto",
                    "La fecha inicial no puede ser posterior a la final."
                )
                return

            with conectar() as conexion:
                self.resultados = conexion.execute("""
                    SELECT
                        ventas.id,
                        ventas.fecha,
                        sucursales.nombre AS sucursal,
                        ventas.concepto,
                        ventas.cantidad,
                        ventas.precio_unitario,
                        ventas.total,
                        ventas.observaciones
                    FROM ventas
                    INNER JOIN sucursales
                        ON ventas.sucursal_id = sucursales.id
                    WHERE ventas.fecha BETWEEN ? AND ?
                    ORDER BY ventas.fecha DESC, ventas.id DESC
                """, (
                    fecha_inicio.isoformat(),
                    fecha_fin.isoformat()
                )).fetchall()

            self.actualizar_resumen()
            self.mostrar_detalle()

        except ValueError:
            messagebox.showwarning(
                "Fecha incorrecta",
                "Utiliza el formato AAAA-MM-DD para las fechas."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible generar el reporte.\n\n{error}"
            )

    def actualizar_resumen(self):
        """Calcula los indicadores generales del reporte."""

        cantidad = len(self.resultados)

        total = sum(
            float(registro["total"])
            for registro in self.resultados
        )

        promedio = total / cantidad if cantidad else 0

        self.etiqueta_cantidad.configure(
            text=f"Productos registrados: {cantidad}"
        )

        self.etiqueta_total.configure(
            text=f"Total vendido: ${total:,.0f} COP"
        )

        self.etiqueta_promedio.configure(
            text=f"Promedio por venta: ${promedio:,.0f} COP"
        )

    def mostrar_detalle(self):
        """Muestra una fila por sucursal y fecha; los productos quedan dentro del detalle."""

        for widget in self.lista_resultados.winfo_children():
            widget.destroy()

        if not self.resultados:
            ctk.CTkLabel(
                self.lista_resultados,
                text="No hay ventas para el periodo seleccionado.",
                font=FUENTES["normal"],
                text_color=COLORES["texto_secundario"]
            ).pack(pady=25)
            return

        grupos = {}
        for registro in self.resultados:
            clave = (registro["sucursal"], registro["fecha"])
            grupos.setdefault(clave, []).append(registro)

        for (sucursal, fecha), productos in grupos.items():
            tarjeta = Tarjeta(self.lista_resultados)
            tarjeta.pack(fill="x", padx=8, pady=6)
            tarjeta.grid_columnconfigure(0, weight=1)

            total = sum(float(p["total"]) for p in productos)
            unidades = sum(float(p["cantidad"]) for p in productos)

            informacion = ctk.CTkFrame(tarjeta, fg_color="transparent")
            informacion.grid(row=0, column=0, padx=15, pady=12, sticky="ew")

            ctk.CTkLabel(
                informacion,
                text=sucursal,
                font=("Segoe UI", 14, "bold"),
                text_color=COLORES["dorado"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                informacion,
                text=f"Fecha: {fecha}  |  {len(productos)} conceptos  |  {unidades:g} unidades",
                font=FUENTES["pequena"],
                text_color=COLORES["texto"]
            ).pack(anchor="w", pady=(4, 0))

            ctk.CTkLabel(
                tarjeta,
                text=f"${total:,.0f} COP",
                font=("Segoe UI", 15, "bold"),
                text_color=COLORES["verde"]
            ).grid(row=0, column=1, padx=15, pady=12)

            BotonSecundario(
                tarjeta,
                "Ver detalle",
                lambda nombre=sucursal, dia=fecha, filas=productos:
                    self.mostrar_detalle_grupo(nombre, dia, filas)
            ).grid(row=0, column=2, padx=(0, 15), pady=12)

    def mostrar_detalle_grupo(self, sucursal, fecha, productos):
        """Abre el detalle de los productos registrados en una sucursal y fecha."""

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle del reporte - {sucursal}")
        ventana.geometry("720x520")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text=f"{sucursal} | {fecha}",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORES["dorado"]
        ).pack(anchor="w", padx=20, pady=(20, 10))

        lista = ctk.CTkScrollableFrame(
            ventana,
            fg_color=COLORES["fondo_secundario"]
        )
        lista.pack(fill="both", expand=True, padx=20, pady=10)

        total_general = 0
        for producto in productos:
            total_general += float(producto["total"])
            fila = Tarjeta(lista)
            fila.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(
                fila,
                text=producto["concepto"],
                font=("Segoe UI", 14, "bold"),
                text_color=COLORES["texto"]
            ).pack(anchor="w", padx=12, pady=(10, 2))

            ctk.CTkLabel(
                fila,
                text=(
                    f"Cantidad: {producto['cantidad']:g}  |  "
                    f"Precio unitario: ${producto['precio_unitario']:,.0f}  |  "
                    f"Total: ${producto['total']:,.0f}"
                ),
                font=FUENTES["pequena"],
                text_color=COLORES["texto_secundario"]
            ).pack(anchor="w", padx=12, pady=(2, 10))

            if producto["observaciones"]:
                ctk.CTkLabel(
                    fila,
                    text=f"Observaciones: {producto['observaciones']}",
                    font=FUENTES["pequena"],
                    text_color=COLORES["texto_secundario"]
                ).pack(anchor="w", padx=12, pady=(0, 8))

        ctk.CTkLabel(
            ventana,
            text=f"TOTAL DE LA SUCURSAL: ${total_general:,.0f} COP",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORES["verde"]
        ).pack(anchor="e", padx=25, pady=(5, 20))

    def exportar_excel(self):
        """Exporta directamente a un libro Excel (.xlsx) con resumen y detalle."""

        if not self.resultados:
            messagebox.showwarning(
                "Sin información",
                "Primero debes consultar un periodo que tenga ventas."
            )
            return

        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
            from openpyxl.utils import get_column_letter
        except ImportError:
            messagebox.showerror(
                "Falta un componente",
                "Para exportar a Excel instala openpyxl desde la consola:\\n\\n"
                "py -3.13 -m pip install openpyxl"
            )
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar reporte de ventas en Excel",
            defaultextension=".xlsx",
            initialfile="reporte_ventas.xlsx",
            filetypes=[("Libro de Excel", "*.xlsx")]
        )

        if not ruta:
            return

        encabezados = [
            "ID", "Fecha", "Sucursal", "Concepto", "Cantidad",
            "Precio unitario (COP)", "Total (COP)", "Observación"
        ]

        try:
            libro = Workbook()
            resumen = libro.active
            resumen.title = "Resumen"
            detalle = libro.create_sheet("Detalle de productos")

            # Estilos del reporte.
            relleno_titulo = PatternFill("solid", fgColor="20242D")
            relleno_encabezado = PatternFill("solid", fgColor="D6AD2C")
            fuente_titulo = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
            fuente_encabezado = Font(name="Calibri", bold=True, color="20242D")
            borde_fino = Side(style="thin", color="D9DDE5")

            # Hoja de resumen: una fila por sucursal y fecha.
            resumen["A1"] = "REPORTE DE VENTAS"
            resumen["A1"].font = fuente_titulo
            resumen["A1"].fill = relleno_titulo
            resumen.merge_cells("A1:E1")
            resumen["A2"] = "Periodo consultado:"
            resumen["B2"] = self.fecha_inicio.get().strip()
            resumen["C2"] = "hasta"
            resumen["D2"] = self.fecha_fin.get().strip()

            grupos = {}
            for registro in self.resultados:
                clave = (registro["sucursal"], registro["fecha"])
                grupos.setdefault(clave, []).append(registro)

            resumen_headers = [
                "Sucursal", "Fecha", "Productos registrados",
                "Unidades", "Total vendido (COP)"
            ]
            fila_encabezado = 4
            for columna, valor in enumerate(resumen_headers, start=1):
                celda = resumen.cell(row=fila_encabezado, column=columna, value=valor)
                celda.font = fuente_encabezado
                celda.fill = relleno_encabezado
                celda.alignment = Alignment(horizontal="center", vertical="center")
                celda.border = Border(bottom=borde_fino)

            fila = fila_encabezado + 1
            for (sucursal, fecha), productos in grupos.items():
                total_grupo = sum(float(item["total"]) for item in productos)
                unidades = sum(float(item["cantidad"]) for item in productos)
                valores = [sucursal, fecha, len(productos), unidades, total_grupo]
                for columna, valor in enumerate(valores, start=1):
                    resumen.cell(row=fila, column=columna, value=valor)
                resumen.cell(row=fila, column=5).number_format = '$#,##0'
                fila += 1

            fila_total = fila + 1
            resumen.cell(row=fila_total, column=1, value="TOTAL GENERAL")
            resumen.cell(row=fila_total, column=3, value=len(self.resultados))
            resumen.cell(
                row=fila_total, column=4,
                value=sum(float(item["cantidad"]) for item in self.resultados)
            )
            resumen.cell(
                row=fila_total, column=5,
                value=sum(float(item["total"]) for item in self.resultados)
            )
            for celda in resumen[fila_total]:
                celda.font = Font(bold=True)
            resumen.cell(row=fila_total, column=5).number_format = '$#,##0'

            # Hoja de detalle: cada producto conserva su propio registro.
            detalle.append(encabezados)
            for registro in self.resultados:
                detalle.append([
                    registro["id"],
                    registro["fecha"],
                    registro["sucursal"],
                    registro["concepto"],
                    float(registro["cantidad"]),
                    float(registro["precio_unitario"]),
                    float(registro["total"]),
                    registro["observaciones"] or ""
                ])

            for hoja in (resumen, detalle):
                hoja.freeze_panes = "A5" if hoja is resumen else "A2"
                # Mostrar los cuadritos de la hoja como en una cuadrícula de Excel.
                hoja.sheet_view.showGridLines = True
                # Bordes finos en las celdas con datos para que la tabla quede delimitada al imprimir.
                for fila_celdas in hoja.iter_rows():
                    for celda in fila_celdas:
                        if celda.value is not None:
                            celda.border = Border(
                                left=Side(style="thin", color="D9DDE5"),
                                right=Side(style="thin", color="D9DDE5"),
                                top=Side(style="thin", color="D9DDE5"),
                                bottom=Side(style="thin", color="D9DDE5")
                            )
                for columna in range(1, hoja.max_column + 1):
                    valores_columna = [
                        str(hoja.cell(row=r, column=columna).value or "")
                        for r in range(1, hoja.max_row + 1)
                    ]
                    ancho = min(max(max((len(v) for v in valores_columna), default=10) + 3, 13), 34)
                    hoja.column_dimensions[get_column_letter(columna)].width = ancho

            for celda in detalle[1]:
                celda.font = fuente_encabezado
                celda.fill = relleno_encabezado
                celda.alignment = Alignment(horizontal="center", vertical="center")
                celda.border = Border(bottom=borde_fino)

            # Centrar el encabezado y el contenido de la columna Observación.
            for fila_numero in range(1, detalle.max_row + 1):
                detalle.cell(fila_numero, 8).alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True
                )

            for numero_fila in range(2, detalle.max_row + 1):
                detalle.cell(numero_fila, 6).number_format = '$#,##0'
                detalle.cell(numero_fila, 7).number_format = '$#,##0'
                detalle.cell(numero_fila, 5).number_format = '#,##0.##'

            # Filtro normal de hoja, sin objetos de Tabla de Excel.
            # Esto evita que Excel tenga que reparar partes /xl/tables/table*.xml.
            if detalle.max_row > 1:
                detalle.auto_filter.ref = f"A1:H{detalle.max_row}"

            resumen.freeze_panes = "A5"
            libro.save(ruta)

            messagebox.showinfo(
                "Exportación exitosa",
                "El reporte de Excel se guardó correctamente.\\n\\n"
                f"Archivo: {ruta}\\n"
                "Incluye las hojas «Resumen» y «Detalle de productos»."
            )

        except (OSError, ValueError, TypeError) as error:
            messagebox.showerror(
                "Error de exportación",
                f"No fue posible guardar el reporte de Excel.\\n\\n{error}"
            )

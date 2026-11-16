import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from database import conectar
from interfaz.estilos import COLORES, FUENTES
from interfaz.componentes import (
    Tarjeta, BotonPrincipal, BotonSecundario, CampoTexto,
    EtiquetaCampo, TituloSeccion
)
from servicios.validaciones import convertir_valor_monetario
from servicios.calculos import calcular_total_venta


class VentasFrame(ctk.CTkFrame):
    """Registro de ventas agrupado visualmente por sucursal y fecha."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORES["fondo"], **kwargs)
        self.sucursales = {}
        self.crear_interfaz()
        self.cargar_sucursales()
        self.cargar_ventas()

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(row=0, column=0, padx=25, pady=(20, 10), sticky="ew")
        TituloSeccion(encabezado, "Registro de ventas").pack(anchor="w")
        ctk.CTkLabel(
            encabezado,
            text="Registra productos y consulta el resumen diario de cada sucursal.",
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w", pady=(5, 0))

        self.crear_formulario()

        TituloSeccion(self, "Ventas agrupadas por sucursal y fecha").grid(
            row=2, column=0, padx=25, pady=(15, 10), sticky="w"
        )
        self.lista_ventas = ctk.CTkScrollableFrame(
            self, fg_color=COLORES["fondo_secundario"], corner_radius=10
        )
        self.lista_ventas.grid(row=3, column=0, padx=25, pady=(0, 20), sticky="nsew")

    def crear_formulario(self):
        tarjeta = Tarjeta(self)
        tarjeta.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        tarjeta.grid_columnconfigure((0, 1, 2), weight=1)

        TituloSeccion(tarjeta, "Agregar producto a las ventas del día").grid(
            row=0, column=0, columnspan=3, padx=18, pady=(15, 12), sticky="w"
        )

        EtiquetaCampo(tarjeta, "Sucursal").grid(row=1, column=0, padx=18, sticky="w")
        self.combo_sucursal = ctk.CTkComboBox(
            tarjeta, values=["Cargando sucursales..."], state="readonly", height=38,
            fg_color=COLORES["entrada"], border_color=COLORES["borde"],
            button_color=COLORES["dorado"],
            button_hover_color=COLORES["dorado_oscuro"],
            text_color=COLORES["blanco"], font=FUENTES["normal"]
        )
        self.combo_sucursal.grid(row=2, column=0, padx=18, pady=(5, 12), sticky="ew")

        EtiquetaCampo(tarjeta, "Fecha").grid(row=1, column=1, padx=18, sticky="w")
        self.entrada_fecha = CampoTexto(tarjeta, "AAAA-MM-DD")
        self.entrada_fecha.insert(0, date.today().isoformat())
        self.entrada_fecha.grid(row=2, column=1, padx=18, pady=(5, 12), sticky="ew")

        EtiquetaCampo(tarjeta, "Producto o concepto").grid(row=1, column=2, padx=18, sticky="w")
        self.entrada_concepto = CampoTexto(tarjeta, "Ejemplo: Pantalones")
        self.entrada_concepto.grid(row=2, column=2, padx=18, pady=(5, 12), sticky="ew")

        EtiquetaCampo(tarjeta, "Cantidad").grid(row=3, column=0, padx=18, sticky="w")
        self.entrada_cantidad = CampoTexto(tarjeta, "Ejemplo: 2")
        self.entrada_cantidad.insert(0, "1")
        self.entrada_cantidad.grid(row=4, column=0, padx=18, pady=(5, 12), sticky="ew")

        EtiquetaCampo(tarjeta, "Precio unitario (COP)").grid(row=3, column=1, padx=18, sticky="w")
        self.entrada_precio = CampoTexto(tarjeta, "Ejemplo: 50000")
        self.entrada_precio.grid(row=4, column=1, padx=18, pady=(5, 12), sticky="ew")

        EtiquetaCampo(tarjeta, "Observaciones").grid(row=3, column=2, padx=18, sticky="w")
        self.entrada_observaciones = CampoTexto(tarjeta, "Opcional")
        self.entrada_observaciones.grid(row=4, column=2, padx=18, pady=(5, 12), sticky="ew")

        self.etiqueta_total = ctk.CTkLabel(
            tarjeta, text="TOTAL: $0", font=("Segoe UI", 18, "bold"),
            text_color=COLORES["dorado"]
        )
        self.etiqueta_total.grid(row=5, column=0, padx=18, pady=(5, 15), sticky="w")

        self.entrada_cantidad.bind("<KeyRelease>", self.actualizar_total)
        self.entrada_precio.bind("<KeyRelease>", self.actualizar_total)

        acciones = ctk.CTkFrame(tarjeta, fg_color="transparent")
        acciones.grid(row=5, column=1, columnspan=2, padx=18, pady=(5, 15), sticky="e")
        BotonSecundario(acciones, "Limpiar", self.limpiar_formulario).pack(side="left", padx=5)
        BotonPrincipal(acciones, "Agregar producto", self.guardar_venta).pack(side="left", padx=5)

    def cargar_sucursales(self):
        try:
            with conectar() as conexion:
                registros = conexion.execute("""
                    SELECT id, nombre FROM sucursales
                    WHERE estado = 'Activa' ORDER BY nombre
                """).fetchall()
            self.sucursales = {r["nombre"]: r["id"] for r in registros}
            opciones = list(self.sucursales)
            self.combo_sucursal.configure(
                values=opciones or ["No hay sucursales activas"],
                state="readonly" if opciones else "disabled"
            )
            self.combo_sucursal.set(opciones[0] if opciones else "No hay sucursales activas")
        except Exception as error:
            messagebox.showerror("Error", f"No fue posible cargar las sucursales.\n\n{error}")

    def actualizar_total(self, evento=None):
        try:
            cantidad = float(self.entrada_cantidad.get().strip().replace(",", "."))
            precio = convertir_valor_monetario(self.entrada_precio.get())
            if cantidad <= 0 or precio < 0:
                raise ValueError
            total = calcular_total_venta(cantidad, precio)
            self.etiqueta_total.configure(text=f"TOTAL: ${total:,.0f}")
        except (ValueError, TypeError):
            self.etiqueta_total.configure(text="TOTAL: $0")

    def guardar_venta(self):
        nombre = self.combo_sucursal.get()
        fecha_texto = self.entrada_fecha.get().strip()
        concepto = self.entrada_concepto.get().strip()
        cantidad_texto = self.entrada_cantidad.get().strip()
        precio_texto = self.entrada_precio.get().strip()
        observaciones = self.entrada_observaciones.get().strip()

        if nombre not in self.sucursales:
            messagebox.showwarning("Sucursal requerida", "Primero debes registrar y activar una sucursal.")
            return
        if not all((fecha_texto, concepto, cantidad_texto, precio_texto)):
            messagebox.showwarning("Campos obligatorios", "Completa la fecha, el producto, la cantidad y el precio.")
            return
        try:
            fecha = date.fromisoformat(fecha_texto).isoformat()
            cantidad = float(cantidad_texto.replace(",", "."))
            precio = convertir_valor_monetario(precio_texto)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            total = calcular_total_venta(cantidad, precio)

            with conectar() as conexion:
                conexion.execute("""
                    INSERT INTO ventas
                    (sucursal_id, fecha, concepto, cantidad, precio_unitario, total, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.sucursales[nombre], fecha, concepto, cantidad, precio, total, observaciones))

            messagebox.showinfo(
                "Producto agregado",
                f"{concepto} se agregó a las ventas de {nombre} del {fecha}.\n\n"
                f"Subtotal: ${total:,.0f} COP"
            )
            self.limpiar_formulario()
            self.cargar_ventas()
        except ValueError as error:
            messagebox.showwarning("Datos no válidos", f"Revisa los datos ingresados.\n\n{error}")
        except Exception as error:
            messagebox.showerror("Error al guardar", f"No fue posible registrar el producto.\n\n{error}")

    def cargar_ventas(self):
        for widget in self.lista_ventas.winfo_children():
            widget.destroy()
        try:
            with conectar() as conexion:
                filas = conexion.execute("""
                    SELECT v.id, v.sucursal_id, v.fecha, v.concepto, v.cantidad,
                           v.precio_unitario, v.total, v.observaciones,
                           s.nombre AS sucursal
                    FROM ventas v
                    INNER JOIN sucursales s ON s.id = v.sucursal_id
                    ORDER BY v.fecha DESC, s.nombre, v.id
                """).fetchall()

            grupos = {}
            for fila in filas:
                clave = (fila["sucursal_id"], fila["fecha"], fila["sucursal"])
                grupos.setdefault(clave, []).append(fila)

            if not grupos:
                ctk.CTkLabel(
                    self.lista_ventas, text="Todavía no hay ventas registradas.",
                    font=FUENTES["normal"], text_color=COLORES["texto_secundario"]
                ).pack(pady=25)
                return

            for (sucursal_id, fecha, sucursal), productos in grupos.items():
                self.crear_tarjeta_grupo(sucursal_id, fecha, sucursal, productos)
        except Exception as error:
            messagebox.showerror("Error de consulta", f"No fue posible consultar las ventas.\n\n{error}")

    def crear_tarjeta_grupo(self, sucursal_id, fecha, sucursal, productos):
        tarjeta = Tarjeta(self.lista_ventas)
        tarjeta.pack(fill="x", padx=8, pady=6)
        tarjeta.grid_columnconfigure(0, weight=1)

        total = sum(float(p["total"]) for p in productos)
        unidades = sum(float(p["cantidad"]) for p in productos)
        resumen = ctk.CTkFrame(tarjeta, fg_color="transparent")
        resumen.grid(row=0, column=0, padx=15, pady=12, sticky="ew")

        ctk.CTkLabel(
            resumen, text=sucursal, font=("Segoe UI", 15, "bold"),
            text_color=COLORES["dorado"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            resumen,
            text=f"Fecha: {fecha}  |  {len(productos)} conceptos  |  {unidades:g} unidades",
            font=FUENTES["pequena"], text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            tarjeta, text=f"${total:,.0f} COP", font=("Segoe UI", 16, "bold"),
            text_color=COLORES["verde"]
        ).grid(row=0, column=1, padx=15, pady=12)

        BotonSecundario(
            tarjeta, "Ver detalle",
            lambda sid=sucursal_id, f=fecha, n=sucursal: self.mostrar_detalle(sid, f, n)
        ).grid(row=0, column=2, padx=(0, 15), pady=12)

    def mostrar_detalle(self, sucursal_id, fecha, sucursal):
        with conectar() as conexion:
            productos = conexion.execute("""
                SELECT id, concepto, cantidad, precio_unitario, total, observaciones
                FROM ventas WHERE sucursal_id = ? AND fecha = ?
                ORDER BY id
            """, (sucursal_id, fecha)).fetchall()

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle de ventas - {sucursal}")
        ventana.geometry("760x560")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        ctk.CTkLabel(
            ventana, text=f"{sucursal} | {fecha}",
            font=("Segoe UI", 20, "bold"), text_color=COLORES["dorado"]
        ).pack(anchor="w", padx=20, pady=(20, 5))
        lista = ctk.CTkScrollableFrame(ventana, fg_color=COLORES["fondo_secundario"])
        lista.pack(fill="both", expand=True, padx=20, pady=10)

        total_general = 0
        for p in productos:
            total_general += float(p["total"])
            fila = Tarjeta(lista)
            fila.pack(fill="x", padx=5, pady=5)
            fila.grid_columnconfigure(0, weight=1)
            texto = ctk.CTkFrame(fila, fg_color="transparent")
            texto.grid(row=0, column=0, padx=12, pady=10, sticky="ew")
            ctk.CTkLabel(
                texto, text=p["concepto"], font=("Segoe UI", 14, "bold"),
                text_color=COLORES["texto"]
            ).pack(anchor="w")
            ctk.CTkLabel(
                texto,
                text=f"Cantidad: {p['cantidad']:g}  |  Precio unitario: ${p['precio_unitario']:,.0f}  |  Subtotal: ${p['total']:,.0f}",
                font=FUENTES["pequena"], text_color=COLORES["texto_secundario"]
            ).pack(anchor="w", pady=(3, 0))
            acciones = ctk.CTkFrame(fila, fg_color="transparent")
            acciones.grid(row=0, column=1, padx=8, pady=8)
            BotonSecundario(
                acciones, "Editar",
                lambda venta_id=p["id"], win=ventana: self.editar_venta(venta_id, win)
            ).pack(pady=3)
            BotonSecundario(
                acciones, "Eliminar",
                lambda venta_id=p["id"], win=ventana: self.eliminar_venta(venta_id, win),
                text_color=COLORES["rojo"]
            ).pack(pady=3)

        ctk.CTkLabel(
            ventana, text=f"TOTAL DEL DÍA: ${total_general:,.0f} COP",
            font=("Segoe UI", 18, "bold"), text_color=COLORES["verde"]
        ).pack(anchor="e", padx=25, pady=(5, 20))

    def editar_venta(self, venta_id, ventana_detalle):
        with conectar() as conexion:
            venta = conexion.execute(
                "SELECT * FROM ventas WHERE id = ?", (venta_id,)
            ).fetchone()
        if not venta:
            messagebox.showwarning("Registro no encontrado", "Esta línea de venta ya no existe.")
            ventana_detalle.destroy()
            self.cargar_ventas()
            return

        dialogo = ctk.CTkToplevel(ventana_detalle)
        dialogo.title("Editar producto")
        dialogo.geometry("430x430")
        dialogo.transient(ventana_detalle)
        dialogo.grab_set()

        campos = {}
        datos = [
            ("Producto o concepto", "concepto", venta["concepto"]),
            ("Cantidad", "cantidad", str(venta["cantidad"])),
            ("Precio unitario", "precio_unitario", str(venta["precio_unitario"])),
            ("Observaciones", "observaciones", venta["observaciones"] or "")
        ]
        for etiqueta, clave, valor in datos:
            ctk.CTkLabel(dialogo, text=etiqueta).pack(anchor="w", padx=20, pady=(12, 2))
            entrada = CampoTexto(dialogo, etiqueta)
            entrada.pack(fill="x", padx=20)
            entrada.insert(0, valor)
            campos[clave] = entrada

        def guardar():
            try:
                concepto = campos["concepto"].get().strip()
                cantidad = float(campos["cantidad"].get().strip().replace(",", "."))
                precio = convertir_valor_monetario(campos["precio_unitario"].get())
                observaciones = campos["observaciones"].get().strip()
                if not concepto:
                    raise ValueError("El producto o concepto no puede estar vacío.")
                if cantidad <= 0 or precio < 0:
                    raise ValueError("La cantidad debe ser mayor que cero y el precio no puede ser negativo.")
                total = calcular_total_venta(cantidad, precio)
                with conectar() as conexion:
                    conexion.execute("""
                        UPDATE ventas SET concepto=?, cantidad=?, precio_unitario=?,
                        total=?, observaciones=? WHERE id=?
                    """, (concepto, cantidad, precio, total, observaciones, venta_id))
                dialogo.destroy()
                ventana_detalle.destroy()
                self.cargar_ventas()
                messagebox.showinfo("Actualizado", "El producto fue actualizado correctamente.")
            except ValueError as error:
                messagebox.showwarning("Datos no válidos", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"No fue posible actualizar el producto.\n\n{error}")

        BotonPrincipal(dialogo, "Guardar cambios", guardar).pack(pady=22)

    def eliminar_venta(self, venta_id, ventana_detalle):
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar este producto de las ventas del día?"):
            return
        try:
            with conectar() as conexion:
                conexion.execute("DELETE FROM ventas WHERE id = ?", (venta_id,))
            ventana_detalle.destroy()
            self.cargar_ventas()
            messagebox.showinfo("Eliminado", "El producto fue eliminado del registro.")
        except Exception as error:
            messagebox.showerror("Error", f"No fue posible eliminar el producto.\n\n{error}")

    def limpiar_formulario(self):
        self.entrada_fecha.delete(0, "end")
        self.entrada_fecha.insert(0, date.today().isoformat())
        self.entrada_concepto.delete(0, "end")
        self.entrada_cantidad.delete(0, "end")
        self.entrada_cantidad.insert(0, "1")
        self.entrada_precio.delete(0, "end")
        self.entrada_observaciones.delete(0, "end")
        self.etiqueta_total.configure(text="TOTAL: $0")

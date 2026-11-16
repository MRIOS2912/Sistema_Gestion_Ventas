import customtkinter as ctk
from tkinter import messagebox

from database import conectar, RUTA_BD
from interfaz.estilos import COLORES, FUENTES
from interfaz.componentes import (
    Tarjeta,
    BotonPrincipal,
    BotonSecundario,
    CampoTexto,
    EtiquetaCampo,
    TituloSeccion
)


class SucursalesFrame(ctk.CTkFrame):
    """Pantalla para registrar, consultar y administrar sucursales."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORES["fondo"],
            **kwargs
        )

        self.sucursal_seleccionada = None
        self.crear_interfaz()
        self.cargar_sucursales()

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(
            row=0, column=0, padx=25, pady=(20, 10), sticky="ew"
        )

        TituloSeccion(
            encabezado, "Gestión de sucursales"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Registra y administra los establecimientos de tu empresa.",
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w", pady=(5, 0))

        self.crear_formulario()

        self.contenedor_lista = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.contenedor_lista.grid(
            row=2, column=0, padx=25, pady=(15, 20), sticky="nsew"
        )
        self.contenedor_lista.grid_columnconfigure(0, weight=1)
        self.contenedor_lista.grid_rowconfigure(1, weight=1)

        self.titulo_lista = TituloSeccion(
            self.contenedor_lista, "Sucursales registradas"
        )
        self.titulo_lista.grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        self.lista = ctk.CTkScrollableFrame(
            self.contenedor_lista,
            fg_color=COLORES["fondo_secundario"],
            corner_radius=10
        )
        self.lista.grid(row=1, column=0, sticky="nsew")

        # Muestra la ruta real para detectar si se está ejecutando
        # otra copia del proyecto o utilizando otra base de datos.
        self.etiqueta_bd = ctk.CTkLabel(
            self.contenedor_lista,
            text=f"Base de datos activa: {RUTA_BD}",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"],
            anchor="w",
            wraplength=950
        )
        self.etiqueta_bd.grid(
            row=2, column=0, sticky="w", pady=(6, 0)
        )

    def crear_formulario(self):
        tarjeta = Tarjeta(self)
        tarjeta.grid(
            row=1, column=0, padx=25, pady=10, sticky="ew"
        )
        tarjeta.grid_columnconfigure((0, 1), weight=1)

        self.titulo_formulario = TituloSeccion(
            tarjeta, "Datos de la sucursal"
        )
        self.titulo_formulario.grid(
            row=0, column=0, columnspan=2,
            padx=18, pady=(15, 12), sticky="w"
        )

        EtiquetaCampo(
            tarjeta, "Nombre de la sucursal"
        ).grid(row=1, column=0, padx=18, sticky="w")

        self.entrada_nombre = CampoTexto(
            tarjeta, "Ejemplo: Sucursal Centro"
        )
        self.entrada_nombre.grid(
            row=2, column=0, padx=18, pady=(5, 12), sticky="ew"
        )

        EtiquetaCampo(
            tarjeta, "Dirección"
        ).grid(row=1, column=1, padx=18, sticky="w")

        self.entrada_direccion = CampoTexto(
            tarjeta, "Dirección de la sucursal"
        )
        self.entrada_direccion.grid(
            row=2, column=1, padx=18, pady=(5, 12), sticky="ew"
        )

        EtiquetaCampo(
            tarjeta, "Teléfono"
        ).grid(row=3, column=0, padx=18, sticky="w")

        self.entrada_telefono = CampoTexto(
            tarjeta, "Número de contacto"
        )
        self.entrada_telefono.grid(
            row=4, column=0, padx=18, pady=(5, 12), sticky="ew"
        )

        self.boton_guardar = BotonPrincipal(
            tarjeta, "Registrar sucursal", self.guardar_sucursal
        )
        self.boton_guardar.grid(
            row=5, column=0, padx=18, pady=(5, 16), sticky="ew"
        )

        self.boton_cancelar = BotonSecundario(
            tarjeta, "Limpiar formulario", self.limpiar_formulario
        )
        self.boton_cancelar.grid(
            row=5, column=1, padx=18, pady=(5, 16), sticky="ew"
        )

    def guardar_sucursal(self):
        nombre = self.entrada_nombre.get().strip()
        direccion = self.entrada_direccion.get().strip()
        telefono = self.entrada_telefono.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Campo obligatorio",
                "Debes escribir el nombre de la sucursal."
            )
            self.entrada_nombre.focus()
            return

        try:
            with conectar() as conexion:
                if self.sucursal_seleccionada is None:
                    # INSERT agrega un registro nuevo; no reemplaza los anteriores.
                    conexion.execute("""
                        INSERT INTO sucursales (nombre, direccion, telefono)
                        VALUES (?, ?, ?)
                    """, (nombre, direccion, telefono))
                    mensaje = "La sucursal fue registrada correctamente."
                else:
                    cursor = conexion.execute("""
                        UPDATE sucursales
                        SET nombre = ?, direccion = ?, telefono = ?
                        WHERE id = ?
                    """, (
                        nombre,
                        direccion,
                        telefono,
                        self.sucursal_seleccionada
                    ))

                    if cursor.rowcount != 1:
                        raise RuntimeError(
                            "La sucursal que intentas editar ya no existe. "
                            "Actualiza la lista e inténtalo nuevamente."
                        )
                    mensaje = "Los cambios de la sucursal se guardaron correctamente."

            self.limpiar_formulario()
            self.cargar_sucursales()
            messagebox.showinfo("Operación exitosa", mensaje)

        except Exception as error:
            mensaje_error = str(error)
            if "UNIQUE constraint failed" in mensaje_error:
                mensaje_error = (
                    "Ya existe una sucursal con ese nombre. "
                    "Escribe un nombre diferente."
                )
            messagebox.showerror(
                "No se pudo guardar",
                f"{mensaje_error}\n\nBase de datos utilizada:\n{RUTA_BD}"
            )

    def cargar_sucursales(self):
        """Vuelve a consultar la tabla completa y reconstruye la lista."""
        for widget in self.lista.winfo_children():
            widget.destroy()

        try:
            with conectar() as conexion:
                sucursales = conexion.execute("""
                    SELECT id, nombre, direccion, telefono, estado
                    FROM sucursales
                    ORDER BY id ASC
                """).fetchall()

            cantidad = len(sucursales)
            self.titulo_lista.configure(
                text=f"Sucursales registradas ({cantidad})"
            )

            if not sucursales:
                ctk.CTkLabel(
                    self.lista,
                    text="Todavía no hay sucursales registradas.",
                    font=FUENTES["normal"],
                    text_color=COLORES["texto_secundario"]
                ).pack(pady=30)
                return

            for sucursal in sucursales:
                self.crear_tarjeta_sucursal(sucursal)

        except Exception as error:
            messagebox.showerror(
                "Error al consultar sucursales",
                f"No fue posible cargar la lista.\n\n{error}\n\n"
                f"Base de datos utilizada:\n{RUTA_BD}"
            )

    def crear_tarjeta_sucursal(self, sucursal):
        tarjeta = Tarjeta(self.lista)
        tarjeta.pack(fill="x", padx=8, pady=7)
        tarjeta.grid_columnconfigure(0, weight=1)

        informacion = ctk.CTkFrame(
            tarjeta, fg_color="transparent"
        )
        informacion.grid(
            row=0, column=0, padx=15, pady=12, sticky="ew"
        )

        ctk.CTkLabel(
            informacion,
            text=sucursal["nombre"],
            font=("Segoe UI", 15, "bold"),
            text_color=COLORES["dorado"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            informacion,
            text=f"Dirección: {sucursal['direccion'] or 'No registrada'}",
            font=FUENTES["pequena"],
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            informacion,
            text=f"Teléfono: {sucursal['telefono'] or 'No registrado'}",
            font=FUENTES["pequena"],
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(3, 0))

        estado = sucursal["estado"]
        color_estado = (
            COLORES["verde"] if estado == "Activa" else COLORES["rojo"]
        )
        ctk.CTkLabel(
            informacion,
            text=f"Estado: {estado}",
            font=FUENTES["pequena"],
            text_color=color_estado
        ).pack(anchor="w", pady=(3, 0))

        acciones = ctk.CTkFrame(
            tarjeta, fg_color="transparent"
        )
        acciones.grid(row=0, column=1, padx=12, pady=12)

        BotonSecundario(
            acciones,
            "Editar",
            lambda registro=sucursal: self.editar_sucursal(registro),
            width=120
        ).pack(pady=3)

        BotonSecundario(
            acciones,
            "Activar / Desactivar",
            lambda registro=sucursal: self.cambiar_estado(registro),
            width=145
        ).pack(pady=3)

        BotonSecundario(
            acciones,
            "Eliminar",
            lambda registro=sucursal: self.eliminar_sucursal(registro),
            width=120,
            text_color=COLORES["rojo"]
        ).pack(pady=3)

    def editar_sucursal(self, sucursal):
        """Carga el registro elegido y cambia el formulario a modo edición."""
        self.sucursal_seleccionada = int(sucursal["id"])

        self.entrada_nombre.delete(0, "end")
        self.entrada_nombre.insert(0, sucursal["nombre"] or "")

        self.entrada_direccion.delete(0, "end")
        self.entrada_direccion.insert(0, sucursal["direccion"] or "")

        self.entrada_telefono.delete(0, "end")
        self.entrada_telefono.insert(0, sucursal["telefono"] or "")

        self.titulo_formulario.configure(
            text=f"EDITANDO SUCURSAL: {sucursal['nombre']}"
        )
        self.boton_guardar.configure(text="Guardar cambios")
        self.boton_cancelar.configure(text="Cancelar edición")
        self.entrada_nombre.focus_set()

        # Lleva visualmente la atención al formulario.
        self.titulo_formulario.update_idletasks()

    def cambiar_estado(self, sucursal):
        estado_actual = sucursal["estado"]
        nuevo_estado = "Inactiva" if estado_actual == "Activa" else "Activa"

        confirmar = messagebox.askyesno(
            "Confirmar cambio",
            f"¿Deseas cambiar el estado de {sucursal['nombre']} "
            f"a {nuevo_estado}?"
        )
        if not confirmar:
            return

        try:
            with conectar() as conexion:
                cursor = conexion.execute("""
                    UPDATE sucursales SET estado = ? WHERE id = ?
                """, (nuevo_estado, sucursal["id"]))

                if cursor.rowcount != 1:
                    raise RuntimeError("No se encontró la sucursal seleccionada.")

            self.cargar_sucursales()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cambiar el estado.\n\n{error}"
            )

    def eliminar_sucursal(self, sucursal):
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás segura de eliminar la sucursal {sucursal['nombre']}?"
        )
        if not confirmar:
            return

        try:
            with conectar() as conexion:
                ventas = conexion.execute("""
                    SELECT COUNT(*) FROM ventas WHERE sucursal_id = ?
                """, (sucursal["id"],)).fetchone()[0]

                if ventas:
                    messagebox.showwarning(
                        "No se puede eliminar",
                        "Esta sucursal tiene ventas registradas. "
                        "Puedes desactivarla en lugar de eliminarla."
                    )
                    return

                conexion.execute(
                    "DELETE FROM sucursales WHERE id = ?",
                    (sucursal["id"],)
                )

            if self.sucursal_seleccionada == sucursal["id"]:
                self.limpiar_formulario()

            self.cargar_sucursales()
            messagebox.showinfo(
                "Eliminación exitosa",
                "La sucursal fue eliminada correctamente."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible eliminar la sucursal.\n\n{error}"
            )

    def limpiar_formulario(self):
        """Cancela la edición o deja el formulario listo para un registro nuevo."""
        self.entrada_nombre.delete(0, "end")
        self.entrada_direccion.delete(0, "end")
        self.entrada_telefono.delete(0, "end")

        self.sucursal_seleccionada = None
        self.titulo_formulario.configure(text="Datos de la sucursal")
        self.boton_guardar.configure(text="Registrar sucursal")
        self.boton_cancelar.configure(text="Limpiar formulario")

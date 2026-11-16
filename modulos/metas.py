
import customtkinter as ctk
from tkinter import messagebox
from datetime import date

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
from database import convertir_valor_monetario
from servicios.calculos import (
    calcular_porcentaje,
    calcular_faltante_meta,
    calcular_excedente_meta,
    obtener_estado_meta
)


class MetasFrame(ctk.CTkFrame):
    """Módulo para administrar y consultar metas de ventas."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORES["fondo"],
            **kwargs
        )

        self.sucursales = {}
        self.crear_interfaz()
        self.cargar_sucursales()
        self.cargar_metas()

    def crear_interfaz(self):
        """Construye la pantalla de control de metas."""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

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
            "Control de metas"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Define objetivos y supervisa el cumplimiento de ventas.",
            font=FUENTES["normal"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w", pady=(5, 0))

        self.crear_formulario()

        TituloSeccion(
            self,
            "Seguimiento de metas"
        ).grid(
            row=2,
            column=0,
            padx=25,
            pady=(6, 6),
            sticky="w"
        )

        self.lista_metas = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORES["fondo_secundario"],
            corner_radius=10
        )
        self.lista_metas.grid(
            row=3,
            column=0,
            padx=25,
            pady=(0, 14),
            sticky="nsew"
        )

    def crear_formulario(self):
        """Crea el formulario para registrar metas."""

        tarjeta = Tarjeta(self)
        tarjeta.grid(
            row=1,
            column=0,
            padx=25,
            pady=6,
            sticky="ew"
        )

        tarjeta.grid_columnconfigure((0, 1, 2), weight=1)

        TituloSeccion(
            tarjeta,
            "Configurar una meta"
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
            values=["Cargando..."],
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

        EtiquetaCampo(
            tarjeta,
            "Periodo"
        ).grid(
            row=1,
            column=1,
            padx=18,
            sticky="w"
        )

        self.entrada_periodo = CampoTexto(
            tarjeta,
            "Ejemplo: 2026-11"
        )
        self.entrada_periodo.insert(
            0,
            date.today().strftime("%Y-%m")
        )
        self.entrada_periodo.grid(
            row=2,
            column=1,
            padx=18,
            pady=(5, 12),
            sticky="ew"
        )

        EtiquetaCampo(
            tarjeta,
            "Valor de la meta (COP)"
        ).grid(
            row=1,
            column=2,
            padx=18,
            sticky="w"
        )

        self.entrada_meta = CampoTexto(
            tarjeta,
            "Ejemplo: 3500000"
        )
        self.entrada_meta.grid(
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
            "Limpiar",
            self.limpiar_formulario
        ).pack(side="left", padx=5)

        BotonPrincipal(
            acciones,
            "Guardar meta",
            self.guardar_meta
        ).pack(side="left", padx=5)

    def cargar_sucursales(self):
        """Carga las sucursales disponibles."""

        try:
            with conectar() as conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT id, nombre
                    FROM sucursales
                    WHERE estado = 'Activa'
                    ORDER BY nombre
                """)

                registros = cursor.fetchall()

            self.sucursales = {
                registro["nombre"]: registro["id"]
                for registro in registros
            }

            opciones = list(self.sucursales.keys())

            if opciones:
                self.combo_sucursal.configure(
                    values=opciones,
                    state="readonly"
                )
                self.combo_sucursal.set(opciones[0])
            else:
                self.combo_sucursal.configure(
                    values=["No hay sucursales activas"],
                    state="disabled"
                )
                self.combo_sucursal.set("No hay sucursales activas")

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar las sucursales.\n\n{error}"
            )

    def validar_periodo(self, periodo):
        """Comprueba que el periodo tenga el formato AAAA-MM."""

        try:
            fecha = date.fromisoformat(f"{periodo}-01")
            return fecha.strftime("%Y-%m") == periodo
        except ValueError:
            return False

    def guardar_meta(self):
        """Registra o actualiza la meta de una sucursal."""

        nombre_sucursal = self.combo_sucursal.get()
        periodo = self.entrada_periodo.get().strip()
        valor_texto = self.entrada_meta.get().strip()

        if nombre_sucursal not in self.sucursales:
            messagebox.showwarning(
                "Sucursal requerida",
                "Debes registrar y activar una sucursal primero."
            )
            return

        if not self.validar_periodo(periodo):
            messagebox.showwarning(
                "Periodo no válido",
                "Utiliza el formato AAAA-MM. Ejemplo: 2026-11."
            )
            return

        try:
            valor_meta = convertir_valor_monetario(valor_texto)

            if valor_meta <= 0:
                messagebox.showwarning(
                    "Meta no válida",
                    "El valor de la meta debe ser mayor que cero."
                )
                return

            sucursal_id = self.sucursales[nombre_sucursal]

            with conectar() as conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT id
                    FROM metas
                    WHERE sucursal_id = ?
                    AND periodo = ?
                """, (sucursal_id, periodo))

                existente = cursor.fetchone()

                if existente:
                    cursor.execute("""
                        UPDATE metas
                        SET valor_meta = ?
                        WHERE id = ?
                    """, (valor_meta, existente["id"]))

                    mensaje = "La meta fue actualizada correctamente."

                else:
                    cursor.execute("""
                        INSERT INTO metas (
                            sucursal_id,
                            periodo,
                            valor_meta
                        )
                        VALUES (?, ?, ?)
                    """, (sucursal_id, periodo, valor_meta))

                    mensaje = "La meta fue registrada correctamente."

            messagebox.showinfo(
                "Operación exitosa",
                mensaje
            )

            self.limpiar_formulario()
            self.cargar_metas()

        except ValueError as error:
            messagebox.showwarning(
                "Valor no válido",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible guardar la meta.\n\n{error}"
            )

    def cargar_metas(self):
        """Consulta las metas y calcula el cumplimiento."""

        for widget in self.lista_metas.winfo_children():
            widget.destroy()

        try:
            with conectar() as conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT
                        metas.id,
                        metas.sucursal_id,
                        metas.periodo,
                        metas.valor_meta,
                        sucursales.nombre AS sucursal,
                        COALESCE(SUM(
                            CASE
                                WHEN strftime(
                                    '%Y-%m',
                                    ventas.fecha
                                ) = metas.periodo
                                THEN ventas.total
                                ELSE 0
                            END
                        ), 0) AS ventas_realizadas
                    FROM metas
                    INNER JOIN sucursales
                        ON metas.sucursal_id = sucursales.id
                    LEFT JOIN ventas
                        ON ventas.sucursal_id = metas.sucursal_id
                    GROUP BY
                        metas.id,
                        metas.sucursal_id,
                        metas.periodo,
                        metas.valor_meta,
                        sucursales.nombre
                    ORDER BY metas.periodo DESC, sucursales.nombre
                """)

                metas = cursor.fetchall()

            if not metas:
                ctk.CTkLabel(
                    self.lista_metas,
                    text="Todavía no hay metas registradas.",
                    font=FUENTES["normal"],
                    text_color=COLORES["texto_secundario"]
                ).pack(pady=25)
                return

            for meta in metas:
                self.crear_tarjeta_meta(meta)

        except Exception as error:
            messagebox.showerror(
                "Error de consulta",
                f"No fue posible cargar las metas.\n\n{error}"
            )

    def crear_tarjeta_meta(self, meta):
        """Construye una tarjeta con el avance de una meta."""

        valor_meta = float(meta["valor_meta"])
        ventas = float(meta["ventas_realizadas"])

        porcentaje = calcular_porcentaje(ventas, valor_meta)
        faltante = calcular_faltante_meta(ventas, valor_meta)
        excedente = calcular_excedente_meta(ventas, valor_meta)

        estado = obtener_estado_meta(ventas, valor_meta)

        if porcentaje >= 100:
            color = COLORES["verde"]
        elif porcentaje >= 75:
            color = COLORES["dorado"]
        else:
            color = COLORES["rojo"]

        tarjeta = Tarjeta(self.lista_metas)
        tarjeta.pack(
            fill="x",
            padx=8,
            pady=7
        )

        tarjeta.grid_columnconfigure(0, weight=1)

        informacion = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )
        informacion.grid(
            row=0,
            column=0,
            padx=18,
            pady=14,
            sticky="ew"
        )

        ctk.CTkLabel(
            informacion,
            text=f"{meta['sucursal']} - {meta['periodo']}",
            font=("Segoe UI", 15, "bold"),
            text_color=COLORES["dorado"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            informacion,
            text=f"Meta: ${valor_meta:,.0f} COP",
            font=FUENTES["normal"],
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(6, 0))

        ctk.CTkLabel(
            informacion,
            text=f"Ventas realizadas: ${ventas:,.0f} COP",
            font=FUENTES["normal"],
            text_color=COLORES["texto"]
        ).pack(anchor="w", pady=(4, 0))

        barra = ctk.CTkProgressBar(
            informacion,
            height=12,
            progress_color=color,
            fg_color=COLORES["borde"]
        )
        barra.pack(fill="x", pady=(12, 5))
        barra.set(min(porcentaje / 100, 1))

        ctk.CTkLabel(
            informacion,
            text=f"Cumplimiento: {porcentaje:.1f}%",
            font=("Segoe UI", 12, "bold"),
            text_color=color
        ).pack(anchor="w")

        if porcentaje >= 100:
            detalle = f"Meta superada por ${excedente:,.0f} COP"
        else:
            detalle = f"Faltan ${faltante:,.0f} COP para alcanzar la meta"

        ctk.CTkLabel(
            informacion,
            text=f"{estado} | {detalle}",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"]
        ).pack(anchor="w", pady=(5, 0))

        BotonSecundario(
            tarjeta,
            "Eliminar",
            lambda identificador=meta["id"]: self.eliminar_meta(
                identificador
            ),
            width=90,
            text_color=COLORES["rojo"]
        ).grid(
            row=0,
            column=1,
            padx=18,
            pady=15
        )

    def eliminar_meta(self, identificador):
        """Elimina una meta después de confirmar."""

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Deseas eliminar esta meta?"
        )

        if not confirmar:
            return

        try:
            with conectar() as conexion:
                conexion.execute(
                    "DELETE FROM metas WHERE id = ?",
                    (identificador,)
                )

            messagebox.showinfo(
                "Meta eliminada",
                "La meta fue eliminada correctamente."
            )

            self.cargar_metas()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible eliminar la meta.\n\n{error}"
            )

    def limpiar_formulario(self):
        """Restablece los campos del formulario."""

        self.entrada_periodo.delete(0, "end")
        self.entrada_periodo.insert(
            0,
            date.today().strftime("%Y-%m")
        )

        self.entrada_meta.delete(0, "end")

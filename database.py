"""
Configuracion y acceso a la base de datos del Sistema de Gestion de Ventas.

Este archivo define el esquema unico utilizado por todos los modulos.
La base de datos se crea con la estructura completa cuando no existe.
"""
import os
import sys
import sqlite3
from contextlib import contextmanager


if getattr(sys, "frozen", False):
    DIRECTORIO_PROYECTO = os.path.dirname(sys.executable)
else:
    DIRECTORIO_PROYECTO = os.path.dirname(os.path.abspath(__file__))

DIRECTORIO_BD = os.path.join(DIRECTORIO_PROYECTO, "base_datos")
RUTA_BD = os.path.join(DIRECTORIO_BD, "ventas.db")


def crear_directorio_bd():
    """Crea la carpeta de almacenamiento de la base de datos."""
    os.makedirs(DIRECTORIO_BD, exist_ok=True)


@contextmanager
def conectar():
    """
    Abre una conexion SQLite con claves foraneas activadas.

    Uso:
        with conectar() as conexion:
            conexion.execute(...)
    """
    crear_directorio_bd()
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")

    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def inicializar_base_datos():
    """
    Crea el esquema definitivo del sistema.

    Importante: CREATE TABLE IF NOT EXISTS no transforma tablas antiguas.
    Esta funcion esta destinada a una base de datos nueva con este esquema.
    """
    crear_directorio_bd()

    with conectar() as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sucursales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL COLLATE NOCASE UNIQUE,
                direccion TEXT NOT NULL DEFAULT '',
                telefono TEXT NOT NULL DEFAULT '',
                estado TEXT NOT NULL DEFAULT 'Activa'
                    CHECK (estado IN ('Activa', 'Inactiva')),
                fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sucursal_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                concepto TEXT NOT NULL,
                cantidad REAL NOT NULL DEFAULT 1 CHECK (cantidad > 0),
                precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),
                total REAL NOT NULL CHECK (total >= 0),
                observaciones TEXT NOT NULL DEFAULT '',
                fecha_registro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sucursal_id)
                    REFERENCES sucursales(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sucursal_id INTEGER NOT NULL,
                periodo TEXT NOT NULL,
                valor_meta REAL NOT NULL CHECK (valor_meta > 0),
                fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (sucursal_id, periodo),
                FOREIGN KEY (sucursal_id)
                    REFERENCES sucursales(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL COLLATE NOCASE UNIQUE,
                contrasena TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'Administrador',
                estado TEXT NOT NULL DEFAULT 'Activo'
                    CHECK (estado IN ('Activo', 'Inactivo'))
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ventas_fecha
            ON ventas(fecha)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ventas_sucursal
            ON ventas(sucursal_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metas_periodo
            ON metas(periodo)
        """)


def obtener_tablas():
    """Devuelve los nombres de las tablas propias del sistema."""
    with conectar() as conexion:
        filas = conexion.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()
        return [fila["name"] for fila in filas]


def ejecutar_consulta(sql, parametros=()):
    """Ejecuta una consulta y devuelve todas las filas."""
    with conectar() as conexion:
        return conexion.execute(sql, parametros).fetchall()


def ejecutar_insercion(sql, parametros=()):
    """Ejecuta una insercion y devuelve el identificador generado."""
    with conectar() as conexion:
        cursor = conexion.execute(sql, parametros)
        return cursor.lastrowid


def ejecutar_actualizacion(sql, parametros=()):
    """Ejecuta una actualizacion o eliminacion y devuelve filas afectadas."""
    with conectar() as conexion:
        cursor = conexion.execute(sql, parametros)
        return cursor.rowcount


def convertir_valor_monetario(valor):
    """
    Convierte valores como 500000, 500.000, $500.000 y 500.000,50
    a un numero decimal.
    """
    if valor is None:
        return 0.0

    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip().upper()
    texto = texto.replace("COP", "").replace("$", "").replace(" ", "")

    if not texto:
        return 0.0

    if "," in texto and "." in texto:
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        partes = texto.split(",")
        if len(partes[-1]) in (1, 2):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "." in texto:
        partes = texto.split(".")
        if len(partes) > 1 and len(partes[-1]) == 3:
            texto = texto.replace(".", "")

    try:
        return float(texto)
    except ValueError as error:
        raise ValueError(f"Valor monetario no valido: {valor}") from error


import os
from pathlib import Path

# ==========================================
# CONFIGURACION GENERAL DEL PROYECTO
# ==========================================

BASE = Path(__file__).resolve().parent

CARPETAS = [
    "base_datos",
    "modulos",
    "interfaz",
    "servicios",
    "recursos",
    "recursos/imagenes",
    "recursos/iconos",
    "reportes_generados",
    "copias_seguridad"
]

ARCHIVOS = [
    "modulos/__init__.py",
    "modulos/sucursales.py",
    "modulos/ventas.py",
    "modulos/consultas.py",
    "modulos/metas.py",
    "modulos/reportes.py",

    "interfaz/__init__.py",
    "interfaz/menu.py",
    "interfaz/componentes.py",
    "interfaz/estilos.py",

    "servicios/__init__.py",
    "servicios/calculos.py",
    "servicios/validaciones.py",
    "servicios/exportaciones.py"
]

# ==========================================
# CREAR CARPETAS
# ==========================================

def crear_carpetas():
    print("\nCREANDO ESTRUCTURA DEL PROYECTO")
    print("=" * 45)

    for carpeta in CARPETAS:
        ruta = BASE / carpeta
        ruta.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Carpeta: {carpeta}")

# ==========================================
# CREAR ARCHIVOS
# ==========================================

def crear_archivos():
    print("\nPREPARANDO ARCHIVOS")
    print("=" * 45)

    for archivo in ARCHIVOS:
        ruta = BASE / archivo

        if not ruta.exists():
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_text("", encoding="utf-8")
            print(f"[CREADO] {archivo}")
        else:
            print(f"[CONSERVADO] {archivo}")

# ==========================================
# VERIFICAR ESTRUCTURA
# ==========================================

def verificar_estructura():
    print("\nVERIFICACION FINAL")
    print("=" * 45)

    for carpeta in CARPETAS:
        ruta = BASE / carpeta

        if ruta.exists():
            print(f"[OK] {carpeta}")
        else:
            print(f"[ERROR] {carpeta}")

    print("\nESTRUCTURA DEL PROYECTO PREPARADA")
    print("Sistema de Gestion de Ventas")

# ==========================================
# EJECUCION
# ==========================================

if __name__ == "__main__":
    crear_carpetas()
    crear_archivos()
    verificar_estructura()

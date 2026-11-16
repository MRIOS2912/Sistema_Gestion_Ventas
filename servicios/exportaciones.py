
import csv
import os
from datetime import datetime
from tkinter import filedialog, messagebox


def exportar_a_csv(datos, encabezados=None, nombre_archivo="reporte_ventas"):
    """
    Exporta una lista de diccionarios a un archivo CSV.
    """
    if not datos:
        messagebox.showwarning(
            "Sin información",
            "No hay datos para exportar."
        )
        return None

    if encabezados is None:
        encabezados = list(datos[0].keys())

    ruta = filedialog.asksaveasfilename(
        title="Guardar reporte CSV",
        defaultextension=".csv",
        initialfile=f"{nombre_archivo}.csv",
        filetypes=[("Archivo CSV", "*.csv")]
    )

    if not ruta:
        return None

    try:
        with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=encabezados,
                extrasaction="ignore",
                delimiter=";"
            )

            escritor.writeheader()
            escritor.writerows(datos)

        messagebox.showinfo(
            "Exportación exitosa",
            f"El archivo se guardó correctamente:\n{ruta}"
        )

        return ruta

    except (OSError, csv.Error) as error:
        messagebox.showerror(
            "Error al exportar",
            f"No fue posible guardar el archivo.\n\nDetalle: {error}"
        )
        return None


def exportar_a_txt(contenido, nombre_archivo="reporte_ventas"):
    """
    Exporta texto a un archivo TXT.
    """
    ruta = filedialog.asksaveasfilename(
        title="Guardar reporte de texto",
        defaultextension=".txt",
        initialfile=f"{nombre_archivo}.txt",
        filetypes=[("Archivo de texto", "*.txt")]
    )

    if not ruta:
        return None

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(str(contenido))

        messagebox.showinfo(
            "Exportación exitosa",
            f"El archivo se guardó correctamente:\n{ruta}"
        )

        return ruta

    except OSError as error:
        messagebox.showerror(
            "Error al exportar",
            f"No fue posible guardar el archivo.\n\nDetalle: {error}"
        )
        return None


def obtener_carpeta_reportes():
    """
    Obtiene la carpeta reportes_generados ubicada en la raíz del proyecto.
    Si no existe, la crea.
    """
    raiz_proyecto = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    carpeta = os.path.join(raiz_proyecto, "reportes_generados")
    os.makedirs(carpeta, exist_ok=True)

    return carpeta


def generar_nombre_reporte(prefijo="reporte"):
    """
    Genera un nombre de archivo con fecha y hora.
    """
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefijo}_{fecha_hora}"

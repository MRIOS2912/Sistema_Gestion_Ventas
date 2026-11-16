# Sistema_Gestion_Ventas
Sistema de Gestión de Ventas desarrollado en Python para la actividad práctica de UNAD
# SISTEMA DE GESTIÓN DE VENTAS

**Aplicación de escritorio desarrollada en Python**

Proyecto académico desarrollado para la actividad práctica del curso **Fundamentos de Algoritmia y Programación** de la Universidad Nacional Abierta y a Distancia (UNAD).

## 1. Descripción del proyecto

El Sistema de Gestión de Ventas es una aplicación de escritorio diseñada para administrar la información comercial de diferentes sucursales. Permite registrar y gestionar sucursales, almacenar operaciones de venta, consultar resultados, controlar metas comerciales y visualizar información mediante indicadores y gráficas.

La aplicación cuenta con una interfaz gráfica y una base de datos local para almacenar la información.

## 2. Funcionalidades principales

- **Sucursales:** registro, consulta, edición y administración de sucursales.
- **Ventas:** registro y administración de operaciones de venta.
- **Consultas:** búsqueda y análisis de información comercial.
- **Metas:** registro y seguimiento de objetivos comerciales.
- **Reportes:** consulta de resultados y presentación de información.
- **Panel principal:** visualización de indicadores generales del sistema.

## 3. Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Lenguaje de programación principal. |
| CustomTkinter | Desarrollo de la interfaz gráfica. |
| SQLite | Administración y almacenamiento de datos. |
| Matplotlib | Generación de gráficas e indicadores visuales. |
| Tkinter | Ventanas de diálogo y selección de archivos. |

## 4. Estructura del proyecto

```text
Sistema_Gestion_Ventas/
│
├── interfaz/
│   ├── componentes.py
│   ├── estilos.py
│   └── menu.py
│
├── modulos/
│   ├── sucursales.py
│   ├── ventas.py
│   ├── consultas.py
│   ├── metas.py
│   └── reportes.py
│
├── servicios/
│   ├── calculos.py
│   ├── validaciones.py
│   └── exportaciones.py
│
├── database.py
├── configurar_proyecto.py
├── main.py
└── Sistema_Gestion_Ventas.spec
```

## 5. Requisitos

- Python instalado.
- Sistema operativo Windows.
- Bibliotecas CustomTkinter y Matplotlib.

## 6. Instalación y ejecución

Clonar el repositorio:

```bash
git clone https://github.com/MRIOS2912/Sistema_Gestion_Ventas.git
```

Ingresar a la carpeta del proyecto:

```bash
cd Sistema_Gestion_Ventas
```

Instalar las dependencias:

```bash
pip install customtkinter matplotlib
```

Ejecutar la aplicación:

```bash
python main.py
```

La base de datos SQLite se inicializa desde el programa y se almacena localmente en la carpeta `base_datos`.

## 7. Organización del código

El proyecto utiliza una organización modular para separar la interfaz gráfica, las operaciones comerciales, el acceso a los datos y los servicios de apoyo.

Esta estructura facilita el mantenimiento del programa y permite identificar la implementación de variables, operadores aritméticos y relacionales, estructuras condicionales, ciclos, acumuladores, contadores y validaciones de datos.

## 8. Autoría académica

**Estudiante:** Charlene Melissa Rios Nelson

**Institución:** Universidad Nacional Abierta y a Distancia – UNAD

**Programa:** Tecnología en Gestión de Analítica y Big Data

**Curso:** Fundamentos de Algoritmia y Programación

**Año:** 2026


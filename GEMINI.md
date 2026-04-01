# Análisis del Proyecto: EL SUPERVISOR (Edu Suite)

Este documento proporciona un resumen técnico y operativo del proyecto **EL SUPERVISOR**, 

## 1. Descripción General del Proyecto

**EL SUPERVISOR**  es una herramienta de interfaz de línea de comandos desarrollada en Python, enfocada en la automatización de procesos robóticos (RPA) para la gestión académica. Su objetivo principal es eliminar la carga administrativa manual mediante la sincronización de datos y el monitoreo en tiempo real de la plataforma blakcboard
### Tecnologías Core:

*   **Lenguaje:** Python 3.11+ (gestionado con `uv`).
*   **Automatización (RPA):** `Playwright` para la interacción con el navegador (Blackboard).
*   **Interfaz de Usuario:** `Rich` para una experiencia de consola visualmente atractiva y con retroalimentación en tiempo real.
*   **Manipulación de Datos:** `Pandas` y `PyArrow` para el procesamiento de archivos Parquet y CSV.
*   **Configuración:** `TOML` para ajustes dinámicos y `python-dotenv` para la gestión de credenciales sensibles.

## 2. Arquitectura y Estructura

El proyecto sigue una estructura modular para separar la lógica de negocio de la automatización:

*   **`bot.py`:** Orquestador principal de la CLI. Define los comandos disponibles.
*   **`src/`:**
    *   `map.py`: Lógica para el comando `map`. Se encarga de autenticarse en Blackboard y extraer el mapeo de IDs de cursos a archivos CSV.
    *   `bb.py`: Lógica para el comando `live`. Monitorea en tiempo real si las clases están siendo grabadas en Blackboard usando Playwright.
*   **`config.toml`:** Centraliza las URLs, selectores CSS de la web y rutas de archivos locales.
*   **`00_data/`:** Almacenamiento de datos de salida (ej. `mapa_ids.csv`).
*   **`01_input/`:** Directorio para insumos y perfiles de navegador (ej. `chrome_profile`).

## 3. Guía de Ejecución

El proyecto utiliza `uv` para la gestión de dependencias y ejecución.

### Configuración Inicial:

1.  **Sincronizar entorno:**
    ```bash
    uv sync
    ```
2.  **Variables de Entorno:** Crear un archivo `.env` en la raíz con las siguientes claves:
    *   `USER_ID_BB`: ID de usuario de Blackboard.
    *   `BB_MAIL`: Correo institucional.
    *   `BB_PASS`: Contraseña de Blackboard.

### Comandos Clave:

*   **Sincronizar IDs de Blackboard:**
    ```bash
    uv run python bot.py map
    ```
    *Genera el archivo `00_data/mapa_ids.csv` necesario para el monitoreo.*

*   **Monitorear asistencia en vivo:**
    ```bash
    uv run python bot.py live
    ```
    *Lee la programación desde un archivo Parquet (definido en `config.toml`) y verifica el estado de las grabaciones en vivo.*

## 4. Convenciones de Desarrollo

*   **Separación de Responsabilidades:** La lógica de RPA debe estar en módulos dentro de `src/`, manteniendo `bot.py` como un orquestador ligero.
*   **Configuración Externa:** Nunca hardcodear selectores o URLs; deben residir en `config.toml`.
*   **Gestión de Sesión:** El bot utiliza un perfil de Chrome persistente (`01_input/chrome_profile`) para evitar logueos constantes y manejar MFA.
*   **Salida de Consola:** Usar las utilidades de `Rich` (`Console`, `Panel`, `Live`, `Table`) para mantener la consistencia visual de la herramienta.
*   **Seguridad:** El archivo `.env` está estrictamente fuera del control de versiones (ignorado en `.gitignore`).

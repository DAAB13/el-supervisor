# 🕵️ EL SUPERVISOR (Edu Suite)

**EL SUPERVISOR** es una herramienta de línea de comandos (CLI) diseñada para la automatización de procesos robóticos (RPA) en la gestión académica. Su objetivo es orquestar y ejecutar tareas repetitivas, como la sincronización de datos y el monitoreo en tiempo real de plataformas educativas.

---

## ✨ Características Principales

*   **Sincronización de Cursos:** Mapea automáticamente los IDs internos de Blackboard para mantener una referencia actualizada.
*   **Monitoreo en Vivo:** Supervisa las aulas virtuales para verificar que las clases se estén grabando correctamente, presentando un estado en tiempo real.
*   **Interfaz Moderna:** Utiliza `Rich` para ofrecer una experiencia de consola visualmente atractiva e informativa.
*   **Configuración Centralizada:** Toda la configuración, como URLs, selectores y rutas, se gestiona desde un único archivo `config.toml`.

## 🛠️ Tecnologías Utilizadas

*   **Core:** Python 3.11+
*   **Gestor de Paquetes:** `uv`
*   **Automatización Web (RPA):** `Playwright`
*   **Interfaz de Consola:** `Rich`
*   **Manejo de Datos:** `Pandas`
*   **Configuración:** `TOML` y `python-dotenv`

## 🚀 Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

1.  **Instalar dependencias:**
    Asegúrate de tener `uv` instalado y luego ejecuta:
    ```bash
    uv sync
    ```

2.  **Crear archivo de entorno:**
    Crea un archivo `.env` en la raíz del proyecto y añade las siguientes credenciales:
    ```ini
    # Credenciales de Blackboard
    USER_ID_BB="tu_id_de_usuario_bb"
    BB_MAIL="tu_correo@institucional.com"
    BB_PASS="tu_contraseña"
    ```

3.  **Revisar la configuración:**
    Abre `config.toml` y ajusta las rutas de archivos, especialmente `parquet_file`, para que apunten a las ubicaciones correctas en tu sistema.

## ⚙️ Guía de Comandos

La herramienta se opera a través del script principal `bot.py`.

### Sincronizar Mapa de Cursos (`map`)

Este comando se conecta a Blackboard, extrae la lista de cursos y guarda un mapeo de IDs en `00_data/mapa_ids.csv`. Es un prerrequisito para el monitoreo.

```bash
uv run python bot.py map
```

### Monitorear Clases en Vivo (`live`)

Inicia un dashboard en la consola que verifica en tiempo real el estado de las grabaciones de las clases programadas para el día actual.

```bash
uv run python bot.py live
```
---
Readme generado por Gemini.

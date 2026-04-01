import os
import re
import pandas as pd
import requests
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pathlib import Path
import tomllib
from rich.console import Console
from rich.panel import Panel

console = Console()
# Ajuste de BASE_DIR: Ahora estamos en src/ (un nivel arriba respecto a src/bot/)
BASE_DIR = Path(__file__).resolve().parent.parent

def run():
    load_dotenv(BASE_DIR / ".env")
    USER_ID_BB = os.getenv("USER_ID_BB")
    BB_MAIL = os.getenv("BB_MAIL")
    BB_PASS = os.getenv("BB_PASS")

    with open(BASE_DIR / "config.toml", "rb") as f:
        config = tomllib.load(f)

    ARCHIVO_SALIDA = BASE_DIR / config['bot_files']['mapa_ids']
    BB_URLS = config['blackboard']['urls']
    BB_SELECTORS = config['blackboard']['selectors']

    if not USER_ID_BB:
        console.print("[bold magenta]❌ ERROR: USER_ID_BB no encontrado en .env[/bold magenta]")
        return

    with sync_playwright() as p:
        console.print("[bold magenta]--- 🎭 INICIANDO AUTENTICACIÓN ---[/bold magenta]")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BB_URLS['login'])
        
        try:
            btn_sup = page.locator("text=Supervisores")
            if btn_sup.is_visible():
                btn_sup.click()

            page.wait_for_selector(BB_SELECTORS['user_input'], timeout=10000)
            page.locator(BB_SELECTORS['user_input']).fill(BB_MAIL)
            page.locator(BB_SELECTORS['pass_input']).fill(BB_PASS)
            page.locator(BB_SELECTORS['login_btn']).click()

            try:
                sel_mfa = BB_SELECTORS['mfa_submit']
                page.wait_for_selector(sel_mfa, state="visible", timeout=15000)
                page.locator(sel_mfa).click()
                console.print("[bold cyan]📲 ¡Acepta en tu celular![/bold cyan]")
            except Exception: pass
            
            page.wait_for_url("**/ultra/stream", timeout=120000)
            console.print("[bold cyan]✅ Acceso concedido.[/bold cyan]")
            
            cookies = context.cookies()
            cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            browser.close()
        except Exception as e:
            console.print(f"[bold magenta]Error en login: {e}[/bold magenta]")
            return

    url_api = BB_URLS['api_memberships'].format(user_id=USER_ID_BB)
    headers = {"Cookie": cookie_string, "User-Agent": "Mozilla/5.0"}

    try:
        with console.status("[bold cyan]📡 Descargando mapa de cursos...", spinner="earth"):
            response = requests.get(url_api, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            lista_cursos = []
            results = data.get('results', [])

            for item in results:
                curso_obj = item.get('course', {})
                nombre_full = curso_obj.get('name', '')
                
                match = re.search(r'(\d{6}\.\d{4})', nombre_full)
                id_nrc = match.group(1) if match else "N/A"

                if curso_obj.get('id'): 
                    lista_cursos.append({
                        "ID": id_nrc,
                        "Nombre_BB": nombre_full,
                        "ID_Interno": curso_obj.get('id'),
                        "ID_Visible": curso_obj.get('courseId')
                    })

            if lista_cursos:
                ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
                df = pd.DataFrame(lista_cursos)
                df.to_csv(ARCHIVO_SALIDA, index=False, sep=';', encoding='latin1')
                console.print(Panel(f"[bold white]🔹 Cursos mapeados: {len(df)}\n💾 Guardado en: {ARCHIVO_SALIDA}[/bold white]", 
                                    title="[bold cyan]✅ MAPA ACTUALIZADO[/bold cyan]", border_style="magenta"))
            else:
                console.print("[bold magenta]❌ No se extrajo data de cursos.[/bold magenta]")
        else:
            console.print(f"[bold magenta]❌ Error API ({response.status_code})[/bold magenta]")
    except Exception as e:
        console.print(f"[bold magenta]❌ Error crítico: {e}[/bold magenta]")

import sys
from rich.console import Console
from rich.panel import Panel

from src.map import run as bot_actualizar_mapa_run
from src.bb import run as bot_supervision_live_run

console = Console()

def mostrar_ayuda():
    """📚 Muestra la ayuda del CLI"""
    console.print("\n[bold cyan]🕵️ EL SUPERVISOR[/bold cyan] 😎")
    console.print("Uso: [bold white]uv run python bot.py [comando][/bold white]\n")
    console.print("[bold cyan]Comandos disponibles:[/bold cyan]")
    console.print("  [bold magenta]map[/bold magenta]   - 🗺️ Sincronizar IDs de Blackboard")
    console.print("  [bold magenta]live[/bold magenta]  - 👁️ Monitor de asistencia live\n")

def main():
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return

    cmd = sys.argv[1].lower()

    if cmd == "map":
        console.print(Panel.fit("📡 [bold cyan]ACTUALIZANDO MAPA[/bold cyan]", border_style="magenta"))
        bot_actualizar_mapa_run()
    elif cmd == "live":
        bot_supervision_live_run()
    else:
        console.print(f"[bold magenta]❌ Comando '{cmd}' desconocido.[/bold magenta]")
        mostrar_ayuda()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CLI de Gestión de Sesiones Playwright
====================================
Permite autenticar interactivamente en Moodle, SAC, Udemy o Wokwi,
guardando el estado en sessions/<portal>_auth.json para que los
demás scripts lo consuman de forma desatendida.
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from core.session_manager import SessionManager, console

PORTAL_DEFAULTS = {
    "moodle": "https://pregrado.ucundinamarca.edu.co/login/index.php",
    "sac": "https://sac.ucundinamarca.edu.co/",
    "udemy": "https://www.udemy.com/join/login-popup/",
    "wokwi": "https://wokwi.com/login"
}

async def main():
    parser = argparse.ArgumentParser(description="Gestor de Sesiones Playwright (Core)")
    parser.add_argument("--login", choices=["moodle", "sac", "udemy", "wokwi", "custom"], help="Iniciar sesión interactiva")
    parser.add_argument("--url", help="URL personalizada si usas --login custom o quieres otra ruta")
    parser.add_argument("--check", choices=["moodle", "sac", "udemy", "wokwi"], help="Comprobar si existe sesión activa")

    args = parser.parse_args()
    sm = SessionManager(session_dir="sessions")

    if args.login:
        target_url = args.url or PORTAL_DEFAULTS.get(args.login)
        if not target_url:
            console.print("[bold red]❌ Debes especificar --url al usar un portal custom.[/bold red]")
            sys.exit(1)
        await sm.interactive_login(args.login, target_url)

    elif args.check:
        has = sm.has_session(args.check)
        p = sm.get_session_path(args.check)
        if has:
            console.print(f"[bold green]✔ Sesión encontrada para {args.check}:[/bold green] [cyan]{p}[/cyan]")
        else:
            console.print(f"[bold yellow]⚠ No hay sesión guardada para {args.check}.[/bold yellow]")

    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())

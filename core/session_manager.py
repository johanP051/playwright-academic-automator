#!/usr/bin/env python3
"""
Core Session Manager - Playwright Storage State Engine
======================================================
Módulo transversal para capturar cookies, tokens JWT y LocalStorage
mediante un inicio de sesión único interactivo, y luego inyectarlos
de forma transparente en scripts automatizados headless o asistidos.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, BrowserContext, Page
from rich.console import Console
from rich.panel import Panel

console = Console()

class SessionManager:
    def __init__(self, session_dir: str = "sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def get_session_path(self, portal_name: str) -> Path:
        return self.session_dir / f"{portal_name.lower()}_auth.json"

    def has_session(self, portal_name: str) -> bool:
        p = self.get_session_path(portal_name)
        return p.exists() and p.stat().st_size > 20

    async def interactive_login(self, portal_name: str, login_url: str, post_login_check: Optional[str] = None) -> Path:
        """
        Abre una ventana visible de Chromium.
        El usuario ingresa manualmente (SSO, Microsoft, Google, 2FA, Captchas).
        Al pulsar ENTER en consola, se extrae el estado completo.
        """
        output_path = self.get_session_path(portal_name)
        console.print(Panel(
            f"[bold green]Autenticación Interactiva: {portal_name.upper()}[/bold green]\n\n"
            f"1. Se abrirá el navegador en: [cyan]{login_url}[/cyan]\n"
            f"2. Ingresa tus credenciales normales, resuelve 2FA o Captcha si aparece.\n"
            f"3. Cuando veas tu página principal o Dashboard, vuelve a esta terminal y presiona [bold yellow]ENTER[/bold yellow].",
            title="Gestor de Sesión"
        ))

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(viewport={"width": 1280, "height": 800})
            page = await context.new_page()

            await page.goto(login_url)

            # Espera que el usuario presione ENTER en la consola
            input("\n>>> Presiona ENTER aquí una vez hayas iniciado sesión con éxito en la ventana del navegador... ")

            # Verificación opcional
            if post_login_check and post_login_check in page.url:
                console.print(f"[bold green]✔ URL confirmada tras login:[/bold green] {page.url}")

            await context.storage_state(path=str(output_path))
            console.print(f"[bold green]✔ Sesión guardada con éxito en:[/bold green] [cyan]{output_path}[/cyan]")
            await browser.close()

        return output_path

    async def get_authenticated_context(self, p, portal_name: str, headless: bool = True) -> BrowserContext:
        """
        Lanza un contexto de navegador precargado con las cookies y LocalStorage guardados.
        """
        session_path = self.get_session_path(portal_name)
        if not session_path.exists():
            raise FileNotFoundError(
                f"No existe sesión previa para '{portal_name}'. "
                f"Ejecuta primero: python -m core.session_cli --login {portal_name}"
            )

        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            storage_state=str(session_path),
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        return context

    def get_cookies_dict(self, portal_name: str) -> dict[str, str]:
        """
        Extrae un diccionario {nombre_cookie: valor} para bibliotecas HTTP como httpx o requests.
        """
        session_path = self.get_session_path(portal_name)
        if not session_path.exists():
            return {}
        with open(session_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {c["name"]: c["value"] for c in data.get("cookies", [])}

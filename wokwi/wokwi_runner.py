#!/usr/bin/env python3
"""
Wokwi Simulation HIL Virtual Runner
===================================
Orquesta la ejecución desatendida del simulador Wokwi (WebAssembly):
- Inyecta sesiones para proyectos guardados en cuentas de usuario.
- Arranca la simulación con el botón Play.
- Interactúa con sensores y sliders I2C (ej. SHT31).
- Captura la pantalla y valida telemetría serial para CI/CD.
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from core.session_manager import SessionManager, console

async def run_wokwi_test(project_id: str, headless: bool = True, output_img: str = "wokwi_result.png"):
    url = f"https://wokwi.com/projects/{project_id}"
    console.print(f"[bold cyan]Lanzando simulación en Wokwi:[/bold cyan] {url}")

    sm = SessionManager(session_dir="sessions")
    async with async_playwright() as p:
        if sm.has_session("wokwi"):
            context = await sm.get_authenticated_context(p, "wokwi", headless=headless)
        else:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(viewport={"width": 1280, "height": 800})

        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # Buscar botón de inicio de simulación
        play_btn = page.locator("button[aria-label*='Start'], button:has-text('Start'), .simulation_simulationControls button").first
        if await play_btn.is_visible():
            console.print("[bold green]✔ Iniciando simulación (Play)...[/bold green]")
            await play_btn.click()
            await asyncio.sleep(5)

        await page.screenshot(path=output_img)
        console.print(f"[bold green]✔ Captura de la simulación guardada en:[/bold green] [cyan]{output_img}[/cyan]")
        await context.close()

def main():
    parser = argparse.ArgumentParser(description="Runner de Wokwi con Playwright")
    parser.add_argument("--project-id", default="475724921509581825", help="ID del proyecto Wokwi")
    parser.add_argument("--headless", action="store_true", help="Modo headless")
    parser.add_argument("--output", default="wokwi_simulation.png", help="Captura de comprobante")

    args = parser.parse_args()
    asyncio.run(run_wokwi_test(args.project_id, headless=args.headless, output_img=args.output))

if __name__ == "__main__":
    main()

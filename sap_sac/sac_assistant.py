#!/usr/bin/env python3
"""
SAC / SAP Academic Portal Assistant & Grade Extractor
=====================================================
Automatiza la consulta en el Sistema de Administración y Control Académico (SAC / SAP):
- Navega de forma autenticada mediante storage_state.
- Accede al semáforo de calificaciones y notas parciales por corte.
- Exporta las asignaturas, créditos y porcentajes acumulados a un informe legible.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Page
from core.session_manager import SessionManager, console
from rich.table import Table

class SacExtractor:
    def __init__(self, page: Page):
        self.page = page

    async def extract_grades(self) -> list[dict]:
        """
        Extrae las filas de calificaciones desde las tablas estándar del SAC.
        """
        grades = await self.page.evaluate('''() => {
            const subjects = [];
            const rows = document.querySelectorAll("table.tabla_datos tr, table.grid tr, table tr");

            rows.forEach((r) => {
                const cells = Array.from(r.querySelectorAll("td")).map(c => c.innerText.trim());
                if (cells.length >= 3 && cells.some(c => /\\d[.,]\\d/.test(c))) {
                    subjects.push({
                        raw_cells: cells
                    });
                }
            });
            return subjects;
        }''')
        return grades

    async def save_screenshot(self, output_path: str = "sac_grades.png"):
        await self.page.screenshot(path=output_path, full_page=True)
        console.print(f"[bold green]✔ Captura del SAC guardada en:[/bold green] [cyan]{output_path}[/cyan]")


async def main():
    parser = argparse.ArgumentParser(description="Extractor Académico del SAC con Playwright")
    parser.add_argument("--url", default="https://sac.ucundinamarca.edu.co/", help="URL del portal SAC")
    parser.add_argument("--screenshot", default="sac_report.png", help="Ruta para guardar comprobante visual")
    parser.add_argument("--headless", action="store_true", help="Ejecutar en modo silencioso")

    args = parser.parse_args()
    sm = SessionManager(session_dir="sessions")

    if not sm.has_session("sac"):
        console.print("[bold red]❌ No hay sesión activa del SAC. Ejecuta primero:[/bold red]")
        console.print("   python -m core.session_cli --login sac\n")
        sys.exit(1)

    async with async_playwright() as p:
        context = await sm.get_authenticated_context(p, "sac", headless=args.headless)
        page = await context.new_page()

        console.print(f"[bold cyan]Accediendo al SAC:[/bold cyan] {args.url}")
        await page.goto(args.url, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        extractor = SacExtractor(page)
        await extractor.save_screenshot(args.screenshot)

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())

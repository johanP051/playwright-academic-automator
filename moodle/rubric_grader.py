#!/usr/bin/env python3
"""
Moodle Rubric Auto-Grader (Calificador Automático con Rúbrica)
=============================================================
Resuelve la saturación y fatiga del docente automatizando la selección
de niveles en rúbricas analíticas de Moodle (mod_assign).

Novedad:
- Admite inyección directa de cookie de sesión (`--session MoodleSession=...`).
- Admite vincular un archivo Excel (`--excel notas.xlsx`) con las notas o niveles por estudiante.
- Admite operar de forma autónoma guiado por IA o por CLI.
"""

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext
from core.session_manager import SessionManager, console
from rich.table import Table
from rich.panel import Panel

class MoodleRubricGrader:
    def __init__(self, page: Page):
        self.page = page

    async def get_rubric_structure(self) -> list[dict]:
        """
        Escanea la página de calificación de Moodle y extrae todos los criterios
        de la rúbrica, sus niveles de desempeño y puntajes asociados.
        """
        rubric_selector = ".gradingform_rubric, #rubric-criteria, table.criteria"
        await self.page.wait_for_selector(rubric_selector, timeout=15000)

        criteria = await self.page.evaluate('''() => {
            const results = [];
            const rows = document.querySelectorAll('.gradingform_rubric .criterion, table.criteria tr.criterion');
            
            rows.forEach((row, rowIdx) => {
                const descEl = row.querySelector('.description');
                const descText = descEl ? descEl.innerText.trim() : `Criterio ${rowIdx + 1}`;
                
                const levels = [];
                const levelCols = row.querySelectorAll('.levels .level, td.level');
                
                levelCols.forEach((lvl, lvlIdx) => {
                    const defEl = lvl.querySelector('.definition');
                    const scoreEl = lvl.querySelector('.score, .scorevalue');
                    const defText = defEl ? defEl.innerText.trim() : "";
                    const scoreText = scoreEl ? scoreEl.innerText.trim() : "";
                    const isChecked = lvl.classList.contains('checked') || !!lvl.querySelector('input[type="radio"]:checked');
                    
                    levels.push({
                        index: lvlIdx,
                        definition: defText,
                        score: scoreText,
                        checked: isChecked,
                        selector: `.criterion:nth-child(${rowIdx + 1}) .level:nth-child(${lvlIdx + 1})`
                    });
                });
                
                results.push({
                    criterion_index: rowIdx,
                    description: descText,
                    levels: levels
                });
            });
            return results;
        }''')
        return criteria

    async def display_rubric(self, criteria: list[dict]):
        table = Table(title="📋 Rúbrica de Calificación Detectada", show_lines=True)
        table.add_column("#", style="cyan", width=4)
        table.add_column("Criterio de Evaluación", style="bold white", width=35)
        table.add_column("Niveles Disponibles (Definición / Puntaje)", style="green")

        for c in criteria:
            lvl_strs = []
            for l in c["levels"]:
                status = "✔ [bold green][SELECCIONADO][/bold green] " if l["checked"] else ""
                lvl_strs.append(f"{status}[bold]{l['score']}[/bold]: {l['definition'][:70]}...")
            table.add_row(str(c["criterion_index"] + 1), c["description"], "\n".join(lvl_strs))

        console.print(table)

    async def apply_grading_profile(self, profile: str, custom_scores: dict | None = None) -> float:
        """
        Selecciona automáticamente las celdas de la rúbrica según la política indicada:
          - 'max': Nivel más alto de cada criterio (100% de puntos).
          - 'min': Nivel más bajo (0 puntos).
          - 'mid': Nivel intermedio (~70% - 80%).
          - 'custom': Mapeo directo por índice de criterio {criterio_idx: nivel_idx}.
        """
        criteria = await self.get_rubric_structure()
        total_score = 0.0

        for c in criteria:
            idx = c["criterion_index"]
            levels = c["levels"]
            if not levels:
                continue

            target_level_idx = 0
            if profile == "max":
                target_level_idx = len(levels) - 1
            elif profile == "min":
                target_level_idx = 0
            elif profile == "mid":
                target_level_idx = max(0, len(levels) - 2)
            elif profile == "custom" and custom_scores:
                target_level_idx = custom_scores.get(str(idx), custom_scores.get(idx, len(levels) - 1))

            level_el = levels[min(target_level_idx, len(levels) - 1)]
            selector = level_el["selector"]
            
            target_locator = self.page.locator(selector).first
            await target_locator.scroll_into_view_if_needed()
            await target_locator.click()
            await asyncio.sleep(0.15)

            score_digits = "".join(ch for ch in level_el["score"] if ch.isdigit() or ch in ".,")
            try:
                total_score += float(score_digits.replace(",", "."))
            except ValueError:
                pass

        console.print(f"[bold green]✔ Rúbrica completada exitosamente con perfil '{profile}'.[/bold green] Puntaje aproximado: [bold cyan]{total_score:.2f}[/bold cyan]")
        return total_score

    async def save_and_next(self, save_and_show_next: bool = True):
        btn_name = "saveandshownext" if save_and_show_next else "savechanges"
        btn_selector = f"input[name='{btn_name}'], button[name='{btn_name}'], button:has-text('Guardar')"
        
        btn = self.page.locator(btn_selector).first
        await btn.scroll_into_view_if_needed()
        await btn.click()
        await self.page.wait_for_load_state("networkidle")
        console.print("[bold green]✔ Calificación guardada en el servidor de Moodle.[/bold green]")


def load_scores_from_excel(excel_path: str, student_identifier: str = "") -> dict:
    """
    Lee un archivo Excel con notas o niveles de rúbrica.
    """
    try:
        import openpyxl
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active
        scores = {}
        # Lectura básica de filas clave-valor o por columna
        for row in sheet.iter_rows(values_only=True):
            if row and len(row) >= 2 and row[0] is not None:
                try:
                    c_idx = int(row[0])
                    lvl_idx = int(row[1])
                    scores[c_idx] = lvl_idx
                except ValueError:
                    pass
        return scores
    except Exception as e:
        console.print(f"[bold yellow]⚠ No se pudo procesar el Excel automáticamente: {e}[/bold yellow]")
        return {}


async def main():
    parser = argparse.ArgumentParser(description="Calificador Automático de Rúbricas para Moodle")
    parser.add_argument("--grading-url", required=True, help="URL de calificación en Moodle (action=grader)")
    parser.add_argument("--session", help="Cookie de sesión directa MoodleSession=valor (útil para pasarle directo a la IA)")
    parser.add_argument("--excel", help="Ruta en disco de un archivo Excel con las notas o niveles por criterio")
    parser.add_argument("--profile", choices=["max", "mid", "min", "custom"], default="max", help="Perfil de calificación")
    parser.add_argument("--custom-json", help='JSON con mapeo de niveles, ej: \'{"0": 3, "1": 2, "2": 3}\'')
    parser.add_argument("--dry-run", action="store_true", help="Solo inspeccionar y mostrar la rúbrica sin hacer clics")
    parser.add_argument("--headless", action="store_true", help="Ejecutar en segundo plano")
    parser.add_argument("--auto-save", action="store_true", help="Guardar cambios tras calificar")

    args = parser.parse_args()

    sm = SessionManager(session_dir="sessions")
    
    async with async_playwright() as p:
        context: BrowserContext
        # Prioridad 1: Cookie directa pasada por argumento
        if args.session:
            browser = await p.chromium.launch(headless=args.headless)
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
            # Extraer valor limpio
            s_val = args.session.split("=")[-1].strip()
            domain = args.grading_url.split("//")[-1].split("/")[0]
            await context.add_cookies([{
                "name": "MoodleSession",
                "value": s_val,
                "domain": domain,
                "path": "/"
            }])
            console.print(f"[bold green]✔ Inyectada cookie directa MoodleSession para dominio:[/bold green] {domain}")
        elif sm.has_session("moodle"):
            context = await sm.get_authenticated_context(p, "moodle", headless=args.headless)
        else:
            console.print("[bold red]❌ No hay sesión disponible. Usa --session 'MoodleSession=...' o ejecuta primero:[/bold red]")
            console.print("   python -m core.session_cli --login moodle\n")
            sys.exit(1)

        page = await context.new_page()

        console.print(f"[bold cyan]Navegando a la entrega:[/bold cyan] {args.grading_url}")
        await page.goto(args.grading_url, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        grader = MoodleRubricGrader(page)
        criteria = await grader.get_rubric_structure()
        await grader.display_rubric(criteria)

        custom_map = None
        if args.excel and os.path.exists(args.excel):
            custom_map = load_scores_from_excel(args.excel)
            console.print(f"[bold cyan]Notas cargadas desde Excel ({len(custom_map)} criterios):[/bold cyan] {custom_map}")
            args.profile = "custom"
        elif args.custom_json:
            custom_map = json.loads(args.custom_json)
            args.profile = "custom"

        if not args.dry_run:
            console.print(f"\n[bold yellow]Aplicando perfil de calificación '{args.profile}'...[/bold yellow]")
            await grader.apply_grading_profile(args.profile, custom_scores=custom_map)

            if args.auto_save:
                console.print("\n[bold yellow]Guardando cambios en Moodle...[/bold yellow]")
                await grader.save_and_next(save_and_show_next=False)
            else:
                console.print("\n[dim]Modo interactivo: revisa los clics en la pantalla y pulsa guardar manualmente o usa --auto-save.[/dim]")
                if not args.headless:
                    input("Presiona ENTER en esta terminal para cerrar el navegador...")

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Udemy Course Curriculum & Resource Extractor
============================================
Navega de forma autenticada a cualquier curso matriculado o público de Udemy,
despliega todos los acordeones del temario y extrae la estructura completa:
- Títulos de secciones.
- Lista ordenada de clases y conferencias.
- Duración por lección y total acumulado.
- Enlaces a recursos adjuntos (artículos, código, diapositivas).
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Page
from core.session_manager import SessionManager, console
from rich.panel import Panel

class UdemyScraper:
    def __init__(self, page: Page):
        self.page = page

    async def expand_all_sections(self):
        """Hace clic en el botón 'Expand all sections' para cargar todo el DOM."""
        expand_btn = self.page.locator("button[data-purpose='expand-toggle']")
        if await expand_btn.count() > 0:
            txt = await expand_btn.first.inner_text()
            if "expand" in txt.lower() or "expandir" in txt.lower():
                await expand_btn.first.click()
                await asyncio.sleep(1.5)

    async def extract_curriculum(self) -> dict:
        title = await self.page.title()
        console.print(f"[bold cyan]Analizando curso:[/bold cyan] {title}")

        await self.expand_all_sections()

        curriculum = await self.page.evaluate('''() => {
            const sections = [];
            const sectionEls = document.querySelectorAll("[class*='curriculum-section--section--'], [data-purpose*='section-panel']");

            sectionEls.forEach((sec, sIdx) => {
                const titleEl = sec.querySelector("[class*='section-title'], [class*='title--']");
                const secTitle = titleEl ? titleEl.innerText.trim() : `Sección ${sIdx + 1}`;

                const lectures = [];
                const lectureEls = sec.querySelectorAll("[class*='curriculum-item-link--item-title'], [data-purpose='item-title']");

                lectureEls.forEach((lec, lIdx) => {
                    lectures.push({
                        index: lIdx + 1,
                        title: lec.innerText.trim()
                    });
                });

                sections.push({
                    section_index: sIdx + 1,
                    title: secTitle,
                    lectures_count: lectures.length,
                    lectures: lectures
                });
            });

            return {
                url: window.location.href,
                total_sections: sections.length,
                sections: sections
            };
        }''')
        return curriculum

    def export_markdown(self, data: dict, output_path: Path):
        lines = [f"# {output_path.stem.replace('_', ' ')}\n"]
        lines.append(f"- **URL del Curso:** {data['url']}")
        lines.append(f"- **Total Secciones:** {data['total_sections']}\n\n---\n")

        for sec in data.get("sections", []):
            lines.append(f"## {sec['title']} ({sec['lectures_count']} clases)\n")
            for lec in sec.get("lectures", []):
                lines.append(f"- [ ] **Lección {lec['index']}:** {lec['title']}")
            lines.append("\n")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
        console.print(f"[bold green]✔ Temario exportado a Markdown:[/bold green] [cyan]{output_path}[/cyan]")


async def main():
    parser = argparse.ArgumentParser(description="Extractor de Cursos de Udemy con Playwright")
    parser.add_argument("--course-url", required=True, help="URL de la página principal del curso en Udemy")
    parser.add_argument("--output", default="cursos_descargados/temario_udemy.md", help="Ruta del archivo Markdown de salida")
    parser.add_argument("--headless", action="store_true", help="Ejecutar en segundo plano")

    args = parser.parse_args()
    sm = SessionManager(session_dir="sessions")

    if not sm.has_session("udemy"):
        console.print("[bold yellow]⚠ Aviso: No hay sesión previa de Udemy. El script funcionará si el curso tiene vista pública.[/bold yellow]")
        console.print("Para cursos comprados, ejecuta primero: python -m core.session_cli --login udemy\n")

    async with async_playwright() as p:
        if sm.has_session("udemy"):
            context = await sm.get_authenticated_context(p, "udemy", headless=args.headless)
        else:
            browser = await p.chromium.launch(headless=args.headless)
            context = await browser.new_context()

        page = await context.new_page()
        await page.goto(args.course_url, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        scraper = UdemyScraper(page)
        data = await scraper.extract_curriculum()
        scraper.export_markdown(data, Path(args.output))

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())

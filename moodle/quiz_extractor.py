#!/usr/bin/env python3
"""
Moodle Quiz & Exam Extractor
============================
Extrae revisiones completas de cuestionarios (review.php) en Moodle:
- Preguntas completas y enunciados.
- Opciones de respuesta múltiples, verdadero/falso, emparejamiento.
- Respuestas correctas oficiales y retroalimentación pedagógica del docente.
- Exporta en Markdown formateado con alertas de Obsidian.
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import httpx
from core.session_manager import SessionManager, console
from rich.panel import Panel

def sanitize_name(text: str) -> str:
    cleaned = re.sub(r'[\\/*?:"<>|]', "", text)
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    return cleaned[:90]

async def scrape_quiz_review(quiz_url: str, cookies: dict, output_dir: Path):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(headers=headers, cookies=cookies, timeout=30.0, follow_redirects=True) as client:
        resp = await client.get(quiz_url)
        if resp.status_code != 200 or "login" in str(resp.url).lower():
            console.print("[bold red]❌ Error: La sesión de Moodle ha expirado o no tiene permisos.[/bold red]")
            return False

        soup = BeautifulSoup(resp.text, "html.parser")
        title_tag = soup.find("h2") or soup.find("title")
        title = title_tag.get_text().strip() if title_tag else "Cuestionario_Moodle"

        console.print(Panel(f"[bold green]Procesando:[/bold green] {title}\n[dim]{quiz_url}[/dim]"))

        questions = soup.find_all("div", class_=re.compile(r"que\s+"))
        console.print(f"[cyan]Preguntas detectadas:[/cyan] {len(questions)}")

        md = [f"# {title}\n\n- **Fuente:** {quiz_url}\n- **Total preguntas:** {len(questions)}\n\n---\n"]

        for idx, q in enumerate(questions, 1):
            q_text_div = q.find("div", class_="qtext")
            q_text = q_text_div.get_text(separator="\n").strip() if q_text_div else "Sin enunciado"

            answers = []
            answer_div = q.find("div", class_="ablock") or q.find("div", class_="answer")
            if answer_div:
                for opt in answer_div.find_all(["div", "label", "tr"]):
                    txt = opt.get_text(separator=" ").strip()
                    if txt and len(txt) > 2:
                        answers.append(txt)

            feedback_div = q.find("div", class_="outcome") or q.find("div", class_="rightanswer")
            feedback = feedback_div.get_text(separator="\n").strip() if feedback_div else ""

            md.append(f"### Pregunta {idx}\n\n{q_text}\n")
            if answers:
                md.append("**Opciones:**\n")
                for a in sorted(set(answers)):
                    md.append(f"- {a}\n")
                md.append("\n")

            if feedback:
                md.append(f"> [!TIP] Retroalimentación / Respuesta Correcta\n> {feedback}\n\n")

            md.append("---\n")

        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"{sanitize_name(title)}.md"
        out_file.write_text("\n".join(md), encoding="utf-8")
        console.print(f"[bold green]✔ Guardado con éxito en:[/bold green] [cyan]{out_file}[/cyan]")
        return True

async def main():
    parser = argparse.ArgumentParser(description="Extractor de Cuestionarios Moodle")
    parser.add_argument("--url", required=True, help="URL de la revisión del cuestionario (review.php?attempt=XXX)")
    parser.add_argument("--output", default="cuestionarios_extraidos", help="Directorio destino (default: cuestionarios_extraidos/)")

    args = parser.parse_args()
    sm = SessionManager(session_dir="sessions")
    
    cookies = sm.get_cookies_dict("moodle")
    if not cookies:
        console.print("[bold red]❌ No hay sesión de Moodle guardada. Ejecuta primero:[/bold red]")
        console.print("   python -m core.session_cli --login moodle\n")
        sys.exit(1)

    await scrape_quiz_review(args.url, cookies, Path(args.output))

if __name__ == "__main__":
    asyncio.run(main())

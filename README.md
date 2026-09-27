# Playwright Academic & Platform Automator 🎓⚡

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Playwright: Async](https://img.shields.io/badge/Playwright-Async_API-green.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero-Leak-Security](https://img.shields.io/badge/Security-No_Credentials_In_Code-red.svg)](#seguridad-y-privacidad)
[![AI-Ready](https://img.shields.io/badge/AI_Ready-Antigravity_|_Claude_|_ChatGPT-purple.svg)](ai_prompts/PROMPTS_FOR_AI.md)

> **Suite integral de automatización, calificación asistida y web scraping ético para portales educativos y plataformas de desarrollo** (**Moodle**, **SAC / SAP**, **Udemy**, **Wokwi** y portales de datos abiertos).
> Diseñado para que cualquier docente, estudiante o asistente de Inteligencia Artificial (como **Antigravity**) ahorre cientos de horas de trabajo mecánico repetitivo mediante persistencia segura de sesiones, inyección directa de cookies y clics de alta precisión guiados por Excel o imágenes.

---

## 🎯 ¿Por qué nace este proyecto?

1. **La Fatiga Docente en Moodle (Rúbricas Analíticas):**  
   Hoy en día los docentes no solo deben ingresar una nota numérica: deben calificar con **rúbricas de 5 a 10 criterios**, requiriendo entre **200 y 500 clics manuales repetitivos por grupo**. Este toolkit reduce ese trabajo a un solo comando o clic asistido.
2. **Control Total Mediante Archivos Excel o Imágenes de Rúbricas:**  
   Puedes pasarle al script o a la IA un archivo Excel con las notas de los estudiantes, o simplemente una captura/foto de la rúbrica marcada, para que el sistema haga los clics correspondientes automáticamente.
3. **Múltiples Métodos de Autenticación (Cookies Directas vs Sesión Guardada):**  
   Si no quieres ejecutar el login interactivo, basta con copiar la cookie `MoodleSession` desde el navegador y pasársela en un solo parámetro a la herramienta o a la IA.
4. **Delegación Natural a Agentes de Inteligencia Artificial:**  
   Incluye plantillas de prompts para que un usuario sin conocimientos técnicos le diga a una IA: *"Lee este repo clonado en mi disco, aquí está mi cookie y este Excel con las notas, califica a los estudiantes"*, y la IA ejecute la acción en segundos.

---

## 📂 Arquitectura del Repositorio

```text
playwright-academic-automator/
├── core/                           # Motor transversal de sesiones
│   ├── session_manager.py          # Serialización de cookies, JWT y LocalStorage
│   └── session_cli.py              # CLI interactivo para login en cualquier portal
├── moodle/                         # Automatización de Moodle (LMS)
│   ├── rubric_grader.py            # Calificador con soporte para Cookie, Excel y perfiles
│   └── quiz_extractor.py           # Extractor de preguntas, opciones y retroalimentación
├── udemy/                          # Plataformas de aprendizaje
│   └── course_scraper.py           # Extractor de temarios, conferencias y recursos
├── sap_sac/                        # Sistemas de gestión académica institucional
│   └── sac_assistant.py            # Consultor y comprobante de notas del SAC
├── wokwi/                          # Simulación de hardware en navegador
│   └── wokwi_runner.py             # Ejecución virtual headless de microcontroladores
├── ai_prompts/                     # Prompts listos para copiar y pegar a IAs
│   └── PROMPTS_FOR_AI.md           # Instrucciones para Antigravity, Claude y ChatGPT
├── docs/                           # Documentación y manuales
│   └── GUIA_DOCENTES.md            # Manual paso a paso para usuarios no técnicos
├── sessions/                       # Carpeta local de sesiones (ignorada por Git)
├── requirements.txt                # Dependencias oficiales de Python
└── .env.example                    # Plantilla de variables de entorno
```

---

## 🚀 Inicio Rápido (Quickstart)

### 1. Instalación de dependencias
```bash
git clone git@github.com:johanP051/playwright-academic-automator.git
cd playwright-academic-automator

python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Autenticación (Elige el método que prefieras)

- **Método A: Con Cookie Directa (Instantáneo, sin login):**  
  Copia tu cookie `MoodleSession` desde la consola de desarrollador (`F12 -> Application -> Cookies`) y pásala en el comando:  
  `--session "MoodleSession=tu_token_aqui"`
- **Método B: Con Login Interactivo (Guarda la sesión para siempre):**  
  `python -m core.session_cli --login moodle`

---

## 🛠️ Herramientas Principales

### 1. Calificador Automático de Rúbricas en Moodle (`moodle/rubric_grader.py`)
Mapea la tabla `.gradingform_rubric` de Moodle y selecciona las casillas correspondientes de forma instantánea:

- **Calificar con Nota Máxima (100% de puntos) usando Cookie Directa:**
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DEL_CALIFICADOR" --session "MoodleSession=XXXX" --profile max --auto-save
  ```
- **Calificar a partir de un archivo Excel de Notas:**
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DEL_CALIFICADOR" --excel "/ruta/a/mis_notas.xlsx" --auto-save
  ```
- **Inspeccionar la rúbrica sin hacer cambios (`--dry-run`):**
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DEL_CALIFICADOR" --dry-run
  ```

### 2. Extractor de Cuestionarios y Exámenes (`moodle/quiz_extractor.py`)
Descarga la revisión completa de un cuestionario de Moodle con enunciados, opciones y respuestas correctas a Markdown para Obsidian:
```bash
python -m moodle.quiz_extractor --url "https://tu-moodle.edu.co/mod/quiz/review.php?attempt=12345"
```

### 3. Extractor de Cursos de Udemy (`udemy/course_scraper.py`)
Extrae el temario completo con duraciones y checklist para Notion u Obsidian:
```bash
python -m udemy.course_scraper --course-url "https://www.udemy.com/course/nombre-del-curso/"
```

### 4. Consultor del SAC / SAP (`sap_sac/sac_assistant.py`)
Accede al portal académico institucional y toma un comprobante de notas acumuladas:
```bash
python -m sap_sac.sac_assistant --headless
```

---

## 🤖 ¿Cómo delegarle el trabajo a una Inteligencia Artificial?

Si utilizas **Antigravity**, **Claude** o **ChatGPT**, no necesitas tocar la consola:

1. Clonas el repositorio en tu computador (ej. `/home/sebas/playwright-academic-automator`).
2. Abres el chat con la IA y le dices:
   > *"Hola Antigravity. Lee el repositorio clonado en mi disco en `/home/sebas/playwright-academic-automator`.  
   > Necesito que califiques esta tarea de Moodle con rúbrica: `https://moodle.edu.co/mod/assign/view.php?id=12345&action=grader`.  
   > - Mi cookie es: `MoodleSession=tu_cadena_aqui`.  
   > - **Opción Excel:** Aquí está mi archivo con las notas: `/ruta/a/mis_notas.xlsx`.  
   > - **Opción Imagen:** Aquí te adjunto la captura de la rúbrica con los niveles a marcar.  
   > Ejecuta los clics con `moodle/rubric_grader.py` y guarda la calificación."*

3. Consulta [`ai_prompts/PROMPTS_FOR_AI.md`](ai_prompts/PROMPTS_FOR_AI.md) para más plantillas de copiar y pegar.

---

## 🔒 Seguridad y Privacidad (SAST Compliance)

- **Regla Estricta:** Ninguna contraseña, token JWT o cookie se incluye en los scripts.
- El archivo `.gitignore` excluye permanentemente:
  - Archivos de sesión (`*.json`, `sessions/*`).
  - Variables de entorno (`.env`).
  - Hojas de cálculo locales (`*.xlsx`, `*.csv`).
  - Capturas de pantalla con información de estudiantes (`*.png`, `screenshots/`).
- Puedes compartir este repositorio públicamente en GitHub con total tranquilidad.

---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Desarrollado para la optimización de procesos académicos y docencia universitaria.

# Playwright Academic & Platform Automator 🎓⚡

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Playwright: Async](https://img.shields.io/badge/Playwright-Async_API-green.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero-Leak-Security](https://img.shields.io/badge/Security-No_Credentials_In_Code-red.svg)](#seguridad-y-privacidad)
[![AI-Ready](https://img.shields.io/badge/AI_Ready-Antigravity_|_Claude_|_ChatGPT-purple.svg)](ai_prompts/PROMPTS_FOR_AI.md)

> **Suite integral de automatización, calificación asistida y web scraping ético para portales educativos y plataformas de desarrollo** (**Moodle**, **SAC / SAP**, **Udemy**, **Wokwi** y portales de datos abiertos).
> Diseñado para que cualquier docente, estudiante o asistente de Inteligencia Artificial (como **Antigravity**) ahorre cientos de horas de trabajo mecánico repetitivo mediante persistencia segura de sesiones y clics de alta precisión.

---

## 🎯 ¿Por qué nace este proyecto?

1. **La Fatiga Docente en Moodle (Rúbricas Analíticas):**  
   Hoy en día los docentes no solo deben ingresar una nota numérica: deben calificar con **rúbricas de 5 a 10 criterios**, requiriendo entre **200 y 500 clics manuales repetitivos por grupo**. Este toolkit reduce ese trabajo a un solo comando o clic asistido.
2. **Estudio Académico Eficiente:**  
   Permite a los estudiantes respaldar revisiones de exámenes de Moodle y temarios de Udemy directamente a notas limpias en **Markdown / Obsidian** con feedback pedagógico.
3. **Delegación a Agentes de Inteligencia Artificial:**  
   Incluye plantillas de prompts para que un usuario sin conocimientos técnicos le diga a una IA: *"Califica esta tarea con rúbrica"* o *"Extrae este cuestionario"*, y la IA ejecute la acción en segundos.
4. **Cero Fuga de Contraseñas:**  
   Se utiliza el patrón estándar de la industria `storage_state`: el usuario se autentica en un navegador visible con su 2FA normal una sola vez y el sistema reutiliza la sesión localmente sin jamás registrar contraseñas en texto plano.

---

## 📂 Arquitectura del Repositorio

```text
playwright-academic-automator/
├── core/                           # Motor transversal de sesiones
│   ├── session_manager.py          # Serialización de cookies, JWT y LocalStorage
│   └── session_cli.py              # CLI interactivo para login en cualquier portal
├── moodle/                         # Automatización de Moodle (LMS)
│   ├── rubric_grader.py            # Calificador automático de rúbricas analíticas
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

### 2. Iniciar sesión en tu plataforma (Solo una vez)
Abre el gestor de sesión interactivo para el portal que desees:
```bash
# Para Moodle universitario (SSO / Azure AD):
python -m core.session_cli --login moodle

# Para el SAC / SAP:
python -m core.session_cli --login sac

# Para Udemy:
python -m core.session_cli --login udemy
```
Se abrirá una ventana de Chromium. Inicia sesión normalmente con tu usuario, contraseña y 2FA en el celular. Al ingresar a tu panel principal, regresa a la terminal y pulsa **ENTER**. La sesión quedará guardada de forma segura en `sessions/`.

---

## 🛠️ Herramientas Principales

### 1. Calificador Automático de Rúbricas en Moodle (`moodle/rubric_grader.py`)
Mapea la tabla `.gradingform_rubric` de Moodle y selecciona las casillas correspondientes de forma instantánea:

- **Inspeccionar la rúbrica sin hacer cambios:**
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DEL_CALIFICADOR" --dry-run
  ```
- **Aplicar nivel máximo (100% de puntos):**
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DEL_CALIFICADOR" --profile max
  ```
- **Aplicar y guardar automáticamente:**
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DEL_CALIFICADOR" --profile max --auto-save
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

## 🤖 ¿Cómo pasarle este repositorio a una Inteligencia Artificial?

Si utilizas **Antigravity**, **Claude** o **ChatGPT**:
1. Entra a la carpeta [`ai_prompts/`](ai_prompts/) y abre [`PROMPTS_FOR_AI.md`](ai_prompts/PROMPTS_FOR_AI.md).
2. Selecciona la plantilla que necesitas (ej. calificar rúbricas o extraer cuestionarios).
3. Pega el prompt a la IA indicándole la URL de la tarea.
4. La IA levantará Playwright con la sesión guardada y completará la tarea sin que tengas que tocar la consola.

---

## 🔒 Seguridad y Privacidad (SAST Compliance)

- **Regla Estricta:** Ninguna contraseña, token JWT o cookie se incluye en los scripts.
- El archivo `.gitignore` excluye permanentemente:
  - Archivos de sesión (`*.json`, `sessions/*`).
  - Variables de entorno (`.env`).
  - Capturas de pantalla con información de estudiantes (`*.png`, `screenshots/`).
  - Reportes y descargas locales (`*.csv`, `*.xlsx`).
- Puedes compartir este repositorio públicamente en GitHub con total tranquilidad; el código es 100% agnóstico y portable.

---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Desarrollado para la optimización de procesos académicos y docencia universitaria.

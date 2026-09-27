# 🤖 Prompts Especializados para Delegar Tareas a IAs (Antigravity / Claude / ChatGPT)

Si eres un profesor, estudiante o profesional que no sabe programar en Python o no tiene tiempo de configurar scripts, puedes copiar y pegar estos prompts en tu asistente de Inteligencia Artificial (como **Antigravity**) para que ejecute la tarea por ti.

---

## 📋 Caso 1: Calificar Tareas de Moodle con Rúbrica Automática

> **Copia y pega este texto a tu IA:**
> 
> *"Hola Antigravity. Necesito calificar un lote de entregas en Moodle que tienen rúbrica analítica y me toma demasiado tiempo hacer clics en cada criterio. Por favor ejecuta el script de rúbricas del repositorio `playwright-academic-automator`:
> 
> 1. Abre el navegador con la sesión guardada en `sessions/moodle_auth.json`.
> 2. Navega a esta URL de calificación: `[PEGA_AQUÍ_LA_URL_DE_LA_TAREA_O_ESTUDIANTE]`
> 3. Aplica el perfil de calificación `max` (o el criterio que te indique).
> 4. Si los criterios coinciden con la entrega, guarda y avanza al siguiente estudiante.
> 5. Muéstrame un resumen con la tabla de criterios y el puntaje asignado."*

---

## 📝 Caso 2: Extraer Preguntas y Respuestas de un Examen de Moodle para Estudiar

> **Copia y pega este texto a tu IA:**
> 
> *"Hola Antigravity. He terminado un cuestionario en Moodle y quiero respaldar la revisión completa para estudiarla en mi bóveda de Obsidian.
> 
> 1. Usa el script `moodle/quiz_extractor.py`.
> 2. Extrae las preguntas, opciones múltiples, respuestas correctas y feedback de esta URL: `[PEGA_AQUÍ_LA_URL_DE_REVIEW.PHP]`
> 3. Guarda el archivo Markdown resultante en mi carpeta de notas académicas."*

---

## 🎓 Caso 3: Respaldar el Temario y Enlaces de un Curso de Udemy

> **Copia y pega este texto a tu IA:**
> 
> *"Hola Antigravity. Quiero un desglose en Markdown de todo el temario de mi curso en Udemy para planificar mi semana de estudio.
> 
> 1. Usa `udemy/course_scraper.py`.
> 2. Navega a este curso: `[PEGA_AQUÍ_LA_URL_DEL_CURSO]`
> 3. Despliega todas las secciones y genera un checklist en Markdown con cada clase y duración."*

---

## ⚙️ Caso 4: Configurar una Nueva Sesión sin Compartir Contraseñas

> **Copia y pega este texto a tu IA:**
> 
> *"Hola Antigravity. Quiero configurar mi sesión para `moodle` (o `sac` / `udemy`) usando `core/session_cli.py`:
> 
> 1. Lanza el comando `python -m core.session_cli --login moodle`.
> 2. Déjame la ventana abierta para que yo ingrese mi usuario, contraseña y 2FA de forma privada.
> 3. Cuando yo presione Enter en la consola, confirma que el archivo `moodle_auth.json` se guardó correctamente sin registrar mi contraseña en texto plano."*

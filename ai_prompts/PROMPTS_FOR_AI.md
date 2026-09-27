# 🤖 Instrucciones para Delegar Tareas a la IA (Antigravity / Claude / ChatGPT)

Este repositorio está diseñado para que cualquier docente o usuario **no tenga que programar ni tocar la terminal**. Simplemente clonas el repositorio en tu computador y le das instrucciones en lenguaje natural a un agente de Inteligencia Artificial (como **Antigravity**) para que se encargue de todo.

---

## 🔑 Las 3 Formas de Identificarte ante la IA

Para que la IA pueda navegar en tu Moodle, SAC o Udemy a calificar o extraer información, puedes darle acceso de cualquiera de estas 3 formas:

1. **Pasándole directamente la Cookie de Sesión (`MoodleSession`):**  
   Abres tu Moodle en el navegador, presionas `F12` (Herramientas de Desarrollador) -> pestaña *Application* (o *Almacenamiento*) -> *Cookies* -> copias el valor de `MoodleSession`.
2. **Usando el estado guardado (`sessions/moodle_auth.json`):**  
   Si previamente corriste `python -m core.session_cli --login moodle`.
3. **Pidiéndole a la IA que te abra la ventana de login:**  
   La IA lanzará el navegador en tu pantalla para que pongas tu usuario y contraseña con tranquilidad.

---

## 📋 Caso 1: Calificar Rúbrica en Moodle Pasándole un Archivo Excel

Si tienes las notas o criterios de tus estudiantes organizados en una hoja de cálculo (`.xlsx` o `.csv`):

> **Copia y pega este prompt a tu IA (ej. Antigravity):**
> 
> *"Hola Antigravity. Por favor lee el repositorio local clonado en mi máquina en:  
> `/ruta/donde/clonaste/playwright-academic-automator`  
> 
> Necesito que califiques una entrega con rúbrica en Moodle usando el script `moodle/rubric_grader.py`.  
> - **URL de la entrega:** `https://mi-universidad.edu.co/mod/assign/view.php?id=12345&action=grader`  
> - **Cookie de sesión:** `MoodleSession=TU_VALOR_AQUI` (o usa la sesión guardada en `sessions/moodle_auth.json`)  
> - **Archivo de notas:** Lee las calificaciones de mi archivo Excel ubicado en `/ruta/en/disco/mis_notas.xlsx`.  
> 
> Por favor abre el navegador con Playwright, haz clic en las casillas correspondientes de cada criterio según el Excel, guarda los cambios (`--auto-save`) y muéstrame una captura o tabla con los puntos asignados."*

---

## 🖼️ Caso 2: Calificar Rúbrica en Moodle Pasándole una Imagen

Si tienes una foto, captura de pantalla o PDF donde se ve la rúbrica marcada con las opciones deseadas:

> **Copia y pega este prompt a tu IA:**
> 
> *"Hola Antigravity. Mira la imagen adjunta donde se ven los criterios y niveles de la rúbrica que debo calificar.  
> 
> Por favor lee el script `moodle/rubric_grader.py` del repositorio clonado en mi disco y:  
> 1. Inyecta mi cookie de sesión: `MoodleSession=TU_VALOR_AQUI` (o usa `sessions/moodle_auth.json`).  
> 2. Navega a la entrega del estudiante: `[PEGA_AQUÍ_LA_URL_DE_CALIFICACIÓN]`.  
> 3. Identifica en la imagen qué opción corresponde a cada criterio (*Does the brochure contain all the required information?*, *Vocabulary*, etc.).  
> 4. Ejecuta los clics necesarios en la tabla de Moodle para marcar exactamente esos niveles.  
> 5. Guarda la calificación y confírmame el puntaje total obtenido."*

---

## ⚡ Caso 3: Calificar Rápido con Perfil Automático (Máximo, Medio o Mínimo)

Si quieres ponerle la nota máxima (o intermedia) a un trabajo excelente sin abrir Excel:

> **Copia y pega este prompt a tu IA:**
> 
> *"Antigravity, por favor califica esta entrega de Moodle con nota máxima en todos los criterios de la rúbrica:  
> - URL: `https://mi-universidad.edu.co/mod/assign/view.php?id=12345&action=grader`  
> - Cookie: `MoodleSession=TU_VALOR_AQUI`  
> 
> Ejecuta `python -m moodle.rubric_grader --grading-url URL --session COOKIE --profile max --auto-save` desde el repositorio local y confírmame cuando esté guardada."*

---

## 📥 Caso 4: Extraer Examen o Cuestionario de Moodle para Estudiar

> **Copia y pega este prompt a tu IA:**
> 
> *"Antigravity, por favor usa el script `moodle/quiz_extractor.py` del repositorio clonado en mi máquina para extraer todas las preguntas, respuestas correctas y explicaciones de esta revisión de Moodle:  
> - URL: `https://mi-universidad.edu.co/mod/quiz/review.php?attempt=67890`  
> - Cookie: `MoodleSession=TU_VALOR_AQUI`  
> 
> Guárdame el resultado en un archivo Markdown limpio en mi carpeta de notas académicas."*

# 📘 Guía Rápida para Docentes y Usuarios No Técnicos

¿Eres profesor o estudiante y estás cansado de hacer decenas de clics repetitivos en plataformas virtuales? Esta guía te explica cómo usar estas herramientas en **3 minutos** sin necesidad de saber programar.

---

## ⚡ El Problema de las Rúbricas en Moodle
Cuando calificas una tarea con rúbrica, Moodle te obliga a:
1. Abrir la entrega del estudiante.
2. Hacer scroll.
3. Buscar la fila del Criterio 1 y hacer clic en la casilla deseada (ej. *1.0 puntos*).
4. Buscar la fila del Criterio 2 y hacer clic.
5. Repetir lo mismo para 5, 8 o 10 criterios por cada estudiante.
6. Si tienes 40 estudiantes por grupo, **¡tienes que hacer entre 200 y 400 clics manuales por tarea!**

Esto satura la mano, fatiga la vista y gasta horas valiosas.

---

## 🚀 La Solución: ¿Cómo Automatizarlo en 3 Pasos?

### Paso 1: Instalar el Entorno (Solo se hace 1 vez)
Abre la terminal de tu computador y ejecuta:
```bash
git clone git@github.com:johanP051/playwright-academic-automator.git
cd playwright-academic-automator
python3 -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

---

### Paso 2: Conectar tu Cuenta de Moodle de Forma Segura
**Nunca** escribas tu contraseña en scripts ni se la des a nadie. Playwright usa un navegador real para que tú inicies sesión con tu cuenta institucional:

```bash
python -m core.session_cli --login moodle
```
1. Se abrirá una ventana de Chrome con la página oficial de tu universidad.
2. Ingresas tu usuario, contraseña y apruebas el código en tu celular (2FA / Microsoft Authenticator).
3. Una vez veas tu lista de cursos en la pantalla, vuelves a la ventana negra de la terminal y presionas **ENTER**.
4. ¡Listo! Tu sesión queda guardada localmente en tu propio computador.

---

### Paso 3: Calificar con Rúbrica con un Solo Comando

Copia el enlace de la entrega de Moodle que deseas calificar y corre:

```bash
python -m moodle.rubric_grader --grading-url "https://tu-moodle.edu.co/mod/assign/view.php?id=12345&action=grader" --profile max
```

#### ¿Qué hace el script por ti?
- Entra a la página del estudiante usando tu sesión.
- Lee automáticamente todos los criterios de la rúbrica (por ejemplo: *¿Contiene toda la información?, ¿Vocabulario pertinente?, etc.*).
- **Hace los clics en todas las casillas de la rúbrica de forma instantánea.**
- Puedes ver en tu pantalla cómo se marcan en verde todas las casillas en 1 segundo.
- Si le agregas `--auto-save`, guarda y avanza al siguiente estudiante automáticamente:
  ```bash
  python -m moodle.rubric_grader --grading-url "URL_DE_LA_TAREA" --profile max --auto-save
  ```

---

## 💡 ¿Y si prefiero que una Inteligencia Artificial lo haga por mí?
Si usas un asistente como **Antigravity**, **Claude** o **ChatGPT**:
1. Abre el archivo [`ai_prompts/PROMPTS_FOR_AI.md`](ai_prompts/PROMPTS_FOR_AI.md).
2. Copia la plantilla del caso que necesitas.
3. Pégasela a la IA pasándole la URL de tu tarea. La IA ejecutará el script en segundo plano y te devolverá el reporte listo.

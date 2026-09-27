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

### Paso 2: Conectar tu Cuenta de Moodle (Elige la opción que prefieras)

#### Opción A: Pasándole tu Cookie de Sesión Directa (La más rápida)
En tu navegador habitual con Moodle abierto:
1. Presiona `F12` para abrir las herramientas de desarrollador.
2. Ve a la pestaña **Application** (o **Almacenamiento**) -> **Cookies**.
3. Busca y copia el valor de `MoodleSession` (una cadena alfanumérica).
4. Ya puedes pasarle esa cookie al script con el parámetro `--session "MoodleSession=tu_cadena"`.

#### Opción B: Inicio de Sesión Interactivo (Guarda la sesión localmente)
```bash
python -m core.session_cli --login moodle
```
Se abrirá una ventana de Chrome. Ingresas tu usuario, contraseña y 2FA. Cuando veas tus cursos, vuelves a la terminal y presionas **ENTER**.

---

### Paso 3: Calificar con Rúbrica en Moodle

#### 1. Calificar con Nota Máxima Instantánea:
```bash
python -m moodle.rubric_grader --grading-url "URL_DE_LA_TAREA" --profile max --auto-save
```

#### 2. Calificar a partir de un archivo Excel de Notas:
Si tienes un archivo Excel con las notas o niveles por criterio:
```bash
python -m moodle.rubric_grader --grading-url "URL_DE_LA_TAREA" --excel "/ruta/a/mi_archivo_notas.xlsx" --auto-save
```

---

## 🤖 ¿Prefieres que una Inteligencia Artificial (Antigravity / Claude) lo haga por ti?

¡No necesitas ejecutar ningún comando! Puedes delegarle todo a la IA de la siguiente manera:

1. **Clona el repositorio en tu computador:** Anota la ruta donde quedó guardado (ej. `C:\Users\tu_usuario\playwright-academic-automator` o `/home/usuario/playwright-academic-automator`).
2. **Abre tu chat con la IA y dile:**
   > *"Hola. Tengo el repositorio clonado en `/ruta/local/playwright-academic-automator`.  
   > Necesito calificar la entrega de un estudiante en Moodle: `https://moodle.edu.co/mod/assign/view.php?id=12345&action=grader`.  
   > Mi cookie de sesión es `MoodleSession=xxxxxx`.  
   > 
   > **Opción A (Con Excel):** Aquí tienes la ruta de mi archivo Excel con las notas: `/ruta/a/notas.xlsx`.  
   > **Opción B (Con Imagen):** Te adjunto esta imagen donde se ve la rúbrica con las opciones que quiero marcar.  
   > 
   > Por favor usa el script `moodle/rubric_grader.py` para hacer los clics necesarios en la rúbrica y guarda la calificación."*

3. **La IA:**
   - Leerá el script local del repositorio.
   - Si le pasaste un Excel, extraerá las notas por criterio.
   - Si le pasaste una imagen, leerá visualmente la rúbrica y deducirá los niveles exactos a marcar.
   - Levantará Playwright inyectando tu cookie de sesión y ejecutará los clics en la rúbrica en segundos.
   - Te confirmará el puntaje total guardado.

# Proyecto de ejemplo: Lista de tareas (full-stack)

Este es el proyecto de ejemplo de la clase de vibe coding. Muestra, en su
versión más simple posible, las mismas piezas que van a usar en el
proyecto final:

- **Backend**: Python + Django, conectado a **PostgreSQL**.
- **API**: el backend expone datos en formato JSON (sin HTML).
- **Frontend**: HTML + CSS + JavaScript puro, que consume esa API con `fetch()`.

No usa Django REST Framework ni TypeScript a propósito: la idea es que se
vea el mecanismo "a mano" antes de sumar herramientas que lo automatizan.
Una vez que entiendan esto, agregar DRF o TypeScript en su propio proyecto
es un paso natural (está explicado en el manual completo).

## Estructura

```
proyecto-ejemplo/
├── backend/          <- Proyecto Django (API + conexión a PostgreSQL)
│   ├── config/        (settings, urls generales)
│   ├── tareas/         (la app: modelo, vistas, urls de la API)
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/         <- HTML + CSS + JS que consume la API
    ├── index.html
    ├── style.css
    └── script.js
```

## Cómo correrlo (paso a paso)

### 1. Base de datos

Con PostgreSQL instalado y corriendo:

```sql
CREATE USER app_user WITH PASSWORD 'app_pass123';
CREATE DATABASE tareas_db OWNER app_user;
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

El backend queda escuchando en `http://127.0.0.1:8000/`.
Probá la API directamente en el navegador: `http://127.0.0.1:8000/api/tareas/`
(al principio va a devolver una lista vacía: `[]`).

### 3. Frontend

Con el backend corriendo, abrí `frontend/index.html` con la extensión
**Live Server** de VS Code (click derecho → "Open with Live Server").

Si lo abrís así, va a quedar en una URL parecida a
`http://127.0.0.1:5500/index.html`, que es un "origen" distinto al del
backend (`8000`). Por eso el backend tiene CORS habilitado — sin eso,
el navegador bloquearía las peticiones.

### 4. Probar

Agregá una tarea desde el formulario, hacé click en el texto para
marcarla como hecha, y en la ✕ para borrarla. Cada una de esas acciones
dispara un `fetch()` en `script.js` que habla con la API de Django, que
a su vez lee y escribe en PostgreSQL.

## Por qué está armado así

Este mismo esqueleto (modelo → vista/API → fetch → pantalla) es el que
van a repetir para cada funcionalidad de su propio proyecto. El manual
completo de la clase explica el "algoritmo" paso a paso para no perderse.

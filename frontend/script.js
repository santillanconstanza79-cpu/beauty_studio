// ------------------------------------------------------------------
// Acá vive TODA la conexión con el backend Django.
// La idea clave: este archivo no sabe cómo se guardan los datos.
// Solo sabe pedirle cosas a esta URL usando fetch().
// ------------------------------------------------------------------
const API_URL = "http://127.0.0.1:8000/api/tareas/";

const lista = document.getElementById("lista-tareas");
const form = document.getElementById("form-nueva-tarea");
const input = document.getElementById("input-titulo");
const mensajeError = document.getElementById("mensaje-error");

function mostrarError(texto) {
  mensajeError.textContent = texto;
  mensajeError.hidden = false;
}

function ocultarError() {
  mensajeError.hidden = true;
}

// 1) LEER: pedirle al backend la lista de tareas y dibujarla en pantalla
async function cargarTareas() {
  try {
    ocultarError();
    const respuesta = await fetch(API_URL);

    if (!respuesta.ok) {
      throw new Error("El servidor respondió con un error");
    }

    const tareas = await respuesta.json();
    dibujarTareas(tareas);
  } catch (error) {
    // Este catch es el que se dispara, por ejemplo, si el backend
    // de Django no está corriendo o si hay un problema de CORS.
    console.error(error);
    mostrarError(
      "No se pudo conectar con el backend. ¿Está corriendo " +
        "'python manage.py runserver'?"
    );
  }
}

function dibujarTareas(tareas) {
  lista.innerHTML = "";

  if (tareas.length === 0) {
    lista.innerHTML = '<li class="vacio">No hay tareas todavía</li>';
    return;
  }

  tareas.forEach((tarea) => {
    const item = document.createElement("li");
    item.className = "tarea" + (tarea.hecha ? " hecha" : "");

    const texto = document.createElement("span");
    texto.textContent = tarea.titulo;
    texto.title = "Click para marcar como hecha / no hecha";
    texto.style.cursor = "pointer";
    texto.addEventListener("click", () => completarTarea(tarea.id));

    const botonBorrar = document.createElement("button");
    botonBorrar.textContent = "✕";
    botonBorrar.title = "Eliminar tarea";
    botonBorrar.addEventListener("click", () => eliminarTarea(tarea.id));

    item.appendChild(texto);
    item.appendChild(botonBorrar);
    lista.appendChild(item);
  });
}

// 2) CREAR: mandarle al backend una tarea nueva
async function crearTarea(titulo) {
  try {
    ocultarError();
    const respuesta = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ titulo }),
    });

    if (!respuesta.ok) {
      throw new Error("No se pudo crear la tarea");
    }

    await cargarTareas();
  } catch (error) {
    console.error(error);
    mostrarError("Ocurrió un error al crear la tarea.");
  }
}

// 3) ACTUALIZAR: marcar una tarea como hecha / no hecha
async function completarTarea(id) {
  try {
    ocultarError();
    const respuesta = await fetch(`${API_URL}${id}/`, { method: "PATCH" });

    if (!respuesta.ok) {
      throw new Error("No se pudo actualizar la tarea");
    }

    await cargarTareas();
  } catch (error) {
    console.error(error);
    mostrarError("Ocurrió un error al actualizar la tarea.");
  }
}

// 4) BORRAR: eliminar una tarea
async function eliminarTarea(id) {
  try {
    ocultarError();
    const respuesta = await fetch(`${API_URL}${id}/`, { method: "DELETE" });

    if (!respuesta.ok) {
      throw new Error("No se pudo eliminar la tarea");
    }

    await cargarTareas();
  } catch (error) {
    console.error(error);
    mostrarError("Ocurrió un error al eliminar la tarea.");
  }
}

form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  const titulo = input.value.trim();
  if (!titulo) return;

  crearTarea(titulo);
  input.value = "";
});

// Al abrir la página, mostramos las tareas que ya existan en la base
cargarTareas();

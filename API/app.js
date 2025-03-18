const baseURL = "http://127.0.0.1:8000";

async function realizarSolicitud(endpoint, opciones = {}) {
    try {
        const respuesta = await fetch(`${baseURL}${endpoint}`, opciones);
        if (!respuesta.ok) {
            throw new Error(`Error: ${respuesta.status} - ${respuesta.statusText}`);
        }
        return await respuesta.json();
    } catch (error) {
        console.error(`Error al realizar la solicitud a ${endpoint}:`, error);
        throw error;
    }
}

async function obtenerJugadores() {
    return await realizarSolicitud("/jugadores/listado");
}

function mostrarJugadoresEnLista(jugadores) {
    const listaJugadores = document.getElementById("listaJugadores");
    if (!listaJugadores) {
        console.error("No se encontró el elemento con ID 'listaJugadores'");
        return;
    }

    listaJugadores.innerHTML = "";

    jugadores.forEach(jugador => {
        const li = document.createElement("li");
        li.textContent = `${jugador.nombre} ${jugador.apellido} (${jugador.numero_camiseta}) - ${jugador.equipo || "Sin equipo"}, ${jugador.posicion}, ${jugador.edad} años`;
        listaJugadores.appendChild(li);
    });
}

async function gestionarJugador(metodo, endpoint, jugador = null) {
    const opciones = {
        method: metodo,
        headers: { "Content-Type": "application/json" },
    };
    if (jugador) {
        opciones.body = JSON.stringify(jugador);
    }
    return await realizarSolicitud(endpoint, opciones);
}

async function cargarJugadores() {
    try {
        const jugadores = await obtenerJugadores();
        mostrarJugadoresEnLista(jugadores);
    } catch (error) {
        console.error("Error al cargar jugadores:", error);
    }
}

document.getElementById("formCrearJugador").addEventListener("submit", async (e) => {
    e.preventDefault();
    const jugador = {
        nombre: document.getElementById("nombre").value,
        apellido: document.getElementById("apellido").value,
        numero_camiseta: parseInt(document.getElementById("numeroCamiseta").value),
        equipo: document.getElementById("equipo").value,
        posicion: document.getElementById("posicion").value,
        edad: parseInt(document.getElementById("edad").value),
    };

    try {
        await gestionarJugador("POST", "/jugadores", jugador);
        await cargarJugadores();
        document.getElementById("formCrearJugador").reset();
    } catch (error) {
        console.error("Error al crear jugador:", error);
    }
});

document.getElementById("modificarJugadorButton").addEventListener("click", async () => {
    const numeroCamiseta = parseInt(document.getElementById("numeroCamisetaModificar").value);
    const jugador = {
        nombre: document.getElementById("nombreModificar").value,
        apellido: document.getElementById("apellidoModificar").value,
        numero_camiseta: numeroCamiseta,
        equipo: document.getElementById("equipoModificar").value,
        posicion: document.getElementById("posicionModificar").value,
        edad: parseInt(document.getElementById("edadModificar").value),
    };

    try {
        await gestionarJugador("PUT", `/jugadores/${numeroCamiseta}`, jugador);
        await cargarJugadores();
        document.getElementById("formModificarJugador").reset();
    } catch (error) {
        console.error("Error al modificar jugador:", error);
    }
});

document.getElementById("eliminarJugadorButton").addEventListener("click", async () => {
    const numeroCamiseta = parseInt(document.getElementById("numeroCamisetaEliminar").value);

    try {
        await gestionarJugador("DELETE", `/jugadores/${numeroCamiseta}`);
        await cargarJugadores();
        document.getElementById("numeroCamisetaEliminar").value = "";
    } catch (error) {
        console.error("Error al eliminar jugador:", error);
    }
});

window.onload = cargarJugadores;

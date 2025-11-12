/**
 * API de Música - Frontend JavaScript
 * Gestiona la interacción con la API y actualización de la interfaz
 * Autor: Jhon Salcedo (@jasl89)
 */

const API_BASE_URL = 'http://localhost:8000/api';

// =============================================================================
// FUNCIONES DE UTILIDAD
// =============================================================================

/**
 * Realiza una petición HTTP a la API
 */
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en la petición');
        }

        // Si es DELETE, no hay contenido que parsear
        if (method === 'DELETE') {
            return { success: true };
        }

        return await response.json();
    } catch (error) {
        console.error('Error en la petición:', error);
        mostrarAlerta(error.message, 'danger');
        throw error;
    }
}

/**
 * Muestra un mensaje de alerta temporal
 */
function mostrarAlerta(mensaje, tipo = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Formatea la duración en segundos a MM:SS
 */
function formatearDuracion(segundos) {
    const minutos = Math.floor(segundos / 60);
    const segs = segundos % 60;
    return `${minutos}:${segs.toString().padStart(2, '0')}`;
}

// =============================================================================
// GESTIÓN DE USUARIOS
// =============================================================================

async function cargarUsuarios() {
    try {
        const usuarios = await apiRequest('/usuarios/');

        // Actualizar estadística
        document.getElementById('total-usuarios').textContent = usuarios.length;

        // Actualizar lista de usuarios
        const listaUsuarios = document.getElementById('lista-usuarios');
        if (usuarios.length === 0) {
            listaUsuarios.innerHTML = '<li class="list-group-item text-center text-muted">No hay usuarios registrados</li>';
            return;
        }

        listaUsuarios.innerHTML = usuarios.map(usuario => `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>${usuario.nombre}</strong><br>
                    <small class="text-muted">
                        <i class="fas fa-envelope"></i> ${usuario.correo}
                    </small><br>
                    <small class="text-muted">
                        <i class="fas fa-calendar"></i> ${new Date(usuario.fecha_registro).toLocaleDateString('es-ES')}
                    </small>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="eliminarUsuario(${usuario.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </li>
        `).join('');

        // Actualizar selectores de favoritos
        actualizarSelectoresUsuarios(usuarios);

    } catch (error) {
        console.error('Error al cargar usuarios:', error);
    }
}

async function crearUsuario(event) {
    event.preventDefault();

    const nombre = document.getElementById('usuario-nombre').value;
    const correo = document.getElementById('usuario-correo').value;

    try {
        await apiRequest('/usuarios/', 'POST', { nombre, correo });
        mostrarAlerta('Usuario registrado exitosamente', 'success');

        // Limpiar formulario
        document.getElementById('form-usuario').reset();

        // Recargar lista
        await cargarUsuarios();
    } catch (error) {
        console.error('Error al crear usuario:', error);
    }
}

async function eliminarUsuario(id) {
    if (!confirm('¿Está seguro de eliminar este usuario? Se eliminarán también sus favoritos.')) {
        return;
    }

    try {
        await apiRequest(`/usuarios/${id}`, 'DELETE');
        mostrarAlerta('Usuario eliminado exitosamente', 'info');
        await cargarUsuarios();
    } catch (error) {
        console.error('Error al eliminar usuario:', error);
    }
}

function actualizarSelectoresUsuarios(usuarios) {
    const selectFavorito = document.getElementById('favorito-usuario');
    const selectVerFavoritos = document.getElementById('ver-favoritos-usuario');

    const opciones = usuarios.map(u =>
        `<option value="${u.id}">${u.nombre} (${u.correo})</option>`
    ).join('');

    selectFavorito.innerHTML = '<option value="">Seleccione un usuario...</option>' + opciones;
    selectVerFavoritos.innerHTML = '<option value="">Seleccione un usuario...</option>' + opciones;
}

// =============================================================================
// GESTIÓN DE CANCIONES
// =============================================================================

async function cargarCanciones() {
    try {
        const canciones = await apiRequest('/canciones/');

        // Actualizar estadística
        document.getElementById('total-canciones').textContent = canciones.length;

        // Actualizar lista de canciones
        const listaCanciones = document.getElementById('lista-canciones');
        if (canciones.length === 0) {
            listaCanciones.innerHTML = '<li class="list-group-item text-center text-muted">No hay canciones en el catálogo</li>';
            return;
        }

        listaCanciones.innerHTML = canciones.map(cancion => `
            <li class="list-group-item cancion-item" data-titulo="${cancion.titulo}" data-artista="${cancion.artista}">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-1"><i class="fas fa-music"></i> ${cancion.titulo}</h6>
                        <p class="mb-1"><strong>Artista:</strong> ${cancion.artista}</p>
                        ${cancion.album ? `<p class="mb-1"><small><strong>Álbum:</strong> ${cancion.album}</small></p>` : ''}
                        <div class="d-flex gap-2 flex-wrap">
                            <span class="badge badge-custom">
                                <i class="fas fa-clock"></i> ${formatearDuracion(cancion.duracion)}
                            </span>
                            ${cancion.año ? `<span class="badge badge-custom"><i class="fas fa-calendar"></i> ${cancion.año}</span>` : ''}
                            ${cancion.genero ? `<span class="badge badge-custom"><i class="fas fa-guitar"></i> ${cancion.genero}</span>` : ''}
                        </div>
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="eliminarCancion(${cancion.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </li>
        `).join('');

        // Actualizar selector de favoritos
        actualizarSelectorCanciones(canciones);

    } catch (error) {
        console.error('Error al cargar canciones:', error);
    }
}

async function crearCancion(event) {
    event.preventDefault();

    const titulo = document.getElementById('cancion-titulo').value;
    const artista = document.getElementById('cancion-artista').value;
    const album = document.getElementById('cancion-album').value || null;
    const duracion = parseInt(document.getElementById('cancion-duracion').value);
    const año = document.getElementById('cancion-año').value ? parseInt(document.getElementById('cancion-año').value) : null;
    const genero = document.getElementById('cancion-genero').value || null;

    try {
        await apiRequest('/canciones/', 'POST', {
            titulo, artista, album, duracion, año, genero
        });
        mostrarAlerta('Canción agregada exitosamente', 'success');

        // Limpiar formulario
        document.getElementById('form-cancion').reset();

        // Recargar lista
        await cargarCanciones();
    } catch (error) {
        console.error('Error al crear canción:', error);
    }
}

async function eliminarCancion(id) {
    if (!confirm('¿Está seguro de eliminar esta canción? Se eliminará también de los favoritos.')) {
        return;
    }

    try {
        await apiRequest(`/canciones/${id}`, 'DELETE');
        mostrarAlerta('Canción eliminada exitosamente', 'info');
        await cargarCanciones();
    } catch (error) {
        console.error('Error al eliminar canción:', error);
    }
}

function actualizarSelectorCanciones(canciones) {
    const selectCancion = document.getElementById('favorito-cancion');

    const opciones = canciones.map(c =>
        `<option value="${c.id}">${c.titulo} - ${c.artista}</option>`
    ).join('');

    selectCancion.innerHTML = '<option value="">Seleccione una canción...</option>' + opciones;
}

// Filtro de búsqueda para canciones
document.getElementById('filtro-canciones')?.addEventListener('input', (e) => {
    const filtro = e.target.value.toLowerCase();
    const canciones = document.querySelectorAll('.cancion-item');

    canciones.forEach(cancion => {
        const titulo = cancion.dataset.titulo.toLowerCase();
        const artista = cancion.dataset.artista.toLowerCase();

        if (titulo.includes(filtro) || artista.includes(filtro)) {
            cancion.style.display = '';
        } else {
            cancion.style.display = 'none';
        }
    });
});

// =============================================================================
// GESTIÓN DE FAVORITOS
// =============================================================================

async function cargarFavoritos() {
    try {
        const favoritos = await apiRequest('/favoritos/');

        // Actualizar estadística
        document.getElementById('total-favoritos').textContent = favoritos.length;

    } catch (error) {
        console.error('Error al cargar favoritos:', error);
    }
}

async function cargarFavoritosUsuario() {
    const usuarioId = document.getElementById('ver-favoritos-usuario').value;
    const container = document.getElementById('lista-favoritos-container');

    if (!usuarioId) {
        container.innerHTML = `
            <div class="alert alert-custom">
                <i class="fas fa-info-circle"></i> Seleccione un usuario para ver sus canciones favoritas
            </div>
        `;
        return;
    }

    try {
        const favoritos = await apiRequest(`/favoritos/usuario/${usuarioId}`);

        if (favoritos.length === 0) {
            container.innerHTML = `
                <div class="alert alert-custom">
                    <i class="fas fa-heart-broken"></i> Este usuario no tiene canciones favoritas aún
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <ul class="list-group">
                ${favoritos.map(fav => `
                    <li class="list-group-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <h6 class="mb-1">
                                    <i class="fas fa-heart text-danger"></i> ${fav.cancion.titulo}
                                </h6>
                                <p class="mb-1"><strong>Artista:</strong> ${fav.cancion.artista}</p>
                                <div class="d-flex gap-2 flex-wrap">
                                    <span class="badge badge-custom">
                                        <i class="fas fa-clock"></i> ${formatearDuracion(fav.cancion.duracion)}
                                    </span>
                                    ${fav.cancion.genero ? `<span class="badge badge-custom"><i class="fas fa-guitar"></i> ${fav.cancion.genero}</span>` : ''}
                                </div>
                                <small class="text-muted">
                                    <i class="fas fa-calendar-plus"></i> Agregado: ${new Date(fav.fecha_agregado).toLocaleDateString('es-ES')}
                                </small>
                            </div>
                            <button class="btn btn-sm btn-outline-danger" onclick="eliminarFavorito(${fav.id})">
                                <i class="fas fa-heart-broken"></i>
                            </button>
                        </div>
                    </li>
                `).join('')}
            </ul>
        `;

    } catch (error) {
        console.error('Error al cargar favoritos del usuario:', error);
    }
}

async function agregarFavorito(event) {
    event.preventDefault();

    const usuario_id = parseInt(document.getElementById('favorito-usuario').value);
    const cancion_id = parseInt(document.getElementById('favorito-cancion').value);

    if (!usuario_id || !cancion_id) {
        mostrarAlerta('Debe seleccionar un usuario y una canción', 'warning');
        return;
    }

    try {
        await apiRequest('/favoritos/', 'POST', { usuario_id, cancion_id });
        mostrarAlerta('Canción agregada a favoritos exitosamente', 'success');

        // Limpiar formulario
        document.getElementById('form-favorito').reset();

        // Recargar estadística
        await cargarFavoritos();

        // Si hay un usuario seleccionado en ver favoritos, recargar su lista
        const verUsuarioId = document.getElementById('ver-favoritos-usuario').value;
        if (verUsuarioId == usuario_id) {
            await cargarFavoritosUsuario();
        }

    } catch (error) {
        console.error('Error al agregar favorito:', error);
    }
}

async function eliminarFavorito(id) {
    if (!confirm('¿Está seguro de eliminar este favorito?')) {
        return;
    }

    try {
        await apiRequest(`/favoritos/${id}`, 'DELETE');
        mostrarAlerta('Favorito eliminado exitosamente', 'info');
        await cargarFavoritos();
        await cargarFavoritosUsuario();
    } catch (error) {
        console.error('Error al eliminar favorito:', error);
    }
}

// =============================================================================
// INICIALIZACIÓN Y EVENTOS
// =============================================================================

function cargarDatos() {
    cargarUsuarios();
    cargarCanciones();
    cargarFavoritos();
}

// Event listeners para formularios
document.getElementById('form-usuario').addEventListener('submit', crearUsuario);
document.getElementById('form-cancion').addEventListener('submit', crearCancion);
document.getElementById('form-favorito').addEventListener('submit', agregarFavorito);

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', cargarDatos);

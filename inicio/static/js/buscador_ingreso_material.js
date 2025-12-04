// Variables globales
let modalProveedorInstance = null;
let toastProveedor = null;
let todosLosMateriales = [];

function inicializarIngresoMaterial() {
    // Inicializar modales y toasts
    const modalProveedorElement = document.getElementById('modalProveedor');
    if (modalProveedorElement) {
        modalProveedorInstance = new bootstrap.Modal(modalProveedorElement);
    }
    
    const toastProveedorElement = document.getElementById('toastProveedor');
    if (toastProveedorElement) {
        toastProveedor = new bootstrap.Toast(toastProveedorElement);
    }
    
    // Configurar event listeners
    configurarEventListenersIngreso();
    
    // Cargar datos iniciales
    cargarProveedores();
    cargarTodosLosMateriales();
}

function configurarEventListenersIngreso() {
    // Botón para abrir modal de proveedor
    const btnAbrirModalProveedor = document.getElementById('btnAbrirModalProveedor');
    if (btnAbrirModalProveedor) {
        btnAbrirModalProveedor.addEventListener('click', function(e) {
            e.preventDefault();
            abrirModalProveedor();
        });
    }
    
    // Botón para guardar proveedor
    const btnGuardarProveedor = document.getElementById('btnGuardarProveedor');
    if (btnGuardarProveedor) {
        btnGuardarProveedor.addEventListener('click', crearProveedor);
    }
    
    // BÚSQUEDA AUTOMÁTICA AL ESCRIBIR - SIMPLIFICADO
    const buscarMaterial = document.getElementById('buscarMaterial');
    
    if (buscarMaterial) {
        // Búsqueda automática mientras se escribe
        buscarMaterial.addEventListener('input', function(e) {
            const termino = this.value.trim();
            buscarMaterialesLocalmente(termino);
        });
        
        // Limpiar búsqueda con Escape (opcional)
        buscarMaterial.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
                buscarMaterialesLocalmente('');
                this.blur();
            }
        });
        
        // Enfocar el buscador automáticamente
        buscarMaterial.focus();
    }
    
    // Botón para registrar ingreso completo
    const btnRegistrarIngreso = document.getElementById('btnRegistrarIngreso');
    if (btnRegistrarIngreso) {
        btnRegistrarIngreso.addEventListener('click', registrarIngresoCompleto);
    }
}

function cargarTodosLosMateriales() {
    const listaMateriales = document.getElementById('listaMateriales');
    if (!listaMateriales) return;
    
    listaMateriales.innerHTML = '<div class="text-center text-muted py-4"><div class="spinner-border spinner-border-sm me-2" role="status"></div> Cargando materiales...</div>';
    
    fetch('/materiales/materiales/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                todosLosMateriales = data.materiales;
                actualizarListaMateriales(todosLosMateriales);
            } else {
                mostrarErrorListaMateriales('Error al cargar materiales');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarErrorListaMateriales('Error de conexión');
        });
}

function buscarMaterialesLocalmente(termino = '') {
    let materialesFiltrados;
    
    if (!termino) {
        // Si está vacío, mostrar todos los materiales
        materialesFiltrados = todosLosMateriales;
    } else {
        // Filtrar materiales localmente
        materialesFiltrados = todosLosMateriales.filter(material => {
            const busqueda = termino.toLowerCase();
            
            // Buscar en múltiples campos
            return (
                material.descripcion.toLowerCase().includes(busqueda) ||
                material.codigo_material.toLowerCase().includes(busqueda) ||
                (material.partida__partida && material.partida__partida.toLowerCase().includes(busqueda)) ||
                (material.partida__categoria && material.partida__categoria.toLowerCase().includes(busqueda)) ||
                (material.unidad_ingreso && material.unidad_ingreso.toLowerCase().includes(busqueda))
            );
        });
    }
    
    actualizarListaMateriales(materialesFiltrados, termino);
}

function actualizarListaMateriales(materiales, busqueda = '') {
    const listaMateriales = document.getElementById('listaMateriales');
    if (!listaMateriales) return;
    
    if (materiales.length === 0) {
        const mensaje = busqueda 
            ? `No se encontraron materiales para "${busqueda}"`
            : 'No hay materiales disponibles';
        
        listaMateriales.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-search fa-2x mb-3"></i>
                <p class="mb-0">${mensaje}</p>
                ${busqueda ? '<small class="text-muted">Intente con otros términos de búsqueda</small>' : ''}
            </div>
        `;
        return;
    }
    
    let html = '';
    materiales.forEach(material => {
        const yaSeleccionado = materialesSeleccionados.some(m => m.id === material.id);
        const claseSeleccionado = yaSeleccionado ? 'material-selected border-success' : '';
        const textoBoton = yaSeleccionado ? '✓ Seleccionado' : 'Ingresar';
        const claseBoton = yaSeleccionado ? 'btn-success' : 'btn-warning';
        
        // Resaltar coincidencias si hay búsqueda
        const descripcionResaltada = busqueda ? this.resaltarCoincidencias(material.descripcion, busqueda) : this.escapeHtml(material.descripcion);
        const codigoResaltado = busqueda ? this.resaltarCoincidencias(material.codigo_material, busqueda) : this.escapeHtml(material.codigo_material);
        
        html += `
            <div class="card material-card shadow-sm p-3 mb-2 ${claseSeleccionado}" 
                 data-material-id="${material.id}" 
                 onclick="seleccionarMaterial(${material.id}, '${this.escapeHtml(material.codigo_material)}', '${this.escapeHtml(material.descripcion)}', '${this.escapeHtml(material.unidad_ingreso)}', '${this.escapeHtml(material.volumen)}', ${material.cantidad_x_unidad_ingreso})"
                 style="cursor: pointer; transition: all 0.2s;">
                <div class="row g-3 align-items-center">
                    <div class="col-md-9 col-8">
                        <h6 class="fw-bold mb-1">${descripcionResaltada}</h6>
                        <span class="text-muted small d-block mb-1">Código: ${codigoResaltado}</span>
                        <span class="text-muted small d-block">Partida: ${this.escapeHtml(material.partida__partida)} - ${this.escapeHtml(material.partida__categoria)}</span>
                        <span class="badge bg-light text-dark small">Unidad: ${this.escapeHtml(material.unidad_ingreso)}</span>
                    </div>
                    <div class="col-md-3 text-md-end text-center">
                        <button class="btn ${claseBoton} mt-2 px-3 fw-semibold" onclick="event.stopPropagation();">
                            ${textoBoton}
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    listaMateriales.innerHTML = html;
}

// Función para resaltar coincidencias en el texto
function resaltarCoincidencias(texto, busqueda) {
    if (!busqueda) return this.escapeHtml(texto);
    
    const textoEscapeado = this.escapeHtml(texto);
    const busquedaEscapeada = this.escapeHtml(busqueda);
    
    const regex = new RegExp(`(${busquedaEscapeada.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    
    return textoEscapeado.replace(regex, '<mark class="bg-warning px-1 rounded">$1</mark>');
}

function mostrarErrorListaMateriales(mensaje) {
    const listaMateriales = document.getElementById('listaMateriales');
    if (!listaMateriales) return;
    
    listaMateriales.innerHTML = `
        <div class="text-center text-danger py-4">
            <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
            <p class="mb-1">${mensaje}</p>
            <button class="btn btn-sm btn-outline-primary mt-2" onclick="cargarTodosLosMateriales()">
                <i class="fas fa-redo"></i> Reintentar
            </button>
        </div>
    `;
}

// Función auxiliar para escapar HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Asignar funciones al objeto global
window.escapeHtml = escapeHtml;
window.resaltarCoincidencias = resaltarCoincidencias;

// Las demás funciones permanecen igual...
function seleccionarMaterial(id, codigo, descripcion, unidad, volumen, cantidadPorUnidad) {
    const index = materialesSeleccionados.findIndex(m => m.id === id);
    
    if (index === -1) {
        materialesSeleccionados.push({
            id: id,
            codigo_material: codigo,
            descripcion: descripcion,
            unidad_ingreso: unidad,
            volumen: volumen,
            cantidad_x_unidad_ingreso: cantidadPorUnidad,
            cantidad: 1
        });
        
        actualizarTablaMateriales();
        actualizarListaMaterialesUI();
        mostrarFeedbackSeleccion(id);
    }
}

function actualizarListaMaterialesUI() {
    const buscarMaterial = document.getElementById('buscarMaterial');
    const termino = buscarMaterial ? buscarMaterial.value.trim() : '';
    buscarMaterialesLocalmente(termino);
}

function mostrarFeedbackSeleccion(materialId) {
    const card = document.querySelector(`[data-material-id="${materialId}"]`);
    if (card) {
        card.classList.add('material-selected', 'border-success');
        const boton = card.querySelector('button');
        if (boton) {
            boton.classList.remove('btn-warning');
            boton.classList.add('btn-success');
            boton.textContent = '✓ Seleccionado';
        }
    }
}

// ... el resto de tus funciones existentes (cargarProveedores, crearProveedor, etc.)
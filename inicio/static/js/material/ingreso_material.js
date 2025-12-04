document.addEventListener('DOMContentLoaded', function() {
    console.log('ingreso_material.js cargado correctamente');
    inicializarIngresoMaterial();
});

// Variables globales
let materialesSeleccionados = [];
let modalProveedorInstance = null;
let toastProveedor = null;

// Manejo de almacenes
let modalAlmacenInstance = null;
let toastAlmacen = null;

// Manejo de partidas (submodal)
let modalPartidaInstance = null;
let toastPartida = null;

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

    // Almacén
    const modalAlmacenElement = document.getElementById('modalAlmacen');
    if (modalAlmacenElement) {
        modalAlmacenInstance = new bootstrap.Modal(modalAlmacenElement);
    }

    const toastAlmacenElement = document.getElementById('toastAlmacen');
    if (toastAlmacenElement) {
        toastAlmacen = new bootstrap.Toast(toastAlmacenElement);
    }

    // Partida (submodal dentro del modal de material)
    const modalPartidaElement = document.getElementById('modalPartida');
    if (modalPartidaElement) {
        modalPartidaInstance = bootstrap.Modal.getOrCreateInstance(modalPartidaElement);
        console.log('Modal de partida inicializado');
    } else {
        console.warn('No se encontró #modalPartida en el DOM');
    }

    const toastPartidaElement = document.getElementById('toastPartida');
    if (toastPartidaElement) {
        toastPartida = new bootstrap.Toast(toastPartidaElement);
    }
    
    // Configurar event listeners
    configurarEventListenersIngreso();
    
    // Cargar datos iniciales
    cargarProveedores();
    cargarAlmacenes();
    cargarMateriales();
    cargarPartidas(); // para el select del modal de material
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

    // Botón para abrir modal de almacén
    const btnAbrirModalAlmacen = document.getElementById('btnAbrirModalAlmacen');
    if (btnAbrirModalAlmacen) {
        btnAbrirModalAlmacen.addEventListener('click', function(e) {
            e.preventDefault();
            abrirModalAlmacen();
        });
    }

    // Botón para guardar almacén
    const btnGuardarAlmacen = document.getElementById('btnGuardarAlmacen');
    if (btnGuardarAlmacen) {
        btnGuardarAlmacen.addEventListener('click', crearAlmacen);
    }

    // Botón para abrir submodal de partida (dentro del modal de material)
    const btnAbrirModalPartida = document.getElementById('btnAbrirModalPartida');
    if (btnAbrirModalPartida) {
        console.log('Encontrado botón #btnAbrirModalPartida');
        btnAbrirModalPartida.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Click en botón de abrir modal de partida');
            abrirModalPartida();
        });
    } else {
        console.warn('No se encontró #btnAbrirModalPartida');
    }

    // Botón para guardar partida (submodal)
    const btnGuardarPartida = document.getElementById('btnGuardarPartida');
    if (btnGuardarPartida) {
        btnGuardarPartida.addEventListener('click', crearPartida);
    }
    
    // Búsqueda de materiales
    const btnBuscarMaterial = document.getElementById('btnBuscarMaterial');
    const buscarMaterial = document.getElementById('buscarMaterial');
    
    if (btnBuscarMaterial) {
        btnBuscarMaterial.addEventListener('click', function() {
            cargarMateriales(buscarMaterial.value);
        });
    }
    
    if (buscarMaterial) {
        buscarMaterial.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                cargarMateriales(this.value);
            }
        });
    }
    
    // Botón para registrar ingreso completo
    const btnRegistrarIngreso = document.getElementById('btnRegistrarIngreso');
    if (btnRegistrarIngreso) {
        btnRegistrarIngreso.addEventListener('click', registrarIngresoCompleto);
    }
}

function cargarProveedores() {
    const selectProveedor = document.getElementById('selectProveedor');
    if (!selectProveedor) return;
    
    fetch('/materiales/proveedores/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarSelectProveedores(data.proveedores);
            } else {
                console.error('Error al cargar proveedores:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function actualizarSelectProveedores(proveedores) {
    const selectProveedor = document.getElementById('selectProveedor');
    if (!selectProveedor) return;
    
    selectProveedor.innerHTML = '<option value="" selected disabled>Seleccionar proveedor...</option>';
    
    if (proveedores.length === 0) {
        selectProveedor.innerHTML += '<option value="" disabled>No hay proveedores disponibles</option>';
        return;
    }
    
    proveedores.forEach(proveedor => {
        const option = document.createElement('option');
        option.value = proveedor.id;
        option.textContent = `${proveedor.proveedor} - NIT: ${proveedor.nit}`;
        selectProveedor.appendChild(option);
    });
}

// =======================
// ALMACENES
// =======================

function cargarAlmacenes() {
    const selectAlmacen = document.getElementById('selectAlmacen');
    if (!selectAlmacen) return;
    
    fetch('/materiales/almacenes/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarSelectAlmacenes(data.almacenes);
            } else {
                console.error('Error al cargar almacenes:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function actualizarSelectAlmacenes(almacenes) {
    const selectAlmacen = document.getElementById('selectAlmacen');
    if (!selectAlmacen) return;
    
    selectAlmacen.innerHTML = '<option value="" selected disabled>Seleccionar almacén...</option>';
    
    if (almacenes.length === 0) {
        selectAlmacen.innerHTML += '<option value="" disabled>No hay almacenes disponibles</option>';
        return;
    }
    
    almacenes.forEach(almacen => {
        const option = document.createElement('option');
        option.value = almacen.id;
        option.textContent = `Nro: ${almacen.nro_almacen} - ${almacen.descripcion}`;
        selectAlmacen.appendChild(option);
    });
}

function abrirModalAlmacen() {
    if (modalAlmacenInstance) {
        const nro = document.getElementById('almacen_nro');
        const desc = document.getElementById('almacen_descripcion');
        const ubi = document.getElementById('almacen_ubicacion');

        if (nro) { nro.value = ''; nro.classList.remove('is-invalid'); }
        if (desc) { desc.value = ''; desc.classList.remove('is-invalid'); }
        if (ubi) { ubi.value = ''; ubi.classList.remove('is-invalid'); }

        modalAlmacenInstance.show();
    }
}

function crearAlmacen() {
    const nroAlmacen = document.getElementById('almacen_nro').value.trim();
    const descripcion = document.getElementById('almacen_descripcion').value.trim();
    const ubicacion = document.getElementById('almacen_ubicacion').value.trim();
    
    if (!nroAlmacen) {
        mostrarErrorCampo('almacen_nro', 'El número de almacén es requerido');
        return;
    }
    if (!descripcion) {
        mostrarErrorCampo('almacen_descripcion', 'La descripción es requerida');
        return;
    }
    if (!ubicacion) {
        mostrarErrorCampo('almacen_ubicacion', 'La ubicación es requerida');
        return;
    }

    const formData = {
        nro_almacen: nroAlmacen,
        descripcion: descripcion,
        ubicacion: ubicacion
    };
    
    const btnGuardar = document.getElementById('btnGuardarAlmacen');
    const originalText = btnGuardar.innerHTML;
    btnGuardar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Guardando...';
    btnGuardar.disabled = true;
    
    fetch('/materiales/crear-almacen/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (modalAlmacenInstance) {
                modalAlmacenInstance.hide();
            }
            
            cargarAlmacenes();
            
            setTimeout(() => {
                const selectAlmacen = document.getElementById('selectAlmacen');
                if (selectAlmacen) {
                    selectAlmacen.value = data.almacen.id;
                }
            }, 300);
            
            mostrarToastAlmacen('Almacén agregado exitosamente', 'success');
        } else {
            mostrarToastAlmacen('Error al crear almacén: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarToastAlmacen('Error al comunicarse con el servidor', 'error');
    })
    .finally(() => {
        btnGuardar.innerHTML = originalText;
        btnGuardar.disabled = false;
    });
}

function mostrarToastAlmacen(mensaje, tipo = 'success') {
    const toastElement = document.getElementById('toastAlmacen');
    const toastMessage = document.getElementById('toastAlmacenMessage');

    if (!toastElement || !toastMessage || !toastAlmacen) return;

    const header = toastElement.querySelector('.toast-header');
    const icon = header ? header.querySelector('i') : null;
    const title = header ? header.querySelector('strong') : null;

    if (tipo === 'error') {
        if (icon) icon.className = 'fas fa-exclamation-triangle text-danger me-2';
        if (title) title.textContent = 'Error';
    } else {
        if (icon) icon.className = 'fas fa-check-circle text-success me-2';
        if (title) title.textContent = 'Éxito';
    }

    toastMessage.textContent = mensaje;
    toastAlmacen.show();
}

// =======================
// PARTIDAS (SUBMODAL)
// =======================

function cargarPartidas() {
    const selectPartida = document.getElementById('selectPartida');
    if (!selectPartida) return;

    fetch('/materiales/partidas-presupuestarias/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarSelectPartidas(data.partidas);
            } else {
                console.error('Error al cargar partidas:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function actualizarSelectPartidas(partidas) {
    const selectPartida = document.getElementById('selectPartida');
    if (!selectPartida) return;

    selectPartida.innerHTML = '<option value="" selected disabled>Seleccionar partida...</option>';

    if (!partidas || partidas.length === 0) {
        selectPartida.innerHTML += '<option value="" disabled>No hay partidas disponibles</option>';
        return;
    }

    partidas.forEach(partida => {
        const option = document.createElement('option');
        option.value = partida.id;
        option.textContent = `${partida.partida} - ${partida.categoria}`;
        selectPartida.appendChild(option);
    });
}

function abrirModalPartida() {
    console.log('Intentando abrir modal de partida...');
    const modalPartidaElement = document.getElementById('modalPartida');

    if (!modalPartidaElement) {
        console.error('No se encontró el elemento #modalPartida en el DOM');
        return;
    }

    // Nos aseguramos de obtener/crear siempre la instancia, aunque falle la inicialización previa
    modalPartidaInstance = bootstrap.Modal.getOrCreateInstance(modalPartidaElement, {
        backdrop: 'static'
    });

    const partidaNumero = document.getElementById('partida_numero');
    const categoria = document.getElementById('categoria');

    if (partidaNumero) {
        partidaNumero.value = '';
        partidaNumero.classList.remove('is-invalid');
    }

    if (categoria) {
        categoria.value = '';
        categoria.classList.remove('is-invalid');
    }

    modalPartidaInstance.show();
}

function crearPartida() {
    const partidaNumeroInput = document.getElementById('partida_numero');
    const categoriaInput = document.getElementById('categoria');

    const partidaNumero = partidaNumeroInput ? partidaNumeroInput.value.trim() : '';
    const categoria = categoriaInput ? categoriaInput.value.trim() : '';

    if (!partidaNumero) {
        mostrarErrorCampo('partida_numero', 'La partida es requerida');
        return;
    }

    if (!categoria) {
        mostrarErrorCampo('categoria', 'La categoría es requerida');
        return;
    }

    const formData = {
        partida: partidaNumero,
        categoria: categoria
    };

    const btnGuardar = document.getElementById('btnGuardarPartida');
    const originalText = btnGuardar.innerHTML;
    btnGuardar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Guardando...';
    btnGuardar.disabled = true;

    fetch('/materiales/crear-partida/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (modalPartidaInstance) {
                modalPartidaInstance.hide();
            }

            cargarPartidas();

            setTimeout(() => {
                const selectPartida = document.getElementById('selectPartida');
                if (selectPartida && data.partida && data.partida.id) {
                    selectPartida.value = data.partida.id;
                }
            }, 300);

            mostrarToastPartida('Partida presupuestaria agregada exitosamente', 'success');
        } else {
            mostrarToastPartida(data.error || 'Error al crear partida', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarToastPartida('Error al comunicarse con el servidor', 'error');
    })
    .finally(() => {
        btnGuardar.innerHTML = originalText;
        btnGuardar.disabled = false;
    });
}

function mostrarToastPartida(mensaje, tipo = 'success') {
    const toastElement = document.getElementById('toastPartida');
    const toastMessage = document.getElementById('toastPartidaMessage');

    if (!toastElement || !toastMessage || !toastPartida) return;

    const header = toastElement.querySelector('.toast-header');
    const icon = header ? header.querySelector('i') : null;
    const title = header ? header.querySelector('strong') : null;

    if (tipo === 'error') {
        if (icon) icon.className = 'fas fa-exclamation-triangle text-danger me-2';
        if (title) title.textContent = 'Error';
    } else {
        if (icon) icon.className = 'fas fa-check-circle text-success me-2';
        if (title) title.textContent = 'Éxito';
    }

    toastMessage.textContent = mensaje;
    toastPartida.show();
}

// =======================
// FIN PARTIDAS
// =======================

function cargarMateriales(busqueda = '') {
    const listaMateriales = document.getElementById('listaMateriales');
    if (!listaMateriales) return;
    
    let url = '/materiales/materiales/';
    if (busqueda) {
        url += `?search=${encodeURIComponent(busqueda)}`;
    }
    
    listaMateriales.innerHTML = '<div class="text-center text-muted py-2"><div class="spinner-border spinner-border-sm me-2" role="status"></div> Cargando...</div>';
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarListaMateriales(data.materiales);
            } else {
                listaMateriales.innerHTML = '<div class="text-center text-danger py-2">Error al cargar materiales</div>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            listaMateriales.innerHTML = '<div class="text-center text-danger py-2">Error de conexión</div>';
        });
}

function actualizarListaMateriales(materiales) {
    const listaMateriales = document.getElementById('listaMateriales');
    if (!listaMateriales) return;
    
    if (materiales.length === 0) {
        listaMateriales.innerHTML = '<div class="text-center text-muted py-4">No se encontraron materiales</div>';
        return;
    }
    
    let html = '';
    materiales.forEach(material => {
        const yaSeleccionado = materialesSeleccionados.some(m => m.id === material.id);
        const claseSeleccionado = yaSeleccionado ? 'material-selected' : '';
        
        html += `
            <div class="card material-card shadow-sm p-3 mb-2 ${claseSeleccionado}" 
                 data-material-id="${material.id}" 
                 onclick="seleccionarMaterial(${material.id}, '${material.codigo_material}', '${material.descripcion}', '${material.unidad_ingreso}', '${material.volumen}', ${material.cantidad_x_unidad_ingreso})">
                <div class="row g-3 align-items-center">
                    <div class="col-md-9 col-8">
                        <h6 class="fw-bold mb-1">${material.descripcion}</h6>
                        <span class="text-muted small d-block mb-1">Código: ${material.codigo_material}</span>
                        <span class="text-muted small d-block">Partida: ${material.partida__partida} - ${material.partida__categoria}</span>
                    </div>
                    <div class="col-md-3 text-md-end text-center">
                        <button class="btn btn-${yaSeleccionado ? 'success' : 'warning'} mt-2 px-3 fw-semibold">
                            ${yaSeleccionado ? '✓ Seleccionado' : 'Ingresar'}
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    listaMateriales.innerHTML = html;
}

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
    }
}

function actualizarTablaMateriales() {
    const tbody = document.getElementById('tablaMaterialesBody');
    const sinMateriales = document.getElementById('sinMateriales');
    const totalMateriales = document.getElementById('totalMateriales');
    
    if (!tbody) return;
    
    if (materialesSeleccionados.length === 0) {
        tbody.innerHTML = '<tr id="sinMateriales"><td colspan="6" class="text-center text-muted py-4">No hay materiales seleccionados.</td></tr>';
        totalMateriales.textContent = '0';
        return;
    }
    
    if (sinMateriales) sinMateriales.style.display = 'none';
    
    let html = '';
    materialesSeleccionados.forEach(material => {
        html += `
            <tr data-material-id="${material.id}">
                <td>${material.codigo_material}</td>
                <td>${material.descripcion}</td>
                <td>${material.unidad_ingreso}</td>
                <td>${material.volumen}</td>
                <td>
                    <input type="number" 
                           class="form-control form-control-sm cantidad-input" 
                           value="${material.cantidad}" 
                           min="1" 
                           max="1000"
                           onchange="actualizarCantidadMaterial(${material.id}, this.value)">
                </td>
                <td>
                    <button type="button" class="btn btn-sm btn-outline-danger" 
                            onclick="eliminarMaterial(${material.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    totalMateriales.textContent = materialesSeleccionados.length;
}

function actualizarListaMaterialesUI() {
    const buscarMaterial = document.getElementById('buscarMaterial');
    cargarMateriales(buscarMaterial ? buscarMaterial.value : '');
}

function actualizarCantidadMaterial(materialId, cantidad) {
    const cantidadNum = parseInt(cantidad);
    if (isNaN(cantidadNum) || cantidadNum < 1) return;
    
    const material = materialesSeleccionados.find(m => m.id === materialId);
    if (material) {
        material.cantidad = cantidadNum;
    }
}

function eliminarMaterial(materialId) {
    materialesSeleccionados = materialesSeleccionados.filter(m => m.id !== materialId);
    actualizarTablaMateriales();
    actualizarListaMaterialesUI();
}

function abrirModalProveedor() {
    if (modalProveedorInstance) {
        modalProveedorInstance.show();
    }
}

function crearProveedor() {
    const proveedorNombre = document.getElementById('proveedor_nombre').value.trim();
    const proveedorNit = document.getElementById('proveedor_nit').value.trim();
    
    if (!proveedorNombre) {
        mostrarErrorCampo('proveedor_nombre', 'El nombre del proveedor es requerido');
        return;
    }
    
    if (!proveedorNit) {
        mostrarErrorCampo('proveedor_nit', 'El NIT es requerido');
        return;
    }
    
    const formData = {
        proveedor: proveedorNombre,
        nit: proveedorNit
    };
    
    const btnGuardar = document.getElementById('btnGuardarProveedor');
    const originalText = btnGuardar.innerHTML;
    btnGuardar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Guardando...';
    btnGuardar.disabled = true;
    
    fetch('/materiales/crear-proveedor/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (modalProveedorInstance) {
                modalProveedorInstance.hide();
            }
            
            cargarProveedores();
            
            setTimeout(() => {
                const selectProveedor = document.getElementById('selectProveedor');
                if (selectProveedor) {
                    selectProveedor.value = data.proveedor.id;
                }
            }, 300);
            
            mostrarToastProveedor('Proveedor agregado exitosamente');
            
        } else {
            mostrarError('Error al crear proveedor: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarError('Error al comunicarse con el servidor');
    })
    .finally(() => {
        btnGuardar.innerHTML = originalText;
        btnGuardar.disabled = false;
    });
}

function registrarIngresoCompleto() {
    const nroIngreso = document.getElementById('nro_ingreso').value.trim();
    const hRuta = document.getElementById('h_ruta').value.trim();
    const fechaIngreso = document.getElementById('fecha_ingreso').value;
    const factura = document.getElementById('factura').value.trim();
    const ordenCompra = document.getElementById('orden_compra').value.trim();
    const selectProveedor = document.getElementById('selectProveedor');
    const proveedorId = selectProveedor ? selectProveedor.value : '';
    const selectAlmacen = document.getElementById('selectAlmacen');
    const almacenId = selectAlmacen ? selectAlmacen.value : '';
    
    if (!nroIngreso || !hRuta || !fechaIngreso || !factura || !ordenCompra || !proveedorId || !almacenId) {
        mostrarError('Por favor complete todos los datos del ingreso (incluido almacén)');
        return;
    }
    
    if (materialesSeleccionados.length === 0) {
        mostrarError('Debe seleccionar al menos un material para ingresar');
        return;
    }
    
    const formData = {
        nro_ingreso: nroIngreso,
        h_ruta: hRuta,
        fecha_ingreso: fechaIngreso,
        factura: factura,
        orden_compra: ordenCompra,
        proveedor_id: proveedorId,
        almacen_id: almacenId,
        materiales_ingresados: materialesSeleccionados.map(m => ({
            material_id: m.id,
            cantidad: m.cantidad
        }))
    };
    
    console.log('Enviando ingreso completo:', formData);
    
    const btnRegistrar = document.getElementById('btnRegistrarIngreso');
    const originalText = btnRegistrar.innerHTML;
    btnRegistrar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Registrando...';
    btnRegistrar.disabled = true;
    
    fetch('/materiales/registrar-ingreso/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarExito('Ingreso registrado exitosamente!');
            if (data.pdf_url) {
                window.open(data.pdf_url, '_blank');
            }            
            const redirectUrl = data.redirect_url || '/materiales/';
            window.location.href = redirectUrl;
            
        } else {
            mostrarError('Error al registrar ingreso: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarError('Error al comunicarse con el servidor');
    })
    .finally(() => {
        btnRegistrar.innerHTML = originalText;
        btnRegistrar.disabled = false;
    });
}

function limpiarFormularioIngreso() {
    document.getElementById('nro_ingreso').value = '';
    document.getElementById('h_ruta').value = '';
    document.getElementById('fecha_ingreso').value = '';
    document.getElementById('factura').value = '';
    document.getElementById('orden_compra').value = '';
    
    const selectProveedor = document.getElementById('selectProveedor');
    if (selectProveedor) selectProveedor.value = '';

    const selectAlmacen = document.getElementById('selectAlmacen');
    if (selectAlmacen) selectAlmacen.value = '';
    
    materialesSeleccionados = [];
    actualizarTablaMateriales();
    actualizarListaMaterialesUI();
}

function mostrarToastProveedor(mensaje) {
    const toastMessage = document.getElementById('toastProveedorMessage');
    if (toastMessage && toastProveedor) {
        toastMessage.textContent = mensaje;
        toastProveedor.show();
    }
}

function mostrarError(mensaje) {
    alert('Error: ' + mensaje);
}

function mostrarExito(mensaje) {
    alert('Éxito: ' + mensaje);
}

function mostrarErrorCampo(campoId, mensaje) {
    const campo = document.getElementById(campoId);
    if (campo) {
        campo.classList.add('is-invalid');
        let feedback = campo.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = mensaje;
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

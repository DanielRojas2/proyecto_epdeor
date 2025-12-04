// static/js/materiales.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('materiales.js cargado correctamente');
    inicializarComponentes();
});

// Variables globales para manejar los modales
let modalMaterialInstance = null;
let modalPartidaInstance = null;

function inicializarComponentes() {
    // Inicializar instancias de modales
    const modalMaterialElement = document.getElementById('modalIngresoMaterial');
    const modalPartidaElement = document.getElementById('modalPartida');
    
    if (modalMaterialElement) {
        modalMaterialInstance = new bootstrap.Modal(modalMaterialElement);
    }
    if (modalPartidaElement) {
        modalPartidaInstance = new bootstrap.Modal(modalPartidaElement);
    }
    
    // Inicializar toast de Bootstrap
    const toastElement = document.getElementById('toastPartida');
    if (toastElement) {
        window.toastPartida = new bootstrap.Toast(toastElement);
    }
    
    // Configurar event listeners
    configurarEventListeners();
}

function configurarEventListeners() {
    // Cargar partidas al abrir el modal de material
    const modalMaterialEl = document.getElementById('modalIngresoMaterial');
    if (modalMaterialEl) {
        modalMaterialEl.addEventListener('show.bs.modal', function() {
            console.log('Modal de material abierto, cargando partidas...');
            cargarPartidasPresupuestarias();
        });
    }

    // Botón para abrir modal de partida
    const btnAbrirModalPartida = document.getElementById('btnAbrirModalPartida');
    if (btnAbrirModalPartida) {
        btnAbrirModalPartida.addEventListener('click', function(e) {
            e.preventDefault();
            abrirModalPartida();
        });
    }

    // Manejar envío de formularios
    const btnGuardarMaterial = document.getElementById('btnGuardarMaterial');
    if (btnGuardarMaterial) {
        btnGuardarMaterial.addEventListener('click', crearMaterial);
    }
    
    const btnGuardarPartida = document.getElementById('btnGuardarPartida');
    if (btnGuardarPartida) {
        btnGuardarPartida.addEventListener('click', crearPartida);
    }

    // Limpiar formularios al cerrar modales
    const modalPartidaEl = document.getElementById('modalPartida');
    if (modalPartidaEl) {
        modalPartidaEl.addEventListener('hidden.bs.modal', function() {
            limpiarFormularioPartida();
        });
    }

    const modalMaterialEl2 = document.getElementById('modalIngresoMaterial');
    if (modalMaterialEl2) {
        modalMaterialEl2.addEventListener('hidden.bs.modal', function() {
            limpiarFormularioMaterial();
        });
    }

    // Permitir enviar formularios con Enter
    const formMaterial = document.getElementById('formMaterial');
    if (formMaterial) {
        formMaterial.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                crearMaterial();
            }
        });
    }

    const formPartida = document.getElementById('formPartida');
    if (formPartida) {
        formPartida.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                crearPartida();
            }
        });
    }
}

function abrirModalPartida() {
    console.log('Abriendo modal de partida...');
    if (modalPartidaInstance) {
        modalPartidaInstance.show();
    }
}

function cargarPartidasPresupuestarias() {
    console.log('Cargando partidas presupuestarias...');
    
    const selectPartida = document.getElementById('selectPartida');
    if (!selectPartida) {
        console.error('No se encontró el select de partidas');
        return;
    }
    
    // Mostrar estado de carga
    selectPartida.innerHTML = '<option value="" disabled>Cargando partidas...</option>';
    
    fetch('/materiales/partidas-presupuestarias/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                actualizarSelectPartidas(data.partidas);
                console.log(`Partidas cargadas: ${data.partidas.length}`);
            } else {
                console.error('Error en la respuesta:', data.error);
                mostrarError('Error al cargar las partidas presupuestarias');
                actualizarSelectPartidas([]);
            }
        })
        .catch(error => {
            console.error('Error en fetch:', error);
            mostrarError('Error de conexión al cargar partidas');
            actualizarSelectPartidas([]);
        });
}

function actualizarSelectPartidas(partidas) {
    const selectPartida = document.getElementById('selectPartida');
    if (!selectPartida) return;
    
    // Guardar selección actual si existe
    const seleccionActual = selectPartida.value;
    
    // Limpiar y actualizar opciones
    selectPartida.innerHTML = '<option value="" selected disabled>Seleccionar partida...</option>';
    
    if (partidas.length === 0) {
        selectPartida.innerHTML += '<option value="" disabled>No hay partidas disponibles</option>';
        return;
    }
    
    partidas.forEach(partida => {
        const option = document.createElement('option');
        option.value = partida.id;
        option.textContent = `${partida.partida} - ${partida.categoria}`;
        selectPartida.appendChild(option);
    });
    
    // Restaurar selección anterior si existe
    if (seleccionActual && partidas.some(p => p.id == seleccionActual)) {
        selectPartida.value = seleccionActual;
    }
}

function crearPartida() {
    console.log('Iniciando creación de partida...');
    
    const partidaNumero = document.getElementById('partida_numero').value.trim();
    const categoria = document.getElementById('categoria').value.trim();
    
    // Validaciones
    if (!partidaNumero) {
        mostrarErrorCampo('partida_numero', 'La partida es requerida');
        return;
    }
    
    if (!categoria) {
        mostrarErrorCampo('categoria', 'La categoría es requerida');
        return;
    }
    
    if (!/^\d{1,5}$/.test(partidaNumero)) {
        mostrarErrorCampo('partida_numero', 'La partida debe contener solo números (máx. 5 dígitos)');
        return;
    }

    const formData = {
        partida: partidaNumero,
        categoria: categoria
    };
    
    // Mostrar estado de carga
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
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log('Partida creada exitosamente:', data.partida);
            
            // Cerrar solo el modal de partida
            if (modalPartidaInstance) {
                modalPartidaInstance.hide();
            }
            
            // Recargar las partidas en el select
            cargarPartidasPresupuestarias();
            
            // Seleccionar automáticamente la nueva partida
            setTimeout(() => {
                seleccionarPartida(data.partida.id);
            }, 300);
            
            // Mostrar toast de éxito
            mostrarToastPartida('Partida presupuestaria agregada exitosamente');
            
        } else {
            mostrarError('Error al crear partida: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarError('Error al comunicarse con el servidor');
    })
    .finally(() => {
        // Restaurar botón
        btnGuardar.innerHTML = originalText;
        btnGuardar.disabled = false;
    });
}

function seleccionarPartida(partidaId) {
    const selectPartida = document.getElementById('selectPartida');
    if (selectPartida) {
        selectPartida.value = partidaId;
        selectPartida.classList.remove('is-invalid');
        selectPartida.classList.add('is-valid');
    }
}

function crearMaterial() {
    const selectPartida = document.getElementById('selectPartida');
    const partidaId = selectPartida ? selectPartida.value : '';
    const descripcion = document.getElementById('descripcion').value.trim();
    const unidadIngreso = document.getElementById('unidad_ingreso').value;
    const unidadSalida = document.getElementById('unidad_salida').value;
    const tipoMaterial = document.getElementById('tipo_material').value;
    
    // Validaciones
    let hayErrores = false;
    
    if (!descripcion) {
        mostrarErrorCampo('descripcion', 'La descripción es requerida');
        hayErrores = true;
    }
    
    if (!partidaId) {
        if (selectPartida) {
            selectPartida.classList.add('is-invalid');
        }
        mostrarError('Por favor seleccione una partida presupuestaria');
        hayErrores = true;
    }
    
    if (!unidadIngreso) {
        mostrarErrorCampo('unidad_ingreso', 'Seleccione una unidad de ingreso');
        hayErrores = true;
    }
    
    if (!unidadSalida) {
        mostrarErrorCampo('unidad_salida', 'Seleccione una unidad de salida');
        hayErrores = true;
    }
    
    if (!tipoMaterial) {
        mostrarErrorCampo('tipo_material', 'Seleccione un tipo de material');
        hayErrores = true;
    }
    
    if (hayErrores) {
        return;
    }

    const formData = {
        descripcion: descripcion,
        partida: partidaId,
        cantidad_minima: parseInt(document.getElementById('cantidad_minima').value) || 1,
        unidad_ingreso: unidadIngreso,
        cantidad_x_unidad_ingreso: parseInt(document.getElementById('cantidad_x_unidad_ingreso').value) || 1,
        volumen: document.getElementById('volumen').value || 'N/A',
        unidad_salida: unidadSalida,
        tipo_material: tipoMaterial
    };
    
    console.log('Enviando datos de material:', formData);
    
    // Mostrar estado de carga
    const btnGuardar = document.getElementById('btnGuardarMaterial');
    const originalText = btnGuardar.innerHTML;
    btnGuardar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Guardando...';
    btnGuardar.disabled = true;
    
    fetch('/materiales/crear-material/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Cerrar modal de material
            if (modalMaterialInstance) {
                modalMaterialInstance.hide();
            }
            
            // Mostrar mensaje de éxito
            mostrarExito(`Material creado exitosamente! Código: ${data.material.codigo_material}`);
            
            // Opcional: Actualizar la lista de materiales
            if (typeof actualizarListaMateriales === 'function') {
                actualizarListaMateriales();
            }
            
        } else {
            mostrarError('Error al crear material: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarError('Error al comunicarse con el servidor');
    })
    .finally(() => {
        // Restaurar botón
        btnGuardar.innerHTML = originalText;
        btnGuardar.disabled = false;
    });
}

function limpiarFormularioPartida() {
    const form = document.getElementById('formPartida');
    if (form) {
        form.reset();
    }
    
    // Limpiar clases de validación
    const partidaInput = document.getElementById('partida_numero');
    const categoriaInput = document.getElementById('categoria');
    
    if (partidaInput) partidaInput.classList.remove('is-invalid');
    if (categoriaInput) categoriaInput.classList.remove('is-invalid');
}

function limpiarFormularioMaterial() {
    const form = document.getElementById('formMaterial');
    if (form) {
        form.reset();
    }
    
    // Limpiar selección de partida
    const selectPartida = document.getElementById('selectPartida');
    if (selectPartida) {
        selectPartida.value = '';
        selectPartida.classList.remove('is-valid', 'is-invalid');
    }
    
    // Limpiar clases de validación de otros campos
    const campos = ['descripcion', 'unidad_ingreso', 'unidad_salida', 'tipo_material'];
    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) {
            elemento.classList.remove('is-invalid');
        }
    });
}

// Funciones de utilidad para mensajes
function mostrarToastPartida(mensaje) {
    const toastMessage = document.getElementById('toastPartidaMessage');
    if (toastMessage && window.toastPartida) {
        toastMessage.textContent = mensaje;
        window.toastPartida.show();
    }
}

function mostrarError(mensaje) {
    // Usar alert temporalmente, puedes cambiar por toast de error
    alert('Error: ' + mensaje);
}

function mostrarExito(mensaje) {
    // Usar alert temporalmente, puedes cambiar por toast de éxito
    alert('Éxito: ' + mensaje);
}

function mostrarErrorCampo(campoId, mensaje) {
    const campo = document.getElementById(campoId);
    if (campo) {
        campo.classList.add('is-invalid');
        
        // Mostrar mensaje de error
        let feedback = campo.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            campo.parentNode.appendChild(feedback);
        }
        feedback.textContent = mensaje;
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

// Funciones para manejar la lista de materiales
function actualizarListaMateriales() {
    console.log('Actualizar lista de materiales...');
    // Implementar según sea necesario
}
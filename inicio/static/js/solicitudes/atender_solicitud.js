function mostrarMensaje(mensaje, tipo = 'success') {
    // Buscar si ya existe un contenedor de toasts
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // Crear el toast
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${tipo} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl);
    toast.show();

    // Remover el toast del DOM después de que se oculte
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}

function actualizarCantidad(detalleId) {
    const cantidadInput = document.getElementById(`cant-${detalleId}`);
    const cantidad = cantidadInput.value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Mostrar indicador de carga
    const originalValue = cantidadInput.value;
    cantidadInput.disabled = true;

    fetch(`/solicitudes/modificar-detalle/${detalleId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `cantidad=${cantidad}`
    })
    .then(response => response.json())
    .then(data => {
        cantidadInput.disabled = false;
        
        if (data.ok) {
            mostrarMensaje('Cantidad actualizada correctamente', 'success');
            cantidadInput.classList.remove('is-invalid');
            cantidadInput.classList.add('is-valid');
            
            // Remover la clase de validación después de 2 segundos
            setTimeout(() => {
                cantidadInput.classList.remove('is-valid');
            }, 2000);
        } else {
            mostrarMensaje(data.error, 'danger');
            cantidadInput.classList.add('is-invalid');
            cantidadInput.value = originalValue;
        }
    })
    .catch(error => {
        cantidadInput.disabled = false;
        mostrarMensaje('Error al actualizar la cantidad', 'danger');
        cantidadInput.classList.add('is-invalid');
        console.error('Error:', error);
    });
}

function aprobarSolicitud(solicitudId) {
    if (!confirm('¿Estás seguro de que deseas aprobar esta solicitud?')) {
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const boton = event.target;
    const originalText = boton.innerHTML;
    
    // Mostrar estado de carga
    boton.disabled = true;
    boton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';

    fetch(`/solicitudes/aprobar/${solicitudId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            mostrarMensaje(data.msg, 'success');
            // Redirigir después de 2 segundos
            setTimeout(() => {
                window.location.href = '/solicitudes/pendientes/';
            }, 2000);
        } else {
            mostrarMensaje('Error al aprobar la solicitud', 'danger');
            boton.disabled = false;
            boton.innerHTML = originalText;
        }
    })
    .catch(error => {
        mostrarMensaje('Error de conexión', 'danger');
        boton.disabled = false;
        boton.innerHTML = originalText;
        console.error('Error:', error);
    });
}

function rechazarSolicitud(solicitudId) {
    if (!confirm('¿Estás seguro de que deseas rechazar esta solicitud?')) {
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const boton = event.target;
    const originalText = boton.innerHTML;
    
    // Mostrar estado de carga
    boton.disabled = true;
    boton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';

    fetch(`/solicitudes/rechazar/${solicitudId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            mostrarMensaje(data.msg, 'warning');
            // Redirigir después de 2 segundos
            setTimeout(() => {
                window.location.href = '/solicitudes/pendientes/';
            }, 2000);
        } else {
            mostrarMensaje('Error al rechazar la solicitud', 'danger');
            boton.disabled = false;
            boton.innerHTML = originalText;
        }
    })
    .catch(error => {
        mostrarMensaje('Error de conexión', 'danger');
        boton.disabled = false;
        boton.innerHTML = originalText;
        console.error('Error:', error);
    });
}

// Validación en tiempo real para los inputs de cantidad
document.addEventListener('DOMContentLoaded', function() {
    const cantidadInputs = document.querySelectorAll('input[type="number"]');
    cantidadInputs.forEach(input => {
        input.addEventListener('input', function() {
            const max = parseInt(this.max);
            const value = parseInt(this.value) || 0;
            
            if (value > max) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
});
// entrega_material.js - Versión mejorada
function registrarEntregaGlobal(solicitudId) {
    if (!confirm('¿Está seguro de registrar esta entrega? Esta acción no se puede deshacer.')) {
        return;
    }

    const form = document.getElementById('form-entrega');
    const formData = new FormData(form);
    
    // Mostrar loading
    const submitBtn = event.target;
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Procesando...';
    submitBtn.disabled = true;

    fetch(`/solicitudes/registrar-entrega/${solicitudId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('success', data.message);
            
            // Redireccionar después de 2 segundos
            setTimeout(() => {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    window.location.href = '/solicitudes/entregas/';
                }
            }, 2000);
        } else {
            showToast('error', data.error || 'Error al registrar la entrega');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Error de conexión. Intente nuevamente.');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Validación en tiempo real de cantidades
document.addEventListener('DOMContentLoaded', function() {
    const cantidadInputs = document.querySelectorAll('.cantidad-entrega');
    
    cantidadInputs.forEach(input => {
        input.addEventListener('change', function() {
            const max = parseInt(this.max);
            const value = parseInt(this.value) || 0;
            
            if (value > max) {
                this.value = max;
                showToast('warning', `La cantidad no puede exceder ${max} unidades`);
            }
            
            if (value < 0) {
                this.value = 0;
                showToast('warning', 'La cantidad no puede ser negativa');
            }
        });
    });
});

// Función para mostrar notificaciones
function showToast(type, message) {
    // Implementar usando tu librería de toasts o Bootstrap Toasts
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}
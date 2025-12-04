// static/js/solicitudes/solicitar_material.js
$(function(){
    function mostrarToastSolicitud(mensaje) {
        const toastEl = document.getElementById("toastSolicitud");
        const msgEl = document.getElementById("toastSolicitudMessage");

        if (!toastEl || !msgEl) return;

        msgEl.textContent = mensaje;

        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function cargarCarrito(){
        $.get("/solicitudes/carrito-parcial/", function(resp){
            $("#carrito-area").html(resp.html);
        });
    }

    $(document).on("click", ".btnAgregar", function(){
        const id = $(this).data("id");
        const cantidad = parseInt($("#cantidad-" + id).val() || 1);
        $.post(`/solicitudes/agregar/${id}/`, {cantidad: cantidad})
            .done(function(resp){
                if (resp.ok){
                    cargarCarrito();
                    if (window.mostrarToast) window.mostrarToast("Agregado", "Material agregado al carrito", "success");
                }
            })
            .fail(function(xhr){
                const msg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "Error al agregar";
                if (window.mostrarToast) window.mostrarToast("Error", msg, "error"); else alert(msg);
            });
    });

    $(document).on("change", ".cantidad-item", function(){
        const mid = $(this).data("mid");
        let cantidad = parseInt($(this).val() || 0);
        $.post(`/solicitudes/actualizar/${mid}/`, {cantidad: cantidad})
            .done(function(resp){
                cargarCarrito();
                if (window.mostrarToast) window.mostrarToast("Actualizado", "Cantidad actualizada", "success");
            })
            .fail(function(xhr){
                const msg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "Error";
                if (window.mostrarToast) window.mostrarToast("Error", msg, "error");
                cargarCarrito();
            });
    });

    $(document).on("click", ".btn-eliminar-item", function(){
        const id = $(this).data("id");
        $.post(`/solicitudes/eliminar/${id}/`, {})
            .done(function(){
                cargarCarrito();
                if (window.mostrarToast) window.mostrarToast("Eliminado", "Material eliminado del carrito", "success");
            })
            .fail(function(){
                if (window.mostrarToast) window.mostrarToast("Error", "No se pudo eliminar", "error");
            });
    });

    // =========================
    // 1) MOSTRAR MODAL CONFIRMACIÓN
    // =========================
    let generando = false;
    const modalConfirmar = new bootstrap.Modal(document.getElementById("modalConfirmarSolicitud"));

    $("#btnGenerarSolicitud").on("click", function(){
        // Copiamos el contenido actual del carrito al modal
        const contenidoCarrito = $("#carrito-area").html().trim();

        if (!contenidoCarrito || contenidoCarrito.length === 0 || /No hay materiales en la solicitud/i.test(contenidoCarrito)) {
            if (window.mostrarToast) {
                window.mostrarToast("Aviso", "No hay materiales en la solicitud", "warning");
            } else {
                alert("No hay materiales en la solicitud");
            }
            return;
        }

        $("#modalConfirmarCarrito").html(contenidoCarrito);
        // deshabilitar inputs/botones en el resumen del modal para que sea solo lectura
        $("#modalConfirmarCarrito").find("input, button").prop("disabled", true);

        modalConfirmar.show();
    });

    // =========================
    // 2) CONFIRMAR Y GENERAR SOLICITUD (AJAX)
    // =========================
    $("#btnConfirmarSolicitud").on("click", function(){
        if (generando) return;
        generando = true;

        const btn = $(this);
        const originalHtml = btn.html();
        btn.html('<span class="spinner-border spinner-border-sm me-1" role="status"></span> Generando...');
        btn.prop("disabled", true);

        $.post("/solicitudes/generar/", {})
            .done(function(resp){
                if (resp.ok){
                    modalConfirmar.hide();

                    if (resp.codigo) {
                        mostrarToastSolicitud(`Solicitud ${resp.codigo} generada correctamente.`);
                    } else {
                        mostrarToastSolicitud(`Solicitud generada correctamente.`);
                    }

                    setTimeout(() => {
                        const redirectUrl = resp.redirect_url || "/";
                        window.location.href = redirectUrl;
                    }, 2000);

                    cargarCarrito();
                } else {
                    if (window.mostrarToast) window.mostrarToast("Error", resp.error || "No se pudo crear la solicitud", "error");
                }
            })
            .fail(function(xhr){
                const msg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "Error al generar solicitud";
                if (window.mostrarToast) window.mostrarToast("Error", msg, "error");
            })
            .always(function(){
                generando = false;
                btn.html(originalHtml);
                btn.prop("disabled", false);
            });
    });

    // inicial
    cargarCarrito();
});

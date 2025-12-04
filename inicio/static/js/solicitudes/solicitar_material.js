// static/js/solicitudes/solicitar_material.js
$(function(){
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

    $("#btnGenerarSolicitud").on("click", function(){
        // Generar solicitud
        $.post("/solicitudes/generar/", {})
            .done(function(resp){
                if (resp.ok){
                    if (window.mostrarToast) window.mostrarToast("Solicitud", resp.msg, "success");
                    // mostrar nota en modal simple
                    const nota = resp.nota || "";
                    const html = `<div class="modal fade" id="modalNota" tabindex="-1"><div class="modal-dialog modal-lg modal-dialog-centered"><div class="modal-content"><div class="modal-header"><h5 class="modal-title">Nota interna - Solicitud ${resp.codigo}</h5><button class="btn-close" data-bs-dismiss="modal"></button></div><div class="modal-body"><pre style="white-space:pre-wrap">${nota}</pre></div><div class="modal-footer"><button class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button></div></div></div></div>`;
                    $("body").append(html);
                    var m = new bootstrap.Modal(document.getElementById("modalNota"));
                    m.show();
                    // remover modal del DOM cuando se oculte
                    $("#modalNota").on("hidden.bs.modal", function(){ $(this).remove(); });
                    cargarCarrito();
                } else {
                    if (window.mostrarToast) window.mostrarToast("Error", resp.error || "No se pudo crear la solicitud", "error");
                }
            })
            .fail(function(xhr){
                const msg = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "Error al generar solicitud";
                if (window.mostrarToast) window.mostrarToast("Error", msg, "error");
            });
    });

    // inicial
    cargarCarrito();
});

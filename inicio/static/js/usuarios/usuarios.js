document.addEventListener("DOMContentLoaded", () => {

    const modalPersonal = document.getElementById("modalPersonal");
    const modalForm = document.querySelector("#modalPersonal form");

    const btnRegistrar = document.getElementById("btnRegistrarPersonal");

    const personalIdInput = document.getElementById("personal_id");
    const nombre = document.getElementById("id_nombre");
    const apP = document.getElementById("id_apellido_paterno");
    const apM = document.getElementById("id_apellido_materno");
    const ci = document.getElementById("id_ci");
    const baja = document.getElementById("id_baja");
    const cargo = document.getElementById("id_cargo");

    btnRegistrar.addEventListener("click", () => {
        modalPersonal.querySelector(".modal-title").innerText = "Registrar Personal";

        modalForm.reset();
        personalIdInput.value = "";
    });

    document.querySelectorAll(".btnEditar").forEach(btn => {
        btn.addEventListener("click", () => {
            modalPersonal.querySelector(".modal-title").innerText = "Editar Personal";

            personalIdInput.value = btn.dataset.id;
            nombre.value = btn.dataset.nombre;
            apP.value = btn.dataset.apellido_p;
            apM.value = btn.dataset.apellido_m;
            ci.value = btn.dataset.ci;
            baja.value = btn.dataset.baja;
            cargo.value = btn.dataset.cargo;

            new bootstrap.Modal(modalPersonal).show();
        });
    });

    const tabla = document.querySelector("#tablaPersonal tbody");
    const buscador = document.querySelector("#buscador");
    const filtroEstado = document.querySelector("#filtroEstado");
    const filtroCargo = document.querySelector("#filtroCargo");

    function filtrar() {
        const texto = buscador.value.toLowerCase();
        const estado = filtroEstado.value.toLowerCase();
        const cargo = filtroCargo.value.toLowerCase();

        for (let fila of tabla.rows) {
            let cNombre = fila.cells[0].innerText.toLowerCase();
            let cEstado = fila.cells[8].innerText.toLowerCase();
            let cCargo = fila.cells[5].innerText.toLowerCase();

            let coincideBusqueda = cNombre.includes(texto);
            let coincideEstado = !estado || cEstado === estado;
            let coincideCargo = !cargo || cCargo === cargo;

            fila.style.display = (coincideBusqueda && coincideEstado && coincideCargo)
                ? ""
                : "none";
        }
    }

    buscador.addEventListener("keyup", filtrar);
    filtroEstado.addEventListener("change", filtrar);
    filtroCargo.addEventListener("change", filtrar);

    document.querySelectorAll(".tbl-header th[data-col]").forEach(th => {
        th.addEventListener("click", () => {
            const col = parseInt(th.dataset.col);
            const rows = Array.from(tabla.rows);

            const asc = th.classList.toggle("asc");

            rows.sort((a, b) => {
                let x = a.cells[col].innerText.toLowerCase();
                let y = b.cells[col].innerText.toLowerCase();
                return asc ? x.localeCompare(y) : y.localeCompare(x);
            });

            rows.forEach(r => tabla.appendChild(r));
        });
    });
});

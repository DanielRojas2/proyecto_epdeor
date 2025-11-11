const searchInput = document.getElementById("searchInput");
const filterSelect = document.getElementById("filterSelect");

searchInput.addEventListener("input", () => {
    filtrarDatos();
});

filterSelect.addEventListener("change", () => {
    filtrarDatos();
});

function filtrarDatos() {
    const texto = searchInput.value.toLowerCase();
    const filtroCargo = filterSelect.value;

    dataFiltrada = empleados.filter(emp => {
        const coincideTexto =
            emp.nombre.toLowerCase().includes(texto) ||
            emp.cargo.toLowerCase().includes(texto);
        const coincideCargo = filtroCargo ? emp.cargo === filtroCargo : true;
        return coincideTexto && coincideCargo;
    });

    renderTable(dataFiltrada);
}

document.querySelectorAll("th").forEach(th => {
    th.addEventListener("click", () => {
        const col = th.dataset.col;
        dataFiltrada.sort((a, b) => {
            if (a[col] < b[col]) return sortDirection ? -1 : 1;
            if (a[col] > b[col]) return sortDirection ? 1 : -1;
            return 0;
        });
        sortDirection = !sortDirection;
        renderTable(dataFiltrada);
    });
});

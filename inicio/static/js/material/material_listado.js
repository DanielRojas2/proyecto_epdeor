class MaterialManager {
    constructor() {
        this.currentPage = 1;
        this.pageSize = 10;
        this.searchTerm = '';
        this.tipoMaterial = '';
        this.initEventListeners();
        this.loadMaterials();
    }

    initEventListeners() {
        document.getElementById('btnBuscar').addEventListener('click', () => {
            this.searchTerm = document.getElementById('buscarMaterial').value;
            this.currentPage = 1;
            this.loadMaterials();
        });

        document.getElementById('buscarMaterial').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchTerm = document.getElementById('buscarMaterial').value;
                this.currentPage = 1;
                this.loadMaterials();
            }
        });

        document.getElementById('btnLimpiar').addEventListener('click', () => {
            document.getElementById('buscarMaterial').value = '';
            this.searchTerm = '';
            this.currentPage = 1;
            this.loadMaterials();
        });

        document.getElementById('filtroTipo').addEventListener('change', (e) => {
            this.tipoMaterial = e.target.value;
            this.currentPage = 1;
            this.loadMaterials();
        });
    }

    async loadMaterials() {
        const tablaBody = document.getElementById('tablaMaterialesBody');
        
        tablaBody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4">
                    <div class="loading-spinner">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Cargando...</span>
                        </div>
                        <p class="mt-2 text-muted">Cargando materiales...</p>
                    </div>
                </td>
            </tr>
        `;

        try {
            const params = new URLSearchParams({
                page: this.currentPage,
                page_size: this.pageSize,
                search: this.searchTerm,
                tipo_material: this.tipoMaterial
            });

            console.log('Solicitando datos con params:', params.toString()); // Debug

            const response = await fetch(`/materiales/materiales-list/?${params}`);
            const data = await response.json();

            console.log('Respuesta recibida:', data); // Debug

            if (data.success) {
                this.renderMaterials(data.materiales);
                this.renderPagination(data.pagination);
            } else {
                throw new Error(data.error || 'Error al cargar los materiales');
            }
        } catch (error) {
            console.error('Error:', error);
            tablaBody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center py-4 text-danger">
                        <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                        <p>Error al cargar los materiales: ${error.message}</p>
                        <button class="btn btn-primary mt-2" onclick="materialManager.loadMaterials()">
                            Reintentar
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    renderMaterials(materiales) {
        const tablaBody = document.getElementById('tablaMaterialesBody');
        
        console.log('Renderizando materiales:', materiales); // Debug

        if (materiales.length === 0) {
            tablaBody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center py-4 text-muted">
                        <i class="fas fa-inbox fa-3x mb-3"></i>
                        <p>No se encontraron materiales</p>
                        ${this.searchTerm || this.tipoMaterial ? 
                            '<p>Intenta con otros criterios de búsqueda</p>' : 
                            '<p>No hay materiales registrados</p>'
                        }
                    </td>
                </tr>
            `;
            return;
        }

        tablaBody.innerHTML = materiales.map(material => {
            // Debug de cada material
            console.log('Material individual:', material);
            
            return `
                <tr>
                    <td width="8%">${this.escapeHtml(material.codigo_material)}</td>
                    <td width="16%">${this.escapeHtml(material.descripcion)}</td>
                    <td width="7%">${this.escapeHtml(material.partida)}</td>
                    <td width="11%">${this.escapeHtml(material.tipo_material)}</td>
                    <td width="8%" class="text-center">${material.cantidad_existente}</td>
                    <td width="8%" class="text-center">${this.escapeHtml(material.unidad_ingreso)}</td>
                    <td width="8%" class="text-center">${material.cantidad_x_unidad_ingreso}</td>
                    <td width="7%" class="text-center">${this.escapeHtml(material.volumen)}</td>
                    <td width="7%" class="text-center">${this.escapeHtml(material.unidad_salida)}</td>
                </tr>
            `;
        }).join('');
    }

    renderPagination(pagination) {
        const paginationContainer = document.getElementById('pagination');
        const paginationInfo = document.getElementById('paginationInfo');
        
        if (!pagination || pagination.total_pages <= 1) {
            paginationContainer.innerHTML = '';
            paginationInfo.innerHTML = pagination ? 
                `Mostrando ${pagination.total_items} materiales` : '';
            return;
        }

        const startItem = ((pagination.current_page - 1) * this.pageSize) + 1;
        const endItem = Math.min(pagination.current_page * this.pageSize, pagination.total_items);
        paginationInfo.innerHTML = `Mostrando ${startItem}-${endItem} de ${pagination.total_items} materiales`;

        let paginationHTML = '';

        if (pagination.has_previous) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${pagination.previous_page_number}">
                        <i class="fas fa-chevron-left"></i>
                    </a>
                </li>
            `;
        } else {
            paginationHTML += `
                <li class="page-item disabled">
                    <span class="page-link">
                        <i class="fas fa-chevron-left"></i>
                    </span>
                </li>
            `;
        }

        const startPage = Math.max(1, pagination.current_page - 2);
        const endPage = Math.min(pagination.total_pages, pagination.current_page + 2);

        for (let i = startPage; i <= endPage; i++) {
            if (i === pagination.current_page) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>
                `;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="#" data-page="${i}">${i}</a>
                    </li>
                `;
            }
        }

        if (pagination.has_next) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${pagination.next_page_number}">
                        <i class="fas fa-chevron-right"></i>
                    </a>
                </li>
            `;
        } else {
            paginationHTML += `
                <li class="page-item disabled">
                    <span class="page-link">
                        <i class="fas fa-chevron-right"></i>
                    </span>
                </li>
            `;
        }

        paginationContainer.innerHTML = paginationHTML;

        paginationContainer.querySelectorAll('.page-link[data-page]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.currentPage = parseInt(link.getAttribute('data-page'));
                this.loadMaterials();
            });
        });
    }

    escapeHtml(unsafe) {
        if (unsafe === null || unsafe === undefined) return '';
        return unsafe
            .toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    window.materialManager = new MaterialManager();
});
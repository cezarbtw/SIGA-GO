const API_URL = 'http://127.0.0.1:8000';

// Armazenamento em memória para filtros instantâneos sem recarregar a rede
let allEmpresas = [];
let allRegistros = [];

// Instâncias ativas dos gráficos do Chart.js
let chartIsoInstance = null;
let chartImpactoInstance = null;

// ========================
// NAVEGAÇÃO ENTRE ABAS (SPA)
// ========================
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(sec => sec.style.display = 'none');
    
    // Atualiza links da navbar
    document.querySelectorAll('.navbar-nav .nav-link').forEach(btn => btn.classList.remove('active'));
    const navBtn = document.getElementById(`nav-${sectionId}`);
    if (navBtn) navBtn.classList.add('active');

    const targetSection = document.getElementById(sectionId);
    if (targetSection) targetSection.style.display = 'block';

    if (sectionId === 'empresas') loadEmpresas();
    if (sectionId === 'registros') loadRegistros();
    if (sectionId === 'dashboard') loadDashboard();
}

function showAlert(message, type = 'success') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show shadow-sm" role="alert">
            <div class="d-flex align-items-center gap-2">
                <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} fs-5"></i>
                <div>${message}</div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    const container = document.getElementById('alert-container');
    container.innerHTML = alertHtml;
    // Rola suavemente até o alerta caso esteja fora da tela
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ========================
// EMPRESAS (STAKEHOLDERS)
// ========================
async function loadEmpresas() {
    try {
        const res = await fetch(`${API_URL}/empresas/`);
        if (!res.ok) throw new Error('Falha ao comunicar com os Web Services de Empresas.');
        allEmpresas = await res.json();

        // Atualiza a combobox de cadastro de novo registro
        const select = document.getElementById('regEmpresaId');
        if (select) {
            select.innerHTML = '';
            if (allEmpresas.length === 0) {
                select.innerHTML = '<option value="">Nenhuma empresa cadastrada</option>';
            } else {
                allEmpresas.forEach(emp => {
                    select.innerHTML += `<option value="${emp.id}">${emp.nome} (${emp.cnpj})</option>`;
                });
            }
        }

        // Atualiza o select de filtro de registros por empresa
        const selectFiltro = document.getElementById('filtroRegistroEmpresa');
        if (selectFiltro) {
            selectFiltro.innerHTML = '<option value="todos">Filtrar por todas as empresas</option>';
            allEmpresas.forEach(emp => {
                selectFiltro.innerHTML += `<option value="${emp.id}">${emp.nome}</option>`;
            });
        }

        renderTabelaEmpresas(allEmpresas);
    } catch (err) {
        console.error('Erro ao carregar empresas:', err);
        showAlert('Não foi possível conectar ao servidor backend (FastAPI). Certifique-se de que a API está em execução.', 'danger');
    }
}

function renderTabelaEmpresas(empresas) {
    const tbody = document.getElementById('tabela-empresas');
    tbody.innerHTML = '';

    const contador = document.getElementById('contador-empresas');
    if (contador) contador.innerText = empresas.length;

    if (empresas.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-4">
                    <i class="bi bi-inbox fs-3 d-block mb-1"></i>
                    Nenhuma organização localizada com os critérios aplicados.
                </td>
            </tr>
        `;
        return;
    }

    empresas.forEach(emp => {
        const badgeIso = emp.certificada_iso14000
            ? '<span class="badge bg-success"><i class="bi bi-patch-check me-1"></i>Certificada</span>'
            : '<span class="badge bg-secondary"><i class="bi bi-dash-circle me-1"></i>Pendente</span>';

        tbody.innerHTML += `
            <tr>
                <td class="fw-bold text-muted">${emp.id}</td>
                <td class="fw-semibold text-dark">${emp.nome}</td>
                <td><code>${emp.cnpj}</code></td>
                <td><i class="bi bi-geo-alt text-danger me-1"></i>${emp.cidade} - ${emp.estado || 'GO'}</td>
                <td>${badgeIso}</td>
            </tr>
        `;
    });
}

// Filtro em tempo real de Empresas
function filtrarEmpresas() {
    const texto = (document.getElementById('filtroEmpresaTexto')?.value || '').toLowerCase();
    const filtroIso = document.getElementById('filtroEmpresaIso')?.value || 'todos';

    const filtradas = allEmpresas.filter(emp => {
        const matchesTexto = emp.nome.toLowerCase().includes(texto) ||
            emp.cnpj.toLowerCase().includes(texto) ||
            emp.cidade.toLowerCase().includes(texto);

        let matchesIso = true;
        if (filtroIso === 'sim') matchesIso = emp.certificada_iso14000 === true;
        if (filtroIso === 'nao') matchesIso = emp.certificada_iso14000 === false;

        return matchesTexto && matchesIso;
    });

    renderTabelaEmpresas(filtradas);
}

// Submissão do Formulário de Empresa
document.getElementById('formEmpresa').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nome: document.getElementById('empNome').value.trim(),
        cnpj: document.getElementById('empCnpj').value.trim(),
        cidade: document.getElementById('empCidade').value.trim(),
        estado: 'GO',
        certificada_iso14000: document.getElementById('empIso').checked
    };

    try {
        const res = await fetch(`${API_URL}/empresas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showAlert('Empresa cadastrada com sucesso no sistema ambiental!');
            const modalEl = document.getElementById('modalEmpresa');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            e.target.reset();
            await loadEmpresas();
            loadDashboard(); // Atualiza os números e gráficos
        } else {
            const error = await res.json();
            showAlert(`Erro na validação do servidor: ${error.detail || 'Falha ao salvar'}`, 'danger');
        }
    } catch (err) {
        showAlert('Erro de tráfego de rede ao tentar conectar com a API.', 'danger');
    }
});

// ========================
// REGISTROS DE IMPACTO
// ========================
async function loadRegistros() {
    try {
        const res = await fetch(`${API_URL}/registros/`);
        if (!res.ok) throw new Error('Falha ao comunicar com os Web Services de Registros.');
        allRegistros = await res.json();
        renderTabelaRegistros(allRegistros);
    } catch (err) {
        console.error('Erro ao carregar registros:', err);
    }
}

function renderTabelaRegistros(registros) {
    const tbody = document.getElementById('tabela-registros');
    tbody.innerHTML = '';

    const contador = document.getElementById('contador-registros');
    if (contador) contador.innerText = registros.length;

    if (registros.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-muted py-4">
                    <i class="bi bi-inbox fs-3 d-block mb-1"></i>
                    Nenhum registro de impacto ambiental cadastrado.
                </td>
            </tr>
        `;
        return;
    }

    registros.forEach(reg => {
        const date = new Date(reg.data_registro).toLocaleDateString('pt-BR');
        
        // Localiza o nome da empresa correspondente
        const emp = allEmpresas.find(e => e.id === reg.empresa_id);
        const nomeEmpresa = emp ? emp.nome : `Empresa #${reg.empresa_id}`;

        const acoesTexto = reg.acoes_mitigacao && reg.acoes_mitigacao.trim() !== ''
            ? `<small class="text-secondary fst-italic">${reg.acoes_mitigacao}</small>`
            : '<span class="text-muted small">Não informado</span>';

        tbody.innerHTML += `
            <tr>
                <td class="fw-bold text-muted">${reg.id}</td>
                <td class="fw-semibold">${nomeEmpresa}</td>
                <td><i class="bi bi-calendar3 text-muted me-1"></i>${date}</td>
                <td class="text-primary fw-semibold">${Number(reg.consumo_agua_litros).toLocaleString('pt-BR')} L</td>
                <td class="text-warning-emphasis fw-semibold">${Number(reg.consumo_energia_kwh).toLocaleString('pt-BR')} kWh</td>
                <td>${Number(reg.residuos_solidos_kg).toLocaleString('pt-BR')} kg</td>
                <td class="text-danger fw-semibold">${Number(reg.residuos_perigosos_kg).toLocaleString('pt-BR')} kg</td>
                <td>${acoesTexto}</td>
            </tr>
        `;
    });
}

// Filtro em tempo real de Registros
function filtrarRegistros() {
    const texto = (document.getElementById('filtroRegistroTexto')?.value || '').toLowerCase();
    const filtroEmpresaId = document.getElementById('filtroRegistroEmpresa')?.value || 'todos';

    const filtrados = allRegistros.filter(reg => {
        const matchesTexto = (reg.acoes_mitigacao || '').toLowerCase().includes(texto);
        const matchesEmpresa = filtroEmpresaId === 'todos' || String(reg.empresa_id) === String(filtroEmpresaId);
        return matchesTexto && matchesEmpresa;
    });

    renderTabelaRegistros(filtrados);
}

// Submissão do Formulário de Registro de Impacto
document.getElementById('formRegistro').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        empresa_id: parseInt(document.getElementById('regEmpresaId').value),
        consumo_agua_litros: parseFloat(document.getElementById('regAgua').value) || 0,
        consumo_energia_kwh: parseFloat(document.getElementById('regEnergia').value) || 0,
        residuos_solidos_kg: parseFloat(document.getElementById('regSolidos').value) || 0,
        residuos_perigosos_kg: parseFloat(document.getElementById('regPerigosos').value) || 0,
        acoes_mitigacao: document.getElementById('regAcoes').value.trim()
    };

    try {
        const res = await fetch(`${API_URL}/registros/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showAlert('Métrica ambiental lançada com sucesso no SGA!');
            const modalEl = document.getElementById('modalRegistro');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            e.target.reset();
            await loadRegistros();
            loadDashboard(); // Atualiza gráficos com a nova medição
        } else {
            const error = await res.json();
            showAlert(`Erro do servidor: ${error.detail || 'Falha ao salvar métrica'}`, 'danger');
        }
    } catch (err) {
        showAlert('Erro de rede ao submeter formulário de impacto.', 'danger');
    }
});

// ========================
// DASHBOARD & CHART.JS
// ========================
async function loadDashboard() {
    try {
        const [resEmp, resReg] = await Promise.all([
            fetch(`${API_URL}/empresas/`),
            fetch(`${API_URL}/registros/`)
        ]);

        if (resEmp.ok) allEmpresas = await resEmp.json();
        if (resReg.ok) allRegistros = await resReg.json();

        // 1. Atualizar métricas resumidas nos cards
        const totalEmpresas = allEmpresas.length;
        const totalRegistros = allRegistros.length;
        const certificadas = allEmpresas.filter(e => e.certificada_iso14000).length;
        const naoCertificadas = totalEmpresas - certificadas;
        const taxaIso = totalEmpresas > 0 ? Math.round((certificadas / totalEmpresas) * 100) : 0;

        const totalAgua = allRegistros.reduce((acc, r) => acc + (Number(r.consumo_agua_litros) || 0), 0);
        const totalEnergia = allRegistros.reduce((acc, r) => acc + (Number(r.consumo_energia_kwh) || 0), 0);
        const totalPerigosos = allRegistros.reduce((acc, r) => acc + (Number(r.residuos_perigosos_kg) || 0), 0);
        const totalSolidos = allRegistros.reduce((acc, r) => acc + (Number(r.residuos_solidos_kg) || 0), 0);

        document.getElementById('dash-empresas').innerText = totalEmpresas;
        document.getElementById('dash-registros').innerText = totalRegistros;
        document.getElementById('dash-taxa-iso').innerText = `${taxaIso}%`;
        document.getElementById('dash-agua').innerText = totalAgua.toLocaleString('pt-BR');
        document.getElementById('dash-energia').innerText = totalEnergia.toLocaleString('pt-BR');
        document.getElementById('dash-perigosos').innerText = totalPerigosos.toLocaleString('pt-BR');

        // 2. Renderizar / Atualizar Gráfico de Donut (ISO 14000)
        renderChartIso(certificadas, naoCertificadas);

        // 3. Renderizar / Atualizar Gráfico de Barras (Impacto Geral)
        renderChartImpacto(totalAgua, totalEnergia, totalSolidos, totalPerigosos);

    } catch (err) {
        console.error('Falha ao sincronizar dashboard:', err);
    }
}

function renderChartIso(certificadas, naoCertificadas) {
    const ctx = document.getElementById('chartIso');
    if (!ctx) return;

    if (chartIsoInstance) {
        chartIsoInstance.destroy();
    }

    const hasData = certificadas > 0 || naoCertificadas > 0;
    const dataValues = hasData ? [certificadas, naoCertificadas] : [1];
    const dataColors = hasData ? ['#198754', '#6c757d'] : ['#e9ecef'];
    const labels = hasData ? ['Certificadas (ISO 14000)', 'Não Certificadas'] : ['Sem empresas cadastradas'];

    chartIsoInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dataValues,
                backgroundColor: dataColors,
                borderWidth: 2,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 14,
                        font: { size: 12 }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

function renderChartImpacto(agua, energia, solidos, perigosos) {
    const ctx = document.getElementById('chartImpacto');
    if (!ctx) return;

    if (chartImpactoInstance) {
        chartImpactoInstance.destroy();
    }

    chartImpactoInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Água (L)', 'Energia (kWh)', 'Res. Sólidos (kg)', 'Res. Perigosos (kg)'],
            datasets: [{
                label: 'Volume Total Monitorado',
                data: [agua, energia, solidos, perigosos],
                backgroundColor: [
                    'rgba(13, 110, 253, 0.75)',
                    'rgba(255, 193, 7, 0.75)',
                    'rgba(108, 117, 125, 0.75)',
                    'rgba(220, 53, 69, 0.75)'
                ],
                borderColor: [
                    '#0d6efd',
                    '#ffc107',
                    '#6c757d',
                    '#dc3545'
                ],
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return value.toLocaleString('pt-BR');
                        }
                    }
                }
            }
        }
    });
}

// ========================
// EXPORTAÇÃO CSV COM UTF-8 BOM (Compatível com Excel)
// ========================
function downloadCSV(csvContent, fileName) {
    // Adiciona o caractere BOM (\uFEFF) para garantir que o Excel abra acentos em português corretamente
    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function exportarEmpresasCSV() {
    if (allEmpresas.length === 0) {
        showAlert('Não há dados de empresas para exportar.', 'warning');
        return;
    }

    let csv = 'ID;Nome;CNPJ;Cidade;Estado;Certificada_ISO14000\n';
    allEmpresas.forEach(e => {
        csv += `${e.id};"${e.nome}";"${e.cnpj}";"${e.cidade}";"${e.estado || 'GO'}";${e.certificada_iso14000 ? 'SIM' : 'NAO'}\n`;
    });

    downloadCSV(csv, 'empresas_siga_go.csv');
}

function exportarRegistrosCSV() {
    if (allRegistros.length === 0) {
        showAlert('Não há registros de impacto para exportar.', 'warning');
        return;
    }

    let csv = 'ID;ID_Empresa;Empresa;Data;Consumo_Agua_Litros;Consumo_Energia_kWh;Residuos_Solidos_kg;Residuos_Perigosos_kg;Acoes_Mitigacao\n';
    allRegistros.forEach(r => {
        const emp = allEmpresas.find(e => e.id === r.empresa_id);
        const nomeEmpresa = emp ? emp.nome : `Empresa #${r.empresa_id}`;
        const dataFormatada = new Date(r.data_registro).toLocaleDateString('pt-BR');
        const acoes = (r.acoes_mitigacao || '').replace(/[\r\n]+/g, ' ');
        csv += `${r.id};${r.empresa_id};"${nomeEmpresa}";"${dataFormatada}";${r.consumo_agua_litros};${r.consumo_energia_kwh};${r.residuos_solidos_kg};${r.residuos_perigosos_kg};"${acoes}"\n`;
    });

    downloadCSV(csv, 'registros_impacto_siga_go.csv');
}

// ========================
// INICIALIZAÇÃO
// ========================
window.onload = async () => {
    await loadEmpresas();
    await loadRegistros();
    await loadDashboard();
};

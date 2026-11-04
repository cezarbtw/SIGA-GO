const API_URL = 'http://127.0.0.1:8000';

// Estado global da aplicação
let isDemoMode = false;
let allEmpresas = [];
let allRegistros = [];

// Instâncias do Chart.js
let chartIsoInstance = null;
let chartImpactoInstance = null;
let chartEmpresasInstance = null;

// ========================
// CONTROLE DE TEMA (DARK / LIGHT)
// ========================
function initTheme() {
    const savedTheme = localStorage.getItem('siga_theme') || 'light';
    setTheme(savedTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('siga_theme', theme);

    const icon = document.getElementById('theme-icon');
    if (icon) {
        if (theme === 'dark') {
            icon.className = 'bi bi-sun-fill text-warning';
        } else {
            icon.className = 'bi bi-moon-stars-fill text-white';
        }
    }

    // Re-renderiza gráficos para ajustar cores aos fundos claro/escuro se houver dados
    if (allEmpresas.length > 0 || allRegistros.length > 0) {
        renderCharts();
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
}

// ========================
// CONTROLE DA SIDEBAR RETRÁTIL (ESTILO TCM-GO)
// ========================
function initSidebar() {
    const isCollapsed = localStorage.getItem('siga_sidebar_collapsed') === 'true';
    if (isCollapsed) {
        setSidebarCollapsed(true);
    }
}

function setSidebarCollapsed(collapsed) {
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.getElementById('main-wrapper');
    const toggleIcon = document.getElementById('sidebar-toggle-icon');

    if (collapsed) {
        sidebar?.classList.add('collapsed');
        mainWrapper?.classList.add('expanded');
        if (toggleIcon) toggleIcon.className = 'bi bi-chevron-right';
        localStorage.setItem('siga_sidebar_collapsed', 'true');
    } else {
        sidebar?.classList.remove('collapsed');
        mainWrapper?.classList.remove('expanded');
        if (toggleIcon) toggleIcon.className = 'bi bi-chevron-left';
        localStorage.setItem('siga_sidebar_collapsed', 'false');
    }

    // Redimensiona os gráficos do Chart.js suavemente
    setTimeout(() => {
        if (chartIsoInstance) chartIsoInstance.resize();
        if (chartImpactoInstance) chartImpactoInstance.resize();
        if (chartEmpresasInstance) chartEmpresasInstance.resize();
    }, 310);
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const isCurrentlyCollapsed = sidebar?.classList.contains('collapsed');
    setSidebarCollapsed(!isCurrentlyCollapsed);
}

function toggleSidebarMobile() {
    const sidebar = document.getElementById('sidebar');
    sidebar?.classList.toggle('mobile-open');
}

// ========================
// NAVEGAÇÃO SPA ENTRE SEÇÕES
// ========================
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(sec => sec.style.display = 'none');

    document.querySelectorAll('.sidebar-link').forEach(btn => btn.classList.remove('active'));
    const navBtn = document.getElementById(`nav-${sectionId}`);
    if (navBtn) navBtn.classList.add('active');

    // Em telas pequenas (mobile), fecha a sidebar ao selecionar um item
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth <= 768 && sidebar) {
        sidebar.classList.remove('mobile-open');
    }

    const targetSection = document.getElementById(sectionId);
    if (targetSection) targetSection.style.display = 'block';

    if (sectionId === 'empresas') renderTabelaEmpresas(allEmpresas);
    if (sectionId === 'registros') renderTabelaRegistros(allRegistros);
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
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ========================
// VERIFICAÇÃO DE STATUS DA API
// ========================
async function checkApiHealth() {
    const dot = document.getElementById('status-dot');
    const text = document.getElementById('status-text');

    if (isDemoMode) {
        if (dot) dot.className = 'status-dot demo';
        if (text) text.innerText = 'Modo Simulação (Goiás)';
        return;
    }

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);

        const res = await fetch(`${API_URL}/`, { signal: controller.signal });
        clearTimeout(timeoutId);

        if (res.ok) {
            if (dot) dot.className = 'status-dot online';
            if (text) text.innerText = 'API Online (Porta 8000)';
        } else {
            throw new Error('Status não 200');
        }
    } catch (e) {
        if (dot) dot.className = 'status-dot offline';
        if (text) text.innerText = 'API Offline';
    }
}

// ========================
// MODO DEMONSTRAÇÃO / SIMULAÇÃO (GOIÁS)
// ========================
const DADOS_SIMULADOS_EMPRESAS = [
    { id: 1, nome: "Hypera Pharma - Complexo DAIA", cnpj: "02.938.746/0001-45", cidade: "Anápolis", estado: "GO", certificada_iso14000: true },
    { id: 2, nome: "AgroVale Grãos & Alimentos", cnpj: "01.838.723/0002-88", cidade: "Rio Verde", estado: "GO", certificada_iso14000: true },
    { id: 3, nome: "Mineração Cerrado Dourado", cnpj: "12.455.670/0001-12", cidade: "Crixás", estado: "GO", certificada_iso14000: false },
    { id: 4, nome: "Laticínios Bela Vista S.A.", cnpj: "00.123.456/0001-99", cidade: "Bela Vista de Goiás", estado: "GO", certificada_iso14000: true },
    { id: 5, nome: "Cooperativa de Reciclagem ReciclaGyn", cnpj: "33.456.789/0001-20", cidade: "Goiânia", estado: "GO", certificada_iso14000: false }
];

const DADOS_SIMULADOS_REGISTROS = [
    { id: 1, empresa_id: 1, data_registro: "2026-10-01T10:30:00Z", consumo_agua_litros: 85000, consumo_energia_kwh: 42000, residuos_solidos_kg: 2400, residuos_perigosos_kg: 320, acoes_mitigacao: "Estação de tratamento de efluentes (ETE) com reuso de 35% de água de lavagem." },
    { id: 2, empresa_id: 1, data_registro: "2026-10-25T14:15:00Z", consumo_agua_litros: 79000, consumo_energia_kwh: 39500, residuos_solidos_kg: 2100, residuos_perigosos_kg: 280, acoes_mitigacao: "Incineração controlada de resíduos químicos em conformidade com NBR 10004." },
    { id: 3, empresa_id: 2, data_registro: "2026-10-05T09:00:00Z", consumo_agua_litros: 145000, consumo_energia_kwh: 58000, residuos_solidos_kg: 6800, residuos_perigosos_kg: 40, acoes_mitigacao: "Compostagem de cascas de grãos e destinação para adubação orgânica local." },
    { id: 4, empresa_id: 2, data_registro: "2026-10-28T16:20:00Z", consumo_agua_litros: 138000, consumo_energia_kwh: 54000, residuos_solidos_kg: 6200, residuos_perigosos_kg: 35, acoes_mitigacao: "Instalação de inversores solares fotovoltaicos de 250 kWp na fábrica." },
    { id: 5, empresa_id: 3, data_registro: "2026-10-12T11:45:00Z", consumo_agua_litros: 220000, consumo_energia_kwh: 92000, residuos_solidos_kg: 18500, residuos_perigosos_kg: 1450, acoes_mitigacao: "Neutralização química de rejeitos de flotação e recirculação de polpa mineral." },
    { id: 6, empresa_id: 4, data_registro: "2026-10-18T08:30:00Z", consumo_agua_litros: 64000, consumo_energia_kwh: 28000, residuos_solidos_kg: 1800, residuos_perigosos_kg: 15, acoes_mitigacao: "Biodigestor para queima de biogás e redução de pegada de carbono (ISO 14001)." },
    { id: 7, empresa_id: 5, data_registro: "2026-10-22T15:10:00Z", consumo_agua_litros: 12000, consumo_energia_kwh: 6500, residuos_solidos_kg: 45000, residuos_perigosos_kg: 0, acoes_mitigacao: "Triagem de 45 toneladas de plásticos PET, alumínio e papelão para indústrias." }
];

function toggleDemoMode() {
    isDemoMode = !isDemoMode;

    const banner = document.getElementById('demo-banner');
    const btnText = document.getElementById('demo-btn-text');

    if (isDemoMode) {
        if (banner) banner.style.display = 'flex';
        if (btnText) btnText.innerText = 'Sair da Demo';
        allEmpresas = [...DADOS_SIMULADOS_EMPRESAS];
        allRegistros = [...DADOS_SIMULADOS_REGISTROS];
        showAlert('Modo Simulação ativado com sucesso! Dados reais de organizações de Goiás carregados.', 'info');
    } else {
        if (banner) banner.style.display = 'none';
        if (btnText) btnText.innerText = 'Dados Demo';
        showAlert('Conectando aos Web Services da API FastAPI local...', 'light');
        loadEmpresas();
        loadRegistros();
    }

    atualizarSeletores();
    renderTabelaEmpresas(allEmpresas);
    renderTabelaRegistros(allRegistros);
    loadDashboard();
    checkApiHealth();
}

function atualizarSeletores() {
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

    const selectFiltro = document.getElementById('filtroRegistroEmpresa');
    if (selectFiltro) {
        selectFiltro.innerHTML = '<option value="todos">Filtrar por todas as empresas</option>';
        allEmpresas.forEach(emp => {
            selectFiltro.innerHTML += `<option value="${emp.id}">${emp.nome}</option>`;
        });
    }
}

// ========================
// EMPRESAS (STAKEHOLDERS)
// ========================
async function loadEmpresas() {
    if (isDemoMode) return;

    try {
        const res = await fetch(`${API_URL}/empresas/`);
        if (!res.ok) throw new Error('Falha no Web Service de empresas.');
        allEmpresas = await res.json();
        atualizarSeletores();
        renderTabelaEmpresas(allEmpresas);
    } catch (err) {
        console.warn('Backend indisponível para empresas:', err);
        // Se a API estiver offline e a lista estiver vazia, convida a ativar o modo Demo
        if (!isDemoMode && allEmpresas.length === 0) {
            showAlert('Não foi possível conectar à API local na porta 8000. Você pode clicar no botão <strong>"Dados Demo"</strong> no topo da página para testar a interface com dados de exemplo de Goiás!', 'warning');
        }
    }
}

function renderTabelaEmpresas(empresas) {
    const tbody = document.getElementById('tabela-empresas');
    if (!tbody) return;
    tbody.innerHTML = '';

    const contador = document.getElementById('contador-empresas');
    if (contador) contador.innerText = empresas.length;

    if (empresas.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted py-4">
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
                <td class="fw-semibold text-dark-emphasis">${emp.nome}</td>
                <td><code>${emp.cnpj}</code></td>
                <td><i class="bi bi-geo-alt text-danger me-1"></i>${emp.cidade} - ${emp.estado || 'GO'}</td>
                <td>${badgeIso}</td>
                <td class="text-center">
                    <button class="btn btn-outline-success btn-sm py-0 px-2" onclick="verDetalhesEmpresa(${emp.id})" title="Ver Histórico de Impacto">
                        <i class="bi bi-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    });
}

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

document.getElementById('formEmpresa').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nome: document.getElementById('empNome').value.trim(),
        cnpj: document.getElementById('empCnpj').value.trim(),
        cidade: document.getElementById('empCidade').value.trim(),
        estado: 'GO',
        certificada_iso14000: document.getElementById('empIso').checked
    };

    if (isDemoMode) {
        data.id = allEmpresas.length + 1;
        allEmpresas.push(data);
        showAlert('Empresa cadastrada com sucesso na simulação!', 'success');
        bootstrap.Modal.getInstance(document.getElementById('modalEmpresa'))?.hide();
        e.target.reset();
        atualizarSeletores();
        renderTabelaEmpresas(allEmpresas);
        loadDashboard();
        return;
    }

    try {
        const res = await fetch(`${API_URL}/empresas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showAlert('Empresa cadastrada com sucesso no sistema ambiental!');
            bootstrap.Modal.getInstance(document.getElementById('modalEmpresa'))?.hide();
            e.target.reset();
            await loadEmpresas();
            loadDashboard();
        } else {
            const error = await res.json();
            showAlert(`Erro na validação do servidor: ${error.detail || 'Falha ao salvar'}`, 'danger');
        }
    } catch (err) {
        showAlert('Erro de tráfego de rede ao tentar conectar com a API.', 'danger');
    }
});

// Modal de Detalhes da Empresa
function verDetalhesEmpresa(empresaId) {
    const emp = allEmpresas.find(e => e.id === empresaId);
    if (!emp) return;

    const registrosEmp = allRegistros.filter(r => r.empresa_id === empresaId);

    const titulo = document.getElementById('detalhesEmpresaTitulo');
    const corpo = document.getElementById('detalhesEmpresaCorpo');

    if (titulo) {
        titulo.innerHTML = `<i class="bi bi-building me-2"></i>${emp.nome}`;
    }

    if (corpo) {
        const totalAgua = registrosEmp.reduce((acc, r) => acc + (Number(r.consumo_agua_litros) || 0), 0);
        const totalEnergia = registrosEmp.reduce((acc, r) => acc + (Number(r.consumo_energia_kwh) || 0), 0);
        const totalPerigosos = registrosEmp.reduce((acc, r) => acc + (Number(r.residuos_perigosos_kg) || 0), 0);

        let linhasRegistros = '';
        if (registrosEmp.length === 0) {
            linhasRegistros = `<tr><td colspan="5" class="text-center text-muted">Nenhuma medição registrada para esta entidade.</td></tr>`;
        } else {
            registrosEmp.forEach(r => {
                const dataFormatada = new Date(r.data_registro).toLocaleDateString('pt-BR');
                linhasRegistros += `
                    <tr>
                        <td>${dataFormatada}</td>
                        <td class="text-primary">${Number(r.consumo_agua_litros).toLocaleString('pt-BR')} L</td>
                        <td class="text-warning-emphasis">${Number(r.consumo_energia_kwh).toLocaleString('pt-BR')} kWh</td>
                        <td>${Number(r.residuos_solidos_kg).toLocaleString('pt-BR')} kg</td>
                        <td class="text-danger">${Number(r.residuos_perigosos_kg).toLocaleString('pt-BR')} kg</td>
                    </tr>
                `;
            });
        }

        corpo.innerHTML = `
            <div class="row g-2 mb-3 bg-body-tertiary p-3 rounded border">
                <div class="col-sm-6"><strong>CNPJ:</strong> <code>${emp.cnpj}</code></div>
                <div class="col-sm-6"><strong>Localidade:</strong> ${emp.cidade} - ${emp.estado || 'GO'}</div>
                <div class="col-sm-6"><strong>Certificação ISO 14000:</strong> ${emp.certificada_iso14000 ? '<span class="badge bg-success">Sim</span>' : '<span class="badge bg-secondary">Não</span>'}</div>
                <div class="col-sm-6"><strong>Lançamentos Ambientais:</strong> ${registrosEmp.length}</div>
            </div>

            <div class="row g-2 mb-3 text-center">
                <div class="col-4">
                    <div class="p-2 border rounded bg-primary-subtle text-primary">
                        <small class="d-block fw-semibold">Água Acumulada</small>
                        <strong>${totalAgua.toLocaleString('pt-BR')} L</strong>
                    </div>
                </div>
                <div class="col-4">
                    <div class="p-2 border rounded bg-warning-subtle text-warning-emphasis">
                        <small class="d-block fw-semibold">Energia Acumulada</small>
                        <strong>${totalEnergia.toLocaleString('pt-BR')} kWh</strong>
                    </div>
                </div>
                <div class="col-4">
                    <div class="p-2 border rounded bg-danger-subtle text-danger">
                        <small class="d-block fw-semibold">Res. Perigosos</small>
                        <strong>${totalPerigosos.toLocaleString('pt-BR')} kg</strong>
                    </div>
                </div>
            </div>

            <h6 class="fw-bold mt-3 mb-2"><i class="bi bi-clock-history me-1"></i>Histórico de Lançamentos de Impacto</h6>
            <div class="table-responsive">
                <table class="table table-sm table-striped border">
                    <thead class="table-light">
                        <tr>
                            <th>Data</th>
                            <th>Água</th>
                            <th>Energia</th>
                            <th>Res. Sólidos</th>
                            <th>Res. Perigosos</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${linhasRegistros}
                    </tbody>
                </table>
            </div>
        `;
    }

    const modal = new bootstrap.Modal(document.getElementById('modalDetalhesEmpresa'));
    modal.show();
}

// ========================
// REGISTROS DE IMPACTO
// ========================
async function loadRegistros() {
    if (isDemoMode) return;

    try {
        const res = await fetch(`${API_URL}/registros/`);
        if (!res.ok) throw new Error('Falha no Web Service de registros.');
        allRegistros = await res.json();
        renderTabelaRegistros(allRegistros);
    } catch (err) {
        console.warn('Backend indisponível para registros:', err);
    }
}

function calcularGrauRisco(r) {
    const perigosos = Number(r.residuos_perigosos_kg) || 0;
    const agua = Number(r.consumo_agua_litros) || 0;
    const energia = Number(r.consumo_energia_kwh) || 0;

    if (perigosos > 100) {
        return '<span class="badge badge-risco-alto"><i class="bi bi-exclamation-octagon me-1"></i>Alto Risco</span>';
    }
    if (perigosos > 0 || agua > 50000 || energia > 30000) {
        return '<span class="badge badge-risco-medio"><i class="bi bi-exclamation-triangle me-1"></i>Médio Impacto</span>';
    }
    return '<span class="badge badge-risco-baixo"><i class="bi bi-check-circle me-1"></i>Monitorado</span>';
}

function renderTabelaRegistros(registros) {
    const tbody = document.getElementById('tabela-registros');
    if (!tbody) return;
    tbody.innerHTML = '';

    const contador = document.getElementById('contador-registros');
    if (contador) contador.innerText = registros.length;

    if (registros.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center text-muted py-4">
                    <i class="bi bi-inbox fs-3 d-block mb-1"></i>
                    Nenhum registro de impacto ambiental cadastrado.
                </td>
            </tr>
        `;
        return;
    }

    registros.forEach(reg => {
        const date = new Date(reg.data_registro).toLocaleDateString('pt-BR');
        const emp = allEmpresas.find(e => e.id === reg.empresa_id);
        const nomeEmpresa = emp ? emp.nome : `Empresa #${reg.empresa_id}`;

        const acoesTexto = reg.acoes_mitigacao && reg.acoes_mitigacao.trim() !== ''
            ? `<small class="text-body-secondary fst-italic">${reg.acoes_mitigacao}</small>`
            : '<span class="text-muted small">Não informado</span>';

        const badgeRisco = calcularGrauRisco(reg);

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
                <td>${badgeRisco}</td>
            </tr>
        `;
    });
}

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

    if (isDemoMode) {
        data.id = allRegistros.length + 1;
        data.data_registro = new Date().toISOString();
        allRegistros.push(data);
        showAlert('Métrica ambiental lançada com sucesso na simulação!', 'success');
        bootstrap.Modal.getInstance(document.getElementById('modalRegistro'))?.hide();
        e.target.reset();
        renderTabelaRegistros(allRegistros);
        loadDashboard();
        return;
    }

    try {
        const res = await fetch(`${API_URL}/registros/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showAlert('Métrica ambiental lançada com sucesso no SGA!');
            bootstrap.Modal.getInstance(document.getElementById('modalRegistro'))?.hide();
            e.target.reset();
            await loadRegistros();
            loadDashboard();
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
    if (!isDemoMode) {
        try {
            const [resEmp, resReg] = await Promise.all([
                fetch(`${API_URL}/empresas/`),
                fetch(`${API_URL}/registros/`)
            ]);

            if (resEmp.ok) allEmpresas = await resEmp.json();
            if (resReg.ok) allRegistros = await resReg.json();
        } catch (err) {
            console.warn('Backend offline ao sincronizar dashboard:', err);
        }
    }

    // 1. Atualizar números dos cards de topo
    const totalEmpresas = allEmpresas.length;
    const totalRegistros = allRegistros.length;
    const certificadas = allEmpresas.filter(e => e.certificada_iso14000).length;
    const naoCertificadas = totalEmpresas - certificadas;
    const taxaIso = totalEmpresas > 0 ? Math.round((certificadas / totalEmpresas) * 100) : 0;

    const totalAgua = allRegistros.reduce((acc, r) => acc + (Number(r.consumo_agua_litros) || 0), 0);
    const totalEnergia = allRegistros.reduce((acc, r) => acc + (Number(r.consumo_energia_kwh) || 0), 0);
    const totalPerigosos = allRegistros.reduce((acc, r) => acc + (Number(r.residuos_perigosos_kg) || 0), 0);
    const totalSolidos = allRegistros.reduce((acc, r) => acc + (Number(r.residuos_solidos_kg) || 0), 0);

    const elEmp = document.getElementById('dash-empresas');
    const elReg = document.getElementById('dash-registros');
    const elIso = document.getElementById('dash-taxa-iso');
    const elAgua = document.getElementById('dash-agua');
    const elEnergia = document.getElementById('dash-energia');
    const elPerigosos = document.getElementById('dash-perigosos');

    if (elEmp) elEmp.innerText = totalEmpresas;
    if (elReg) elReg.innerText = totalRegistros;
    if (elIso) elIso.innerText = `${taxaIso}%`;
    if (elAgua) elAgua.innerText = totalAgua.toLocaleString('pt-BR');
    if (elEnergia) elEnergia.innerText = totalEnergia.toLocaleString('pt-BR');
    if (elPerigosos) elPerigosos.innerText = totalPerigosos.toLocaleString('pt-BR');

    // 2. Renderizar gráficos
    renderCharts(certificadas, naoCertificadas, totalAgua, totalEnergia, totalSolidos, totalPerigosos);
}

function renderCharts(certificadas, naoCertificadas, totalAgua, totalEnergia, totalSolidos, totalPerigosos) {
    if (certificadas === undefined) {
        const totalEmpresas = allEmpresas.length;
        certificadas = allEmpresas.filter(e => e.certificada_iso14000).length;
        naoCertificadas = totalEmpresas - certificadas;
        totalAgua = allRegistros.reduce((acc, r) => acc + (Number(r.consumo_agua_litros) || 0), 0);
        totalEnergia = allRegistros.reduce((acc, r) => acc + (Number(r.consumo_energia_kwh) || 0), 0);
        totalPerigosos = allRegistros.reduce((acc, r) => acc + (Number(r.residuos_perigosos_kg) || 0), 0);
        totalSolidos = allRegistros.reduce((acc, r) => acc + (Number(r.residuos_solidos_kg) || 0), 0);
    }

    const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
    const textColor = isDark ? '#adb5bd' : '#495057';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

    // Gráfico 1: Donut ISO 14000
    renderChartIso(certificadas, naoCertificadas, textColor);

    // Gráfico 2: Balanço de Insumos (Barras Verticais)
    renderChartImpacto(totalAgua, totalEnergia, totalSolidos, totalPerigosos, textColor, gridColor);

    // Gráfico 3: Comparativo por Organização (Barras Horizontais)
    renderChartEmpresas(textColor, gridColor);
}

function renderChartIso(certificadas, naoCertificadas, textColor) {
    const ctx = document.getElementById('chartIso');
    if (!ctx) return;

    if (chartIsoInstance) chartIsoInstance.destroy();

    const hasData = certificadas > 0 || naoCertificadas > 0;
    const dataValues = hasData ? [certificadas, naoCertificadas] : [1];
    const dataColors = hasData ? ['#198754', '#6c757d'] : ['#e9ecef'];
    const labels = hasData ? ['Certificadas (ISO 14000)', 'Pendente'] : ['Sem dados cadastrados'];

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
                        color: textColor,
                        boxWidth: 14,
                        font: { size: 12 }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

function renderChartImpacto(agua, energia, solidos, perigosos, textColor, gridColor) {
    const ctx = document.getElementById('chartImpacto');
    if (!ctx) return;

    if (chartImpactoInstance) chartImpactoInstance.destroy();

    chartImpactoInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Água (L)', 'Energia (kWh)', 'Res. Sólidos (kg)', 'Res. Perigosos (kg)'],
            datasets: [{
                label: 'Volume Monitorado',
                data: [agua, energia, solidos, perigosos],
                backgroundColor: [
                    'rgba(13, 110, 253, 0.75)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(108, 117, 125, 0.75)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderColor: ['#0d6efd', '#ffc107', '#6c757d', '#dc3545'],
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
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: textColor,
                        callback: function (v) { return v.toLocaleString('pt-BR'); }
                    },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

function renderChartEmpresas(textColor, gridColor) {
    const ctx = document.getElementById('chartEmpresas');
    if (!ctx) return;

    if (chartEmpresasInstance) chartEmpresasInstance.destroy();

    // Consolida dados por empresa
    const nomes = [];
    const dadosAgua = [];
    const dadosEnergia = [];

    allEmpresas.slice(0, 6).forEach(emp => {
        nomes.push(emp.nome.length > 20 ? emp.nome.substring(0, 18) + '...' : emp.nome);
        const regs = allRegistros.filter(r => r.empresa_id === emp.id);
        const somaAgua = regs.reduce((acc, r) => acc + (Number(r.consumo_agua_litros) || 0), 0);
        const somaEnergia = regs.reduce((acc, r) => acc + (Number(r.consumo_energia_kwh) || 0), 0);
        dadosAgua.push(somaAgua);
        dadosEnergia.push(somaEnergia);
    });

    chartEmpresasInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nomes.length > 0 ? nomes : ['Nenhuma empresa'],
            datasets: [
                {
                    label: 'Água (Litros)',
                    data: dadosAgua.length > 0 ? dadosAgua : [0],
                    backgroundColor: 'rgba(13, 110, 253, 0.7)',
                    borderColor: '#0d6efd',
                    borderWidth: 1,
                    borderRadius: 4
                },
                {
                    label: 'Energia (kWh)',
                    data: dadosEnergia.length > 0 ? dadosEnergia : [0],
                    backgroundColor: 'rgba(255, 193, 7, 0.75)',
                    borderColor: '#ffc107',
                    borderWidth: 1,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: textColor, boxWidth: 12 }
                }
            },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: textColor,
                        callback: function (v) { return v.toLocaleString('pt-BR'); }
                    },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

// ========================
// EXPORTAÇÃO CSV COM UTF-8 BOM (EXCEL)
// ========================
function downloadCSV(csvContent, fileName) {
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
    initTheme();
    initSidebar();
    await checkApiHealth();
    await loadEmpresas();
    await loadRegistros();
    await loadDashboard();
};

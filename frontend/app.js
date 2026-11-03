const API_URL = 'http://127.0.0.1:8000';

// Navegação simples entre as seções
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(sec => sec.style.display = 'none');
    document.getElementById(sectionId).style.display = 'block';

    if (sectionId === 'empresas') loadEmpresas();
    if (sectionId === 'registros') loadRegistros();
    if (sectionId === 'dashboard') loadDashboard();
}

function showAlert(message, type = 'success') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.getElementById('alert-container').innerHTML = alertHtml;
}

// ========================
// EMPRESAS
// ========================
async function loadEmpresas() {
    try {
        const res = await fetch(`${API_URL}/empresas/`);
        if (!res.ok) throw new Error('Erro ao carregar empresas');
        const empresas = await res.json();

        const tbody = document.getElementById('tabela-empresas');
        tbody.innerHTML = '';

        // Atualiza combobox de registros
        const select = document.getElementById('regEmpresaId');
        select.innerHTML = '';

        empresas.forEach(emp => {
            tbody.innerHTML += `
                <tr>
                    <td>${emp.id}</td>
                    <td>${emp.nome}</td>
                    <td>${emp.cnpj}</td>
                    <td>${emp.cidade}</td>
                    <td>${emp.certificada_iso14000 ? '<span class="badge bg-success">Sim</span>' : '<span class="badge bg-secondary">Não</span>'}</td>
                </tr>
            `;

            select.innerHTML += `<option value="${emp.id}">${emp.nome}</option>`;
        });
    } catch (err) {
        console.error(err);
        showAlert('Não foi possível conectar à API de Web Services.', 'danger');
    }
}

document.getElementById('formEmpresa').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nome: document.getElementById('empNome').value,
        cnpj: document.getElementById('empCnpj').value,
        cidade: document.getElementById('empCidade').value,
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
            showAlert('Empresa cadastrada com sucesso!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalEmpresa'));
            modal.hide();
            e.target.reset();
            loadEmpresas();
        } else {
            const error = await res.json();
            showAlert(`Erro: ${error.detail}`, 'danger');
        }
    } catch (err) {
        showAlert('Erro ao enviar dados.', 'danger');
    }
});

// ========================
// REGISTROS
// ========================
async function loadRegistros() {
    try {
        const res = await fetch(`${API_URL}/registros/`);
        const registros = await res.json();

        const tbody = document.getElementById('tabela-registros');
        tbody.innerHTML = '';

        registros.forEach(reg => {
            const date = new Date(reg.data_registro).toLocaleDateString('pt-BR');
            tbody.innerHTML += `
                <tr>
                    <td>${reg.id}</td>
                    <td>${reg.empresa_id}</td>
                    <td>${date}</td>
                    <td>${reg.consumo_agua_litros}</td>
                    <td>${reg.consumo_energia_kwh}</td>
                    <td>${reg.residuos_solidos_kg}</td>
                    <td>${reg.residuos_perigosos_kg}</td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
    }
}

document.getElementById('formRegistro').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        empresa_id: parseInt(document.getElementById('regEmpresaId').value),
        consumo_agua_litros: parseFloat(document.getElementById('regAgua').value),
        consumo_energia_kwh: parseFloat(document.getElementById('regEnergia').value),
        residuos_solidos_kg: parseFloat(document.getElementById('regSolidos').value),
        residuos_perigosos_kg: parseFloat(document.getElementById('regPerigosos').value),
        acoes_mitigacao: document.getElementById('regAcoes').value
    };

    try {
        const res = await fetch(`${API_URL}/registros/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showAlert('Registro ambiental salvo com sucesso!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalRegistro'));
            modal.hide();
            e.target.reset();
            loadRegistros();
        } else {
            const error = await res.json();
            showAlert(`Erro: ${error.detail}`, 'danger');
        }
    } catch (err) {
        showAlert('Erro ao enviar dados.', 'danger');
    }
});

// ========================
// DASHBOARD
// ========================
async function loadDashboard() {
    try {
        const resEmp = await fetch(`${API_URL}/empresas/`);
        const resReg = await fetch(`${API_URL}/registros/`);

        const empresas = await resEmp.json();
        const registros = await resReg.json();

        document.getElementById('dash-empresas').innerText = empresas.length || 0;
        document.getElementById('dash-registros').innerText = registros.length || 0;
    } catch (err) {
        console.log('API off para dashboard', err);
    }
}

// Init
window.onload = () => {
    loadDashboard();
    loadEmpresas(); // Load once to populate select
};


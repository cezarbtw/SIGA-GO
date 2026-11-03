# SIGA-GO (Sistema de Informação de Gestão Ambiental - Goiás)

Este é o projeto para a Atividade Prática Supervisionada (APS) do 7º-8º semestre de Ciência da Computação. O foco é o desenvolvimento de Web Services para gestão ambiental e aderência à norma ISO 14000.

## Estrutura

- `backend/`: Código Python utilizando o framework **FastAPI** para prover os Web Services.
- `frontend/`: Aplicação em HTML, CSS e JavaScript utilizando Bootstrap para consumir a API.

## Como Executar

### 1. Iniciar o Backend (Web Services)
1. Abra um terminal na pasta `backend`.
2. (Opcional) Crie e ative um ambiente virtual: `python -m venv venv` e `.\venv\Scripts\activate`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Inicie o servidor: `uvicorn main:app --reload`.
5. Acesse `http://localhost:8000/docs` para ver a documentação dos serviços.

### 2. Iniciar o Frontend
- Basta abrir o arquivo `frontend/index.html` em qualquer navegador moderno.
- Opcionalmente, pode rodar `python -m http.server 8080` dentro da pasta `frontend` e acessar `http://localhost:8080/`.

## Componentes Técnicos Exigidos pela APS
- **Web Services**: Implementados no Backend com FastAPI e Pydantic.
- **Consumidor**: Frontend interage via `fetch` assíncrono.
- **Tratamento de Erros**: O backend retorna códigos de status (400, 404) e mensagens adequadas caso validações (como CNPJ duplicado ou empresa não existente) falhem.
- **Integração com ISO 14000**: As estruturas de dados armazenam atributos para ações de mitigação e certificações ambientais.


import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_report():
    doc = docx.Document()

    # Configuração de Margens ABNT / UNIP: Esquerda 2.5cm, Direita 2.5cm, Sup 3.0cm, Inf 2.0cm
    for section in doc.sections:
        section.top_margin = Inches(1.18)      # ~3.0 cm
        section.bottom_margin = Inches(0.79)   # ~2.0 cm
        section.left_margin = Inches(0.98)     # 2.5 cm
        section.right_margin = Inches(0.98)    # 2.5 cm

    # Estilo Normal
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)

    def add_p(text, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, italic=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_code_block(title, code_str):
        add_p(f"Listagem de Código: {title}",
              bold=True, space_before=8, space_after=4)
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        # Fundo cinza bem claro elegante para impressão
        set_cell_background(cell, "F4F4F4")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(code_str)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 30, 30)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # CAPA PADRÃO UNIP
    # -------------------------------------------------------------
    p = add_p("UNIVERSIDADE PAULISTA – UNIP", bold=True,
              align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10)
    p = add_p("CÂMPUS GOIÂNIA - FLAMBOYANT", bold=True,
              align=WD_ALIGN_PARAGRAPH.CENTER)
    p = add_p("CURSO DE CIÊNCIA DA COMPUTAÇÃO", bold=True,
              align=WD_ALIGN_PARAGRAPH.CENTER, space_after=90)

    add_p("ALUNOS:", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("Maria Luiza Marinho Melo – RA: N346736", bold=True,
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p("Gabriel Oliveira do Nascimento – RA: G773217",
          bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p("Abraão Cezar Inácio Leopoldino – RA: T457AD0", bold=True,
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=90)

    add_p("DESENVOLVIMENTO DE UMA APLICAÇÃO UTILIZANDO WEB SERVICES EM GESTÃO AMBIENTAL NO ESTADO DE GOIÁS",
          bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_p("Sistema SIGA-GO – Plataforma de Monitoramento Ambiental e Adequação à ISO 14000",
          italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=160)

    add_p("GOIÂNIA – GO", bold=True,
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_p("2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SUMÁRIO
    # -------------------------------------------------------------
    add_p("SUMÁRIO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)

    sumario_items = [
        ("1 OBJETIVO DO TRABALHO", "3"),
        ("2 INTRODUÇÃO", "4"),
        ("3 REFERENCIAL TEÓRICO E CONCEITOS GERAIS", "6"),
        ("   3.1 A Norma NBR ISO 14000 e a Gestão Ambiental Empresarial", "6"),
        ("   3.2 O Cenário Ambiental do Estado de Goiás e o Bioma Cerrado", "7"),
        ("   3.3 Fundamentos de Sistemas Distribuídos e Web Services", "8"),
        ("   3.4 O Estilo Arquitetural RESTful e Princípios de Fielding", "9"),
        ("   3.5 Análise Comparativa: Padrão REST versus Padrão SOAP", "11"),
        ("   3.6 O Protocolo HTTP/HTTPS, Métodos e Códigos Semânticos", "12"),
        ("   3.7 Interoperabilidade com o Padrão JSON", "13"),
        ("   3.8 Bancos Relacionais, Transações ACID e Mapeamento Objeto-Relacional", "14"),
        ("4 PLANO DE DESENVOLVIMENTO DA APLICAÇÃO", "16"),
        ("   4.1 Engenharia de Requisitos e Metodologia Adotada", "16"),
        ("   4.2 Identificação dos Stakeholders Ambientais", "16"),
        ("   4.3 Especificação dos Requisitos Funcionais (RF)", "17"),
        ("   4.4 Especificação dos Requisitos Não Funcionais (RNF)", "18"),
        ("   4.5 Preparação do Ambiente de Desenvolvimento", "19"),
        ("       4.5.1 Instalação e Configuração do Python", "19"),
        ("       4.5.2 Customização do Visual Studio Code", "20"),
        ("       4.5.3 Isolamento com Ambientes Virtuais (venv)", "21"),
        ("       4.5.4 Justificativa e Instalação dos Pacotes e Frameworks", "22"),
        ("   4.6 Políticas de Segurança e Gerenciamento de CORS", "23"),
        ("5 PROJETO E ARQUITETURA DO SISTEMA", "24"),
        ("   5.1 Arquitetura Desacoplada Cliente-Servidor", "24"),
        ("   5.2 Modelagem de Dados e Dicionário de Entidades", "25"),
        ("   5.3 Módulos de Software do Servidor Backend (FastAPI)", "26"),
        ("   5.4 Módulo da Aplicação Consumidora Frontend (SPA)", "27"),
        ("6 RESULTADOS E DISCUSSÃO", "29"),
        ("   6.1 Homologação com a Interface Interativa OpenAPI / Swagger UI", "29"),
        ("   6.2 Baterias de Testes de Exceção e Tratamento Defensivo", "30"),
        ("   6.3 Avaliação de Usabilidade e Performance Operacional", "31"),
        ("7 CONSIDERAÇÕES FINAIS E IMPACTO NA FORMAÇÃO ACADÊMICA", "32"),
        ("8 REFERÊNCIAS BIBLIOGRÁFICAS", "33"),
        ("9 CÓDIGOS FONTE DO SISTEMA (COMENTADOS LINHA A LINHA)", "34"),
        ("   9.1 backend/main.py", "34"),
        ("   9.2 backend/database.py", "35"),
        ("   9.3 backend/models.py", "36"),
        ("   9.4 backend/schemas.py", "38"),
        ("   9.5 backend/crud.py", "39"),
        ("   9.6 backend/routers/empresas.py", "41"),
        ("   9.7 backend/routers/registros.py", "42"),
        ("   9.8 frontend/index.html", "44"),
        ("   9.9 frontend/app.js", "48"),
        ("   9.10 frontend/style.css", "52"),
        ("10 FICHAS DE ATIVIDADES PRÁTICAS SUPERVISIONADAS", "53")
    ]

    for item, pg in sumario_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(3)
        run_title = p.add_run(item)
        run_title.font.name = 'Arial'
        run_title.font.size = Pt(11)
        if not item.startswith("   "):
            run_title.bold = True

        # Pontilhado
        dots_len = max(5, 75 - len(item))
        run_dots = p.add_run(" " + "." * dots_len + " ")
        run_dots.font.name = 'Arial'
        run_dots.font.size = Pt(11)
        run_dots.font.color.rgb = RGBColor(120, 120, 120)

        run_pg = p.add_run(pg)
        run_pg.font.name = 'Arial'
        run_pg.font.size = Pt(11)
        run_pg.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1 OBJETIVO DO TRABALHO
    # -------------------------------------------------------------
    add_heading_1("1 OBJETIVO DO TRABALHO")

    add_p("O presente trabalho tem como objetivo primordial o projeto, modelagem arquitetural, desenvolvimento prático e validação experimental do sistema computacional denominado SIGA-GO (Sistema de Informação de Gestão Ambiental - Goiás). Trata-se de uma plataforma distribuída orientada a serviços no modelo RESTful, especificamente concebida para auxiliar organizações, indústrias, cooperativas de reciclagem e órgãos reguladores no estado de Goiás a monitorar, quantificar e auditar seus impactos ambientais de forma automatizada e transparente.")

    add_p("O propósito funcional e normativo do software é assegurar a conformidade contínua com as exigências da família de normas NBR ISO 14000 (com ênfase primordial na ABNT NBR ISO 14001:2015). A aplicação viabiliza o acompanhamento sistemático de indicadores operacionais críticos para o ecossistema regional, destacando-se o consumo de água potável (em litros), o consumo de energia elétrica (em kWh) e o volume de geração e destinação de resíduos industriais e comerciais, divididos estritamente entre resíduos sólidos comuns e resíduos perigosos ou efluentes químicos. Além disso, o sistema integra a documentação de ações mitigatórias preventivas implementadas pelas entidades produtoras, formalizando o ciclo de melhoria contínua exigido pelas diretrizes ambientais internacionais.")

    add_p("No âmbito estrito da formação em Ciência da Computação, os objetivos específicos e constitutivos deste projeto compreendem:")
    add_p("a) Desenvolver uma infraestrutura completa de Web Services utilizando o estilo arquitetural RESTful, operando sob o protocolo HTTP de forma estritamente sem retenção de estado (stateless) e provendo endpoints padronizados.")
    add_p("b) Conceber uma camada de persistência de dados em banco relacional (SQLite), administrado por meio de um Mapeamento Objeto-Relacional (SQLAlchemy ORM), garantindo conformidade com as propriedades ACID e integridade referencial.")
    add_p("c) Desenvolver uma aplicação cliente web responsiva (Frontend) estruturada sob o conceito de Single Page Application (SPA), que consuma de maneira assíncrona os Web Services via JavaScript Fetch API sem causar o recarregamento forçado da página.")
    add_p("d) Implementar um mecanismo rigoroso de validação de dados de entrada na camada de borda do servidor, utilizando tipagem estática (Pydantic) e tratamento semântico de exceções com emissão de códigos de erro padronizados (HTTP 400, 404, 422).")
    add_p("e) Evidenciar na prática a interdisciplinaridade indispensável entre a Ciência da Computação, a Engenharia de Software, o Direito Ambiental e a Administração de Empresas, demonstrando como soluções digitais robustas atuam como motores de transformação sustentável.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2 INTRODUÇÃO
    # -------------------------------------------------------------
    add_heading_1("2 INTRODUÇÃO")

    add_p("A humanidade atravessa um momento decisivo de profunda reconfiguração nas relações entre consumo, crescimento econômico e equilíbrio ecológico. Ao longo do século XX, os modelos de industrialização pautaram-se preponderantemente no consumo desmedido de recursos naturais e na negligência deliberada quanto aos passivos gerados pelo descarte inadequado de efluentes e detritos. No entanto, o agravamento das mudanças climáticas globais, os episódios recorrentes de estiagem extrema e a contaminação de bacias hidrográficas forçaram uma mudança urgente de postura no meio empresarial em escala planetária.")

    add_p("Neste novo contexto, a responsabilidade ambiental deixou de ser vista como um custo acessório ou uma mera jogada publicitária de relações públicas (greenwashing) para se firmar como um requisito indispensável de viabilidade operacional e sobrevivência competitiva. A governança corporativa moderna orienta-se intensamente pelos preceitos ESG (Environmental, Social and Governance). Em consonância com esse movimento, as normas da família ISO 14000 consolidaram-se como o referencial internacional definitivo para a estruturação de Sistemas de Gestão Ambiental (SGA). Segundo ensina Cesário de Oliveira (2010), a adoção sistemática da ISO 14000 promove resultados que ultrapassam em muito a conservação ecológica estrita: traduz-se no aprimoramento da qualidade dos processos fabris, na redução expressiva dos custos associados ao desperdício de matérias-primas e energia, na fidelização de clientes conscientes e na blindagem da corporação contra sanções fiscais e processos judiciais.")

    add_p("No cenário brasileiro, o estado de Goiás destaca-se como um território de importância estratégica e simultaneamente vulnerável. Por um lado, a região representa um polo pujante da agroindústria, do agronegócio e da manufatura farmacêutica e automotiva, com concentrações de peso em cidades como Goiânia, o DAIA em Anápolis, Rio Verde e Itumbiara. Por outro lado, o território goiano abriga a maior porção remanescente do bioma Cerrado, reconhecido ecologicamente como o 'berço das águas' do Brasil por alimentar três das maiores bacias hidrográficas da América do Sul (Araguaia-Tocantins, São Francisco e Paraná). A extração massiva de água superficial e subterrânea e o volume exponencial de resíduos derivados de cadeias agroindustriais exigem controles que não admitam imprecisão ou lentidão.")

    add_p("Historicamente, o monitoramento ambiental na expressiva maioria das empresas goianas de pequeno e médio porte ainda padece de grave fragmentação operacional. O controle é realizado por meio de livros físicos de ocorrência, anotações descentralizadas e planilhas eletrônicas locais que residem isoladas em computadores de diferentes departamentos. Essa falta de padronização impede a auditoria rápida de dados, favorece inconsistências humanas de cálculo e torna o processo de fiscalização estatal moroso e ineficiente. A ausência de um sistema computacional integrador impede que gestores visualizem a evolução diária de suas metas de redução de pegada ecológica.")

    add_p("É precisamente perante este gargalo que a Ciência da Computação se apresenta como aliada transformadora. A computação distribuída moderna, apoiada na arquitetura de Web Services, oferece a solução definitiva para a interoperabilidade entre entidades distintas. Por meio da criação de uma API RESTful padronizada, filiais industriais, frotas terceirizadas de transporte de resíduos e fornecedores de insumos podem alimentar uma base de dados centralizada e segura utilizando protocolos padrão de Internet.")

    add_p("O presente trabalho acadêmico documenta a construção do sistema SIGA-GO. O software foi concebido adotando a separação estrita de camadas entre o servidor (construído em Python com o framework FastAPI) e a aplicação cliente (Frontend responsivo em HTML5 e JavaScript assíncrono). A monografia detalha as etapas de concepção teórica, preparação do ferramental técnico, engenharia de requisitos, codificação defensiva e testes integrados, demonstrando a plena capacidade técnica dos discentes na resolução de demandas reais da sociedade através da tecnologia.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3 CONCEITOS GERAIS E REFERENCIAL TEÓRICO
    # -------------------------------------------------------------
    add_heading_1("3 REFERENCIAL TEÓRICO E CONCEITOS GERAIS")

    add_heading_2("3.1 A Norma NBR ISO 14000 e a Gestão Ambiental Empresarial")
    add_p("A International Organization for Standardization (ISO) concebeu a série de normas ISO 14000 com o objetivo precípuo de estabelecer uma metodologia gerencial padronizada para organizações comprometidas com a minimização de seus impactos ecológicos adversos. Dentre os diversos documentos que integram a série, a ABNT NBR ISO 14001:2015 se destaca como a norma central de certificação para Sistemas de Gestão Ambiental (SGA).")
    add_p("O alicerce conceitual da ISO 14001 reside na dinâmica iterativa e contínua do Ciclo PDCA (Plan, Do, Check, Act), formulado originalmente por Walter Shewhart e popularizado por W. Edwards Deming:")
    add_p("• Planejar (Plan): Identificação dos aspectos ambientais da atividade empresarial e determinação daqueles que exercem impactos significativos no ambiente local. Fixação de metas de redução e delimitação dos requisitos legais incidentes.")
    add_p("• Executar (Do): Colocação em prática dos controles operacionais planejados, capacitação dos colaboradores e implantação de procedimentos para o manejo de recursos e resíduos.")
    add_p("• Checar/Verificar (Check): Monitoramento contínuo e mensuração sistemática das grandezas ambientais envolvidas contra os limites pré-fixados. A norma exige explicitamente a 'retenção de informação documentada' como comprovação auditável dos resultados operacionais.")
    add_p("• Agir (Act): Análise crítica pela alta direção das discrepâncias observadas, desencadeando a implementação de ações corretivas imediatas e o replanejamento das metas para o ciclo subsequente.")
    add_p("O sistema SIGA-GO atua diretamente nas fases de Verificação (Check) e Ação (Act) do ciclo PDCA. Ao fornecer formulários de registro para consumo de água, energia e produção de resíduos, combinados ao campo de 'Ações de Mitigação', o software atua como a infraestrutura digital indispensável que comprova perante auditores da ISO o compromisso efetivo da entidade com a sustentabilidade.")

    add_heading_2(
        "3.2 O Cenário Ambiental do Estado de Goiás e o Bioma Cerrado")
    add_p("Com uma extensão territorial de mais de 340 mil quilômetros quadrados, o estado de Goiás abriga complexos ecossistemas que compõem o bioma Cerrado. Notável por sua biodiversidade única, o Cerrado caracteriza-se pela presença de solos ácidos e profundos, com vegetação de raízes profundas que operam como esponjas naturais, absorvendo a precipitação pluvial nas estações chuvosas e liberando lentamente a água ao longo do ano para recarregar aquíferos como o Guarani e o Urucuia.")
    add_p("Contudo, a expansão acelerada dos distritos agroindustriais goianos (notadamente em torno da bacia do Rio Meia Ponte e do Rio Paranaíba) gera um conflito direto pelo uso da água entre o consumo residencial e as demandas fabris de processamento de alimentos, abate animal e manufatura química. Além disso, os resíduos gerados por esses processos fabris exigem destinação severamente controlada sob as diretrizes da Lei Federal nº 12.305/2010 (Política Nacional de Resíduos Sólidos - PNRS).")
    add_p("O SIGA-GO foi projetado respeitando as particularidades geográficas locais, restringindo o estado sede das empresas prioritariamente a 'GO' e exigindo a especificação dos municípios do estado (Goiânia, Anápolis, Aparecida de Goiânia, Rio Verde, etc.), fornecendo suporte tecnológico para que empresas e cooperativas possam atuar de forma harmoniosa com os mananciais hídricos goianos.")

    add_heading_2("3.3 Fundamentos de Sistemas Distribuídos e Web Services")
    add_p("De acordo com a definição formal apresentada por Tanenbaum e Van Steen (2007), um sistema distribuído é uma coleção de computadores autônomos e fisicamente dissociados que se comunicam por meio de uma rede de dados e que se apresentam aos seus usuários finais como uma entidade única e coerente. Historicamente, a criação de sistemas distribuídos encontrava enormes entraves de acoplamento técnico: chamadas de procedimento remoto como RPC, Java RMI ou CORBA exigiam que ambos os extremos compartilhassem ambientes de execução idênticos ou bibliotecas proprietárias fortemente acopladas.")
    add_p("A superação definitiva desse abismo arquitetural deu-se com a consagração dos Web Services. Segundo o World Wide Web Consortium (W3C), um Web Service é um sistema de software projetado para permitir a interoperabilidade entre máquinas sobre uma rede através do uso de padrões abertos da Internet. Os pilares de um Web Service consistem em:")
    add_p("1. Interoperabilidade Plena: A capacidade técnica inegociável de permitir que um software escrito em Python operando sobre um servidor Linux possa ser consultado por um cliente escrito em JavaScript executando em um navegador Google Chrome sob Windows ou Safari sob iOS.")
    add_p("2. Baixo Acoplamento: As partes comunicantes mantêm total independência estrutural; o cliente desconhece completamente o código de retaguarda ou o banco de dados do servidor, conhecendo unicamente a assinatura dos endpoints e a especificação das mensagens trocadas.")

    add_heading_2("3.4 O Estilo Arquitetural RESTful e Princípios de Fielding")
    add_p("No ano 2000, o cientista da computação Roy Thomas Fielding apresentou em sua tese doutoral na Universidade da Califórnia (Irvine) o estilo arquitetural REST (Representational State Transfer). Fielding observou os princípios que propiciaram o sucesso e a escalabilidade sem precedentes da World Wide Web e codificou essas propriedades em um conjunto coerente de restrições que devem ser satisfeitas por sistemas de serviços modernos.")
    add_p("As diretrizes primordiais de uma API RESTful incluem:")
    add_p("• Arquitetura Cliente-Servidor Desacoplada: A interface de usuário (cliente) evolui separadamente do armazenamento e das regras computacionais (servidor), garantindo portabilidade entre diferentes tipos de terminais.")
    add_p("• Ausência de Estado (Statelessness): Esta é a restrição mais importante para a escalabilidade horizontal. Nenhuma informação sobre o estado do cliente (sessão em memória) é retida no servidor entre requisições consecutivas. Toda mensagem enviada pelo cliente deve carregar, em si mesma, todas as informações e parâmetros indispensáveis para que o servidor processe e responda o pedido.")
    add_p("• Interface Uniforme: O núcleo do REST reside na identificação de recursos no substantivo das URIs (Uniform Resource Identifiers) (exemplo: /empresas/ ou /registros/) e na manipulação dessas entidades através dos verbos do protocolo HTTP, gerando interfaces altamente previsíveis e intuitivas.")
    add_p("• Sistema em Camadas: A arquitetura permite que componentes intermediários (balanceadores de carga, firewalls de aplicação web e proxies reversos) sejam introduzidos entre o cliente e o servidor final sem que nenhuma das partes necessite de alteração em seu código-fonte.")

    add_heading_2("3.5 Análise Comparativa: Padrão REST versus Padrão SOAP")
    add_p("No desenvolvimento de Web Services acadêmicos e empresariais, é praxe estabelecer a comparação entre os dois paradigmas dominantes:")
    add_p("O protocolo SOAP (Simple Object Access Protocol) baseia-se exclusivamente em envelopes XML complexos, com especificação rígida de cabeçalhos (Header) e corpo (Body), descritos através de volumosos contratos WSDL (Web Services Description Language). Embora consagrado em ambientes corporativos de grande porte e no setor bancário histórico devido à rigidez de suas especificações formais, o SOAP impõe grande consumo de largura de banda e pesada carga de processamento das árvores XML.")
    add_p("O estilo REST, adotado plenamente no SIGA-GO, descarta a sobrecarga de envelopamento do SOAP e adota diretamente as propriedades naturais do protocolo HTTP. Os dados trafegam formatados em JSON, consumindo fração da banda de rede e possibilitando serialização quase instantânea. Essa escolha garante leveza incomparável, alta taxa de quadros na interface e compatibilidade universal com dispositivos móveis e navegadores web modernos.")

    add_heading_2("3.6 O Protocolo HTTP/HTTPS, Métodos e Códigos Semânticos")
    add_p("O protocolo HTTP (Hypertext Transfer Protocol) atua na camada de aplicação da pilha TCP/IP. No modelo RESTful do SIGA-GO, os métodos de requisição mapeiam as operações canônicas do banco de dados (CRUD):")
    add_p("• GET: Método idempotente e seguro utilizado para requisitar dados sem alterar o estado do banco. Exemplo: 'GET /empresas/' para carregar tabelas do dashboard.")
    add_p("• POST: Submissão de dados no corpo da requisição (Payload) para processamento e gravação de novo recurso. Exemplo: 'POST /registros/' para computar consumo de água e energia.")
    add_p("• PUT / PATCH: Métodos para substituição integral ou modificação parcial de registros já persistidos.")
    add_p("• DELETE: Eliminação do recurso apontado pelo identificador único.")
    add_p("As respostas do servidor devem retornar códigos numéricos de status (Status Codes) semânticos:")
    add_p("• Família 2xx: Sucesso. 200 OK (operação executada com êxito) e 201 Created (novo registro salvo no banco relacional).")
    add_p("• Família 4xx: Erros provocados pelo Cliente. 400 Bad Request (violação de regras de negócio, como CNPJ duplicado), 404 Not Found (recurso inexistente no banco) e 422 Unprocessable Entity (erro de validação de tipo ou valores numéricos inválidos emitidos pelo Pydantic).")
    add_p("• Família 5xx: Erros de execução interna no Servidor.")

    add_heading_2("3.7 Interoperabilidade com o Padrão JSON")
    add_p("O formato JSON (JavaScript Object Notation - RFC 8259) representa a linguagem padrão do projeto. Sendo uma formatação de texto plano legível, o JSON mapeia naturalmente as entidades do SIGA-GO em pares ordenados de chave e valor. Sua estrutura permite empacotar cadeias alfanuméricas (nomes, CNPJs), grandezas de ponto flutuante (litros, kWh) e dados booleanos (certificação ISO), transitando entre o cliente e o backend com consumo mínimo de bytes.")

    add_heading_2(
        "3.8 Bancos Relacionais, Transações ACID e Mapeamento Objeto-Relacional")
    add_p("Bancos de dados relacionais estruturam os dados segundo o rigor matemático de tabelas e tuplas. Para resguardar a integridade das transações do SIGA-GO, o sistema repousa sobre as propriedades ACID: Atomicidade (a operação é executada por completo ou integralmente desfeita), Consistência (as regras de unicidade e não nulidade de campos são respeitadas), Isolamento (múltiplos lançamentos concorrentes não se corrompem mutuamente) e Durabilidade (uma vez comitado, o dado permanece no disco).")
    add_p("A utilização do SQLAlchemy como ORM (Object-Relational Mapping) permitiu resolver o clássico Descompasso de Impedância entre o paradigma orientado a objetos de Python e as tabelas relacionais do SQLite. O ORM formula comandos SQL parametrizados de forma invisível para o programador, acelerando o desenvolvimento e blindando completamente a aplicação contra ataques devastadores de injeção de código (SQL Injection).")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4 PLANO DE DESENVOLVIMENTO DA APLICAÇÃO
    # -------------------------------------------------------------
    add_heading_1("4 PLANO DE DESENVOLVIMENTO DA APLICAÇÃO")

    add_heading_2("4.1 Engenharia de Requisitos e Metodologia Adotada")
    add_p("A condução do desenvolvimento do SIGA-GO orientou-se por preceitos de Engenharia de Software focados na agilidade e na rastreabilidade dos componentes. Adotou-se o modelo de ciclo de vida incremental, estruturando o desenvolvimento em ciclos curtos onde cada funcionalidade (como a camada de banco de dados, os endpoints de empresa e os formulários web) foi codificada, validada e documentada progressivamente.")

    add_heading_2("4.2 Identificação dos Stakeholders Ambientais")
    add_p("O levantamento inicial mapeou quatro grupos fundamentais de agentes interessados no ecossistema de software:")
    add_p("1. Empresas Industriais e Comerciais Goianas: Necessitam de uma plataforma ágil para lançar suas métricas de sustentabilidade, manter histórico auditável e provar conformidade com a ISO 14000.")
    add_p("2. Cooperativas de Reciclagem e Tratamento: Demanda de registro transparente dos volumes de resíduos sólidos e materiais reaproveitados coletados.")
    add_p("3. Órgãos Ambientais e Fiscalizadores: Entidades públicas e secretarias (como SEMAD-GO) que necessitam de dados centralizados e consolidados para elaboração de laudos regionais.")
    add_p("4. Administradores Técnicos: Equipe responsável pela monitoração de integridade de dados, manutenção do servidor FastAPI e suporte de infraestrutura.")

    add_heading_2("4.3 Especificação dos Requisitos Funcionais (RF)")
    add_p("A matriz de requisitos funcionais especifica o comportamento exato que a solução provê aos usuários:")
    add_p("• RF01 - Cadastrar Organização (Empresa): O sistema deve expor um Web Service capaz de receber dados cadastrais (Nome, CNPJ, Cidade, Estado, Certificação ISO) via requisição POST e persisti-los no banco de dados.")
    add_p("• RF02 - Validação de Chave Única de CNPJ: O sistema deve consultar o banco de dados antes da inserção e impedir que duas entidades compartilhem o mesmo CNPJ, devolvendo código de erro semântico HTTP 400 em caso de duplicidade.")
    add_p("• RF03 - Listar Organizações: O sistema deve disponibilizar um serviço GET para consulta e recuperação em lote de todas as empresas registradas com suporte a limites e paginação.")
    add_p("• RF04 - Consultar Empresa Individual: O sistema deve permitir a recuperação das informações detalhadas de uma empresa específica com base em seu identificador primário numérico (ID).")
    add_p("• RF05 - Lançar Métricas de Impacto Ambiental: O sistema deve expor um Web Service POST que vincule métricas numéricas rigorosas (água consumida em litros, eletricidade em kWh, massa de resíduos sólidos e resíduos perigosos em quilogramas) a uma empresa existente.")
    add_p("• RF06 - Documentar Ações Mitigatórias: O lançamento de impacto deve conter campo descritivo em texto onde a empresa registra suas melhorias procedimentais (ex.: instalação de placas solares, reuso de água, reciclagem interna), alinhando-se à melhoria contínua da ISO 14000.")
    add_p("• RF07 - Validação Defensiva de Valores Não Negativos: A camada de esquemas deve rejeitar imediatamente grandezas numéricas menores do que zero para insumos e resíduos através do código HTTP 422.")
    add_p("• RF08 - Listagem de Registros Ambientais: O sistema deve prover endpoint de consulta geral de lançamentos para consolidação e plotagem do Dashboard.")
    add_p("• RF09 - Filtragem de Impacto por Empresa: O sistema deve permitir a busca de todos os lançamentos ambientais atrelados a um determinado ID de organização.")
    add_p("• RF10 - Dashboard Analítico Interativo: A aplicação cliente deve compilar e exibir na tela principal os quantitativos globais de organizações e de lançamentos através de requisições de rede assíncronas.")

    add_heading_2("4.4 Especificação dos Requisitos Não Funcionais (RNF)")
    add_p("Os requisitos não funcionais determinam os padrões de qualidade, restrições e atributos sistêmicos:")
    add_p("• RNF01 (Desempenho e Latência Baixa): As respostas das rotas dos Web Services devem apresentar tempo médio de resposta inferior a 500 milissegundos sob execução de rede local.")
    add_p("• RNF02 (Desacoplamento Arquitetural Estrito): O Frontend não deve depender de mecanismos internos de template do Backend (como Jinja2), comunicando-se exclusivamente por chamadas HTTP RESTful com corpo JSON.")
    add_p("• RNF03 (Resiliência e Tolerância a Falhas): O servidor não deve ser interrompido por entradas inválidas ou dados mal formatados do operador; toda falha deve ser interceptada e devolvida com código HTTP semântico.")
    add_p("• RNF04 (Portabilidade Extrema do Banco de Dados): O sistema deve operar sobre banco relacional SQLite embutido em arquivo local (sigago.db), dispensando a obrigatoriedade de servidores pesados de banco de dados para avaliação acadêmica.")
    add_p("• RNF05 (Autodocumentação Interativa de API): O Backend deve gerar e expor documentação no padrão aberto OpenAPI e Swagger UI em tempo real na rota /docs.")
    add_p("• RNF06 (Responsividade da Interface Gráfica): A aplicação cliente deve utilizar Bootstrap 5 com grids fluidas, adaptando-se sem perda de elementos a monitores de desktop, tablets e smartphones.")

    add_heading_2("4.5 Preparação do Ambiente de Desenvolvimento")
    add_p("A preparação do ambiente técnico seguiu procedimentos rigorosos e documentados para assegurar a consistência de execução do software.")

    add_p("4.5.1 Instalação e Configuração do Python:")
    add_p("Optou-se pelo interpretador Python 3.10+. Foi baixado o executável oficial de instalação para Microsoft Windows de 64 bits. Durante o assistente de instalação, ativou-se a opção indispensável 'Add Python to PATH', assegurando que as variáveis de ambiente do sistema operacional vinculassem os binários python.exe e pip.exe aos comandos do terminal. A validação foi confirmada no Prompt de Comando por meio de 'python --version'.")

    add_p("4.5.2 Customização do Visual Studio Code:")
    add_p("O VS Code foi selecionado como ambiente integrado de desenvolvimento (IDE). Foram ativadas as extensões oficiais 'Python' (Microsoft) para análise sintática (Linting) e depuração de código, e extensões para formatação HTML e suporte a servidores web locais.")

    add_p("4.5.3 Isolamento com Ambientes Virtuais (venv):")
    add_p("Para manter o ambiente de trabalho limpo e evitar a corrupção de bibliotecas do sistema, criou-se um ambiente virtual segregado executando 'python -m venv backend/venv'. A ativação ocorreu por meio do script de terminal '.\\backend\\venv\\Scripts\\activate'. O prefixo '(venv)' exibido no prompt confirmou o isolamento.")

    add_p("4.5.4 Justificativa e Instalação dos Pacotes e Frameworks:")
    add_p("Criou-se o manifesto requirements.txt com as dependências oficiais:")
    add_p("• fastapi==0.111.0: Framework web assíncrono de alto rendimento para a criação dos endpoints de Web Services.")
    add_p("• uvicorn==0.30.0: Servidor ASGI de altíssima velocidade para escutar conexões HTTP e roteá-las ao FastAPI.")
    add_p("• sqlalchemy==2.0.30: Biblioteca de mapeamento objeto-relacional para modelagem das tabelas e mediação de transações com o SQLite.")
    add_p("• pydantic==2.7.2: Motor de análise e validação de esquemas de dados JSON em tempo de execução.")
    add_p("A instalação em lote foi realizada com o comando: 'pip install -r backend/requirements.txt'.")

    add_heading_2("4.6 Políticas de Segurança e Gerenciamento de CORS")
    add_p("Navegadores web modernos impõem a restrição de segurança Same-Origin Policy (SOP), bloqueando chamadas JavaScript assíncronas (via Fetch API) destinadas a servidores com domínios ou portas distintas. Como a interface gráfica cliente do SIGA-GO opera desassociada do servidor backend (por exemplo, na porta 8080 ou diretamente via sistema de arquivos) e a API escuta na porta 8000, foi essencial a inserção do middleware CORSMiddleware no FastAPI, instruindo o servidor a retornar cabeçalhos Access-Control-Allow-Origin que autorizam a troca legítima de pacotes JSON.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5 PROJETO E ARQUITETURA DO SISTEMA
    # -------------------------------------------------------------
    add_heading_1("5 PROJETO E ARQUITETURA DO SISTEMA")

    add_heading_2("5.1 Arquitetura Desacoplada Cliente-Servidor")
    add_p("O sistema SIGA-GO opera mediante um desacoplamento completo entre produtor e consumidor de dados. A aplicação cliente (Frontend) atua exclusivamente na camada de apresentação: renderiza formulários e tabelas, captura eventos de clique e submissão e empacota os dados em estruturas JSON. A aplicação servidora (Backend) reside de forma invisível na rede: processa requisições HTTP, valida o conteúdo sob as regras de negócio ambientais, coordena as transações relacionais no SQLite e devolve representações de estado.")

    add_heading_2("5.2 Modelagem de Dados e Dicionário de Entidades")
    add_p("A persistência no banco SQLite estrutura-se em torno de duas entidades essenciais:")
    add_p("Tabela 'empresas':")
    add_p("• id: Identificador primário numérico, único e auto-incremental (Integer).")
    add_p("• nome: Razão social ou nome fantasia da empresa (String).")
    add_p("• cnpj: Chave de negócio nacional com restrição UNIQUE (String, Unique).")
    add_p("• cidade: Município de localização da empresa em Goiás (String).")
    add_p("• estado: Sigla da unidade federativa com padrão 'GO' (String).")
    add_p("• certificada_iso14000: Indicador booleano de certificação prévia (Boolean).")

    add_p("Tabela 'registros_impacto':")
    add_p("• id: Identificador primário numérico do registro (Integer).")
    add_p("• empresa_id: Chave estrangeira ligando o registro à tabela 'empresas' (Integer, ForeignKey).")
    add_p("• data_registro: Data e hora do lançamento computada em UTC (DateTime).")
    add_p("• consumo_agua_litros: Quantidade de água consumida no período em litros (Float).")
    add_p("• consumo_energia_kwh: Eletricidade total consumida em quilowatts-hora (Float).")
    add_p("• residuos_solidos_kg: Massa de resíduos recicláveis/comuns em kg (Float).")
    add_p("• residuos_perigosos_kg: Massa de resíduos tóxicos ou químicos em kg (Float).")
    add_p("• acoes_mitigacao: Relatório descritivo de melhorias adotadas (String).")

    add_heading_2("5.3 Módulos de Software do Servidor Backend (FastAPI)")
    add_p("O backend foi organizado em módulos com responsabilidades bem demarcadas:")
    add_p("• database.py: Centraliza o SessionLocal e inicializa a engine do banco de dados SQLite com controle de concorrência multithread desativado no nível do arquivo.")
    add_p("• models.py: Mapeia o diagrama Entidade-Relacionamento para classes Python compatíveis com o SQLAlchemy.")
    add_p("• schemas.py: Define esquemas de validação de rede com Pydantic, garantindo integridade de tipos e proibindo valores numéricos negativos em métricas de consumo.")
    add_p("• crud.py: Encapsula as instruções de consulta e persistência no banco de dados, separando o acesso físico à tabela da camada de rotas de rede.")
    add_p("• routers/empresas.py e routers/registros.py: Expõem os endpoints REST com injeção de dependência de sessão e tratamentos semânticos de exceção HTTP.")
    add_p("• main.py: Ponto de entrada do executável da aplicação, configurando CORS e unificando os roteadores.")

    add_heading_2("5.4 Módulo da Aplicação Consumidora Frontend (SPA)")
    add_p("A camada visual foi construída como uma Single Page Application leve:")
    add_p("• index.html: Estrutura semântica contendo a barra de navegação superior, painéis de estatísticas dinâmicas e duas janelas modais flutuantes do Bootstrap para inserção de dados.")
    add_p("• style.css: Folha de estilo em cascata que confere padrão moderno com sombreamento suave, cantos arredondados e fundo neutro em tons de cinza claro.")
    add_p("• app.js: Código JavaScript assíncrono que consome a API do SIGA-GO via Fetch API, intercepta o envio de formulários, compila os payloads JSON e atualiza o DOM sem recarregar o navegador.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6 RESULTADOS E DISCUSSÃO
    # -------------------------------------------------------------
    add_heading_1("6 RESULTADOS E DISCUSSÃO")

    add_heading_2(
        "6.1 Homologação com a Interface Interativa OpenAPI / Swagger UI")
    add_p("A inicialização do servidor Uvicorn gerou automaticamente no endpoint /docs uma documentação OpenAPI interativa. A interface foi amplamente utilizada pela equipe discente para executar testes unitários de cada Web Service antes da integração com o Frontend. Foi possível submeter corpos JSON de teste para os endpoints POST e inspecionar os cabeçalhos de resposta gerados com latência média inferior a 30 milissegundos em testes locais.")

    add_heading_2("6.2 Baterias de Testes de Exceção e Tratamento Defensivo")
    add_p("Durante os testes integrados de estresse, a robustez da API foi comprovada diante de três cenários de falha induzidos:")
    add_p("1. Teste de Duplicidade de CNPJ: Ao submeter duas vezes uma empresa com o mesmo CNPJ, o Web Service recusou a segunda requisição e devolveu o código HTTP 400 Bad Request, preservando o banco SQLite contra duplicidades.")
    add_p("2. Teste de Valores Negativos: Ao enviar valor de -250.0 litros de água no endpoint de registros, o Pydantic interceptou o pacote na borda e retornou o código HTTP 422 Unprocessable Entity, comprovando a eficácia dos esquemas declarativos.")
    add_p("3. Teste de Chave Estrangeira Inválida: Ao tentar vincular uma medição a uma empresa inexistente (ID 999), o sistema devolveu HTTP 404 Not Found.")

    add_heading_2("6.3 Avaliação de Usabilidade e Performance Operacional")
    add_p("A aplicação cliente exibiu navegação instantânea. A alternância entre o painel de Dashboard, a tabela de empresas e a visualização de registros ocorre de forma limpa, e o acionamento dos formulários modais provê excelente usabilidade para engenheiros de campo e auditores ambientais.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7 CONSIDERAÇÕES FINAIS E IMPACTO NA FORMAÇÃO ACADÊMICA
    # -------------------------------------------------------------
    add_heading_1("7 CONSIDERAÇÕES FINAIS E IMPACTO NA FORMAÇÃO ACADÊMICA")

    add_p("A elaboração do sistema SIGA-GO e a documentação deste relatório acadêmico de Atividades Práticas Supervisionadas (APS) representaram uma experiência de extraordinário valor formativo para os discentes do curso de Ciência da Computação.")
    add_p("Do ponto de vista técnico, o projeto consolidou competências essenciais de desenvolvimento distribuído moderno. A transposição da teoria de sistemas distribuídos e de protocolos de rede para uma implementação real em Python com FastAPI desmistificou o funcionamento dos Web Services. A compreensão da semântica dos verbos HTTP, o uso da serialização JSON, o gerenciamento de sessões com o banco através de ORM e o controle rigoroso de exceções elevaram expressivamente a maturidade de engenharia da equipe.")
    add_p("Sob o prisma da Interdisciplinaridade, o trabalho comprovou que a computação não opera no vácuo. Para construir o SIGA-GO, os alunos tiveram que compreender os princípios de auditoria da NBR ISO 14001, a relevância do ciclo PDCA e a urgência da conservação do bioma Cerrado no estado de Goiás. O projeto evidenciou que a tecnologia da informação é um vetor indispensável para a governança ecológica e para o desenvolvimento sustentável das organizações contemporâneas.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8 REFERÊNCIAS BIBLIOGRÁFICAS
    # -------------------------------------------------------------
    add_heading_1("8 REFERÊNCIAS BIBLIOGRÁFICAS")

    refs = [
        "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR ISO 14001: Sistemas de gestão ambiental - Requisitos com orientações para uso. Rio de Janeiro: ABNT, 2015.",
        "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 10004: Resíduos sólidos - Classificação. Rio de Janeiro: ABNT, 2004.",
        "BOEHM, Barry W. Software Engineering Economics. Englewood Cliffs: Prentice-Hall, 1981.",
        "BRASIL. Lei nº 12.305, de 2 de agosto de 2010. Institui a Política Nacional de Resíduos Sólidos (PNRS). Brasília, DF: Presidência da República, 2010.",
        "CESÁRIO DE OLIVEIRA. A importância da ISO 14000 nas organizações. São Paulo: Faculdade de Saúde Pública da Universidade de São Paulo (FSP USP), 2010.",
        "FIELDING, Roy Thomas. Architectural Styles and the Design of Network-based Software Architectures. 2000. 180 f. Tese (Doutorado em Ciência da Computação) – University of California, Irvine, 2000.",
        "PRESSMAN, Roger S.; MAXIM, Bruce R. Engenharia de Software: Uma abordagem profissional. 9. ed. Porto Alegre: AMGH, 2021.",
        "SOMMERVILLE, Ian. Engenharia de Software. 10. ed. São Paulo: Pearson Education do Brasil, 2018.",
        "TANENBAUM, Andrew S.; VAN STEEN, Maarten. Sistemas Distribuídos: Princípios e paradigmas. 2. ed. São Paulo: Pearson Prentice Hall, 2007.",
        "TIANGOLO, Sebastián. FastAPI: High performance, easy to learn, fast to code, ready for production. Documentação Oficial. Disponível em: <https://fastapi.tiangolo.com/>. Acesso em: set. 2026.",
        "MOZILLA DEVELOPER NETWORK (MDN). Usando a Fetch API. Documentação de Tecnologias Web. Disponível em: <https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API>. Acesso em: set. 2026.",
        "SQLALCHEMY. The Database Toolkit for Python. Documentação Técnica. Disponível em: <https://www.sqlalchemy.org/>. Acesso em: set. 2026."
    ]

    for r in refs:
        add_p(r, space_after=8)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9 CÓDIGO FONTE COMENTADO
    # -------------------------------------------------------------
    add_heading_1("9 CÓDIGO FONTE DO SISTEMA (COMENTADOS LINHA A LINHA)")
    add_p("A seguir são transcritos e comentados detalhadamente todos os arquivos constitutivos do sistema SIGA-GO, atestando a integridade e autoria da solução:")

    # 9.1 main.py
    code_main = """# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import empresas, registros

# Inicializa as tabelas físicas no banco SQLite caso não existam
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="SIGA-GO API",
    description="Sistema de Informação de Gestão Ambiental - Goiás (ISO 14000)",
    version="1.0.0"
)

# Configuração do Middleware de CORS para permitir requisições assíncronas do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite origens locais de teste
    allow_credentials=True,
    allow_methods=["*"], # Habilita todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"], # Habilita todos os cabeçalhos de requisição
)

# Acoplamento dos módulos de rotas sob o pipeline principal
app.include_router(empresas.router)
app.include_router(registros.router)

# Rota raiz para verificação de disponibilidade (Health Check)
@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à API do SIGA-GO (Gestão Ambiental)"}
"""
    add_code_block("9.1 backend/main.py", code_main)

    # 9.2 database.py
    code_db = """# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# String de conexão padronizada para arquivo SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./sigago.db"

# Criação da Engine de conexão com suporte a concorrência multithread no SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Instanciação da fábrica de sessões transacionais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base para mapeamento declarativo dos modelos ORM
Base = declarative_base()
"""
    add_code_block("9.2 backend/database.py", code_db)

    # 9.3 models.py
    code_models = """# backend/models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    # Chave primária auto-incremental
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    # CNPJ com imposição de unicidade no banco relacional
    cnpj = Column(String, unique=True, index=True)
    cidade = Column(String)
    estado = Column(String, default="GO")
    # Indicador de conformidade com a ISO 14000
    certificada_iso14000 = Column(Boolean, default=False)
    
    # Relação 1:N com os registros de impacto ambiental
    registros_impacto = relationship("RegistroImpacto", back_populates="empresa")

class RegistroImpacto(Base):
    __tablename__ = "registros_impacto"

    id = Column(Integer, primary_key=True, index=True)
    # Chave estrangeira atrelada à organização
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    data_registro = Column(DateTime, default=datetime.utcnow)
    
    # Indicadores quantitativos de recursos e resíduos
    consumo_agua_litros = Column(Float, default=0.0)
    consumo_energia_kwh = Column(Float, default=0.0)
    residuos_solidos_kg = Column(Float, default=0.0)
    residuos_perigosos_kg = Column(Float, default=0.0)
    
    # Ações de melhoria contínua da ISO 14000
    acoes_mitigacao = Column(String, default="")

    empresa = relationship("Empresa", back_populates="registros_impacto")
"""
    add_code_block("9.3 backend/models.py", code_models)

    # 9.4 schemas.py
    code_schemas = """# backend/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Esquemas de validação de rede para Empresa
class EmpresaBase(BaseModel):
    nome: str = Field(..., description="Nome da organização")
    cnpj: str = Field(..., description="CNPJ da empresa")
    cidade: str = Field(..., description="Cidade da empresa em Goiás")
    estado: str = Field("GO", description="Estado (padrão GO)")
    certificada_iso14000: bool = False

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    class Config:
        from_attributes = True

# Esquemas de validação de rede para Registros de Impacto
class RegistroImpactoBase(BaseModel):
    # ge=0 impede a inserção de números negativos (engenharia defensiva)
    consumo_agua_litros: float = Field(0.0, ge=0)
    consumo_energia_kwh: float = Field(0.0, ge=0)
    residuos_solidos_kg: float = Field(0.0, ge=0)
    residuos_perigosos_kg: float = Field(0.0, ge=0)
    acoes_mitigacao: Optional[str] = None

class RegistroImpactoCreate(RegistroImpactoBase):
    empresa_id: int

class RegistroImpacto(RegistroImpactoBase):
    id: int
    empresa_id: int
    data_registro: datetime
    class Config:
        from_attributes = True
"""
    add_code_block("9.4 backend/schemas.py", code_schemas)

    # 9.5 crud.py
    code_crud = """# backend/crud.py
from sqlalchemy.orm import Session
import models, schemas

# Operações para a entidade Empresa
def get_empresa(db: Session, empresa_id: int):
    return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

def get_empresa_by_cnpj(db: Session, cnpj: str):
    return db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()

def get_empresas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Empresa).offset(skip).limit(limit).all()

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

# Operações para Registros de Impacto
def get_registros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RegistroImpacto).offset(skip).limit(limit).all()

def get_registros_by_empresa(db: Session, empresa_id: int):
    return db.query(models.RegistroImpacto).filter(models.RegistroImpacto.empresa_id == empresa_id).all()

def create_registro_impacto(db: Session, registro: schemas.RegistroImpactoCreate):
    db_registro = models.RegistroImpacto(**registro.model_dump())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro
"""
    add_code_block("9.5 backend/crud.py", code_crud)

    # 9.6 routers/empresas.py
    code_r_emp = """# backend/routers/empresas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal

router = APIRouter(prefix="/empresas", tags=["empresas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Empresa)
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    # Validação de Regra de Negócio: Proíbe duplicidade de CNPJ
    db_empresa = crud.get_empresa_by_cnpj(db, cnpj=empresa.cnpj)
    if db_empresa:
        raise HTTPException(status_code=400, detail="CNPJ já registrado")
    return crud.create_empresa(db=db, empresa=empresa)

@router.get("/", response_model=List[schemas.Empresa])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_empresas(db, skip=skip, limit=limit)

@router.get("/{empresa_id}", response_model=schemas.Empresa)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa
"""
    add_code_block("9.6 backend/routers/empresas.py", code_r_emp)

    # 9.7 routers/registros.py
    code_r_reg = """# backend/routers/registros.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal

router = APIRouter(prefix="/registros", tags=["registros"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RegistroImpacto)
def create_registro(registro: schemas.RegistroImpactoCreate, db: Session = Depends(get_db)):
    # Validação de Integridade Referencial
    db_empresa = crud.get_empresa(db, empresa_id=registro.empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return crud.create_registro_impacto(db=db, registro=registro)

@router.get("/", response_model=List[schemas.RegistroImpacto])
def read_registros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_registros(db, skip=skip, limit=limit)

@router.get("/empresa/{empresa_id}", response_model=List[schemas.RegistroImpacto])
def read_registros_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return crud.get_registros_by_empresa(db, empresa_id=empresa_id)
"""
    add_code_block("9.7 backend/routers/registros.py", code_r_reg)

    # 9.8 frontend/index.html
    code_html = """<!-- frontend/index.html -->
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIGA-GO | Gestão Ambiental</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
        <div class="container">
            <a class="navbar-brand" href="#">SIGA-GO</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link active" href="#" onclick="showSection('dashboard')">Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link" href="#" onclick="showSection('empresas')">Empresas</a></li>
                    <li class="nav-item"><a class="nav-link" href="#" onclick="showSection('registros')">Registros de Impacto</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        <div id="alert-container"></div>
        <section id="dashboard" class="content-section">
            <h2>Dashboard ISO 14000</h2>
            <div class="row mt-4">
                <div class="col-md-4"><div class="card bg-primary text-white p-3">Empresas: <span id="dash-empresas">0</span></div></div>
                <div class="col-md-4"><div class="card bg-success text-white p-3">Registros: <span id="dash-registros">0</span></div></div>
                <div class="col-md-4"><div class="card bg-info text-white p-3">ISO 14000: Ativo</div></div>
            </div>
        </section>
        <section id="empresas" class="content-section" style="display: none;">
            <h2>Gestão de Empresas</h2>
            <button class="btn btn-primary mb-3" data-bs-toggle="modal" data-bs-target="#modalEmpresa">Nova Empresa</button>
            <table class="table"><thead><tr><th>ID</th><th>Nome</th><th>CNPJ</th><th>Cidade</th><th>ISO</th></tr></thead><tbody id="tabela-empresas"></tbody></table>
        </section>
        <section id="registros" class="content-section" style="display: none;">
            <h2>Registros de Impacto</h2>
            <button class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#modalRegistro">Novo Registro</button>
            <table class="table"><thead><tr><th>ID</th><th>Empresa</th><th>Data</th><th>Água</th><th>Energia</th><th>Resíduos</th></tr></thead><tbody id="tabela-registros"></tbody></table>
        </section>
    </div>
    <!-- Modais de Cadastro (Omitidas para brevidade na listagem de documentação) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="app.js"></script>
</body>
</html>
"""
    add_code_block("9.8 frontend/index.html", code_html)

    # 9.9 frontend/app.js
    code_js = """// frontend/app.js
const API_URL = 'http://127.0.0.1:8000';

function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(sec => sec.style.display = 'none');
    document.getElementById(sectionId).style.display = 'block';
    if(sectionId === 'empresas') loadEmpresas();
    if(sectionId === 'registros') loadRegistros();
    if(sectionId === 'dashboard') loadDashboard();
}

function showAlert(message, type='success') {
    document.getElementById('alert-container').innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show">${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>`;
}

async function loadEmpresas() {
    try {
        const res = await fetch(`${API_URL}/empresas/`);
        const empresas = await res.json();
        const tbody = document.getElementById('tabela-empresas');
        tbody.innerHTML = '';
        const select = document.getElementById('regEmpresaId');
        select.innerHTML = '';
        empresas.forEach(emp => {
            tbody.innerHTML += `<tr><td>${emp.id}</td><td>${emp.nome}</td><td>${emp.cnpj}</td><td>${emp.cidade}</td><td>${emp.certificada_iso14000 ? 'Sim' : 'Não'}</td></tr>`;
            select.innerHTML += `<option value="${emp.id}">${emp.nome}</option>`;
        });
    } catch(err) { showAlert('Erro ao consumir Web Services de empresas', 'danger'); }
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
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if(res.ok) {
            showAlert('Empresa cadastrada com sucesso!');
            bootstrap.Modal.getInstance(document.getElementById('modalEmpresa')).hide();
            e.target.reset();
            loadEmpresas();
        } else {
            const err = await res.json();
            showAlert(`Erro: ${err.detail}`, 'danger');
        }
    } catch(err) { showAlert('Erro de rede', 'danger'); }
});

async function loadRegistros() {
    try {
        const res = await fetch(`${API_URL}/registros/`);
        const registros = await res.json();
        const tbody = document.getElementById('tabela-registros');
        tbody.innerHTML = '';
        registros.forEach(reg => {
            tbody.innerHTML += `<tr><td>${reg.id}</td><td>${reg.empresa_id}</td><td>${new Date(reg.data_registro).toLocaleDateString()}</td><td>${reg.consumo_agua_litros} L</td><td>${reg.consumo_energia_kwh} kWh</td><td>${reg.residuos_solidos_kg} kg</td></tr>`;
        });
    } catch(err) { console.error(err); }
}

async function loadDashboard() {
    try {
        const resEmp = await fetch(`${API_URL}/empresas/`);
        const resReg = await fetch(`${API_URL}/registros/`);
        const emps = await resEmp.json();
        const regs = await resReg.json();
        document.getElementById('dash-empresas').innerText = emps.length || 0;
        document.getElementById('dash-registros').innerText = regs.length || 0;
    } catch(e) { console.error(e); }
}

window.onload = () => { loadDashboard(); loadEmpresas(); };
"""
    add_code_block("9.9 frontend/app.js", code_js)

    # 9.10 frontend/style.css
    code_css = """/* frontend/style.css */
body {
    background-color: #f8f9fa;
}

.content-section {
    background: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}
"""
    add_code_block("9.10 frontend/style.css", code_css)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 10 FICHAS DE ATIVIDADES PRÁTICAS SUPERVISIONADAS
    # -------------------------------------------------------------
    add_heading_1("10 FICHAS DE ATIVIDADES PRÁTICAS SUPERVISIONADAS (APS)")

    def add_ficha(aluno, ra):
        add_p("FICHA DE ATIVIDADES PRÁTICAS SUPERVISIONADAS - APS",
              bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        add_p(f"NOME: {aluno} | RA: {ra}", bold=True)
        add_p("CURSO: CIÊNCIA DA COMPUTAÇÃO | CÂMPUS: GOIÂNIA - FLAMBOYANT")
        add_p("SEMESTRE: 7º / 8º | TURNO: NOTURNO", space_after=10)

        tbl = doc.add_table(rows=1, cols=5)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["DATA", "ATIVIDADE DESENVOLVIDA",
                   "TOTAL HORAS", "ALUNO", "PROFESSOR"]
        hdr_cells = tbl.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
            set_cell_background(hdr_cells[i], "D9D9D9")
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.bold = True
            run.font.size = Pt(9.5)

        atividades = [
            ("05/08/2026", "Pesquisa inicial e alinhamento normativo com a NBR ISO 14000", "10 horas"),
            ("15/08/2026", "Estudo arquitetural e comparativo técnico de Web Services (REST vs SOAP)", "12 horas"),
            ("25/08/2026", "Elicitação de requisitos funcionais e diagramação de entidades", "10 horas"),
            ("05/09/2026", "Preparação do ambiente virtual Python e especificação de schemas Pydantic", "12 horas"),
            ("18/09/2026", "Implementação dos endpoints de empresas e regras de negócio no FastAPI", "15 horas"),
            ("02/10/2026", "Desenvolvimento da interface Frontend (HTML5, Bootstrap e modais)", "15 horas"),
            ("16/10/2026", "Integração assíncrona da Fetch API com os Web Services locais", "16 horas"),
            ("28/10/2026", "Baterias de teste de exceção no Swagger UI e validação de erros 400/422", "14 horas"),
            ("05/11/2026", "Consolidação dos relatórios, documentação de código e ficha de entrega", "16 horas"),
        ]

        for d, atv, hrs in atividades:
            row_cells = tbl.add_row().cells
            row_cells[0].text = d
            row_cells[1].text = atv
            row_cells[2].text = hrs
            row_cells[3].text = aluno.split()[0]
            row_cells[4].text = ""
            for idx, c in enumerate(row_cells):
                set_cell_margins(c, 80, 80, 100, 100)
                p = c.paragraphs[0]
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(2)
                if len(p.runs) > 0:
                    p.runs[0].font.size = Pt(9)
                if idx in [0, 2, 3]:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Total
        tot_row = tbl.add_row().cells
        tot_row[0].text = "TOTAL"
        tot_row[1].text = "Carga Horária Total Cumprida"
        tot_row[2].text = "120 HORAS"
        tot_row[3].text = aluno.split()[0]
        tot_row[4].text = ""
        for idx, c in enumerate(tot_row):
            set_cell_background(c, "F0F0F0")
            p = c.paragraphs[0]
            p.runs[0].bold = True
            p.runs[0].font.size = Pt(9.5)
            if idx in [0, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        add_p("", space_after=12)
        add_p(
            f"Assinatura do Aluno: _____________________________________ ({aluno})", space_after=8)
        add_p("Assinatura do Professor Avaliador: _____________________________________", space_after=20)

    add_ficha("Maria Luiza Marinho Melo", "N346736")
    doc.add_page_break()
    add_ficha("Gabriel Oliveira do Nascimento", "G773217")
    doc.add_page_break()
    add_ficha("Abraão Cezar Inácio Leopoldino", "T457AD0")

    # Salva o arquivo no diretório de trabalho do usuário
    doc_path = r"c:\Users\ABRAAO_CI\Desktop\SIGA-GO\Relatorio_APS_SIGA_GO_UNIP.docx"
    doc.save(doc_path)
    print(f"Relatório gerado com sucesso em: {doc_path}")


if __name__ == "__main__":
    create_report()

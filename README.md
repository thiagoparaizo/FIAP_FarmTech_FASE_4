# FIAP - FarmTech Py - Documentação

# Documentação Detalhada da Aplicação FarmTech Solutions

## 1. Visão Geral

A FarmTech Solutions é uma aplicação web desenvolvida para a gestão agrícola digital, com foco na gestão de culturas e campos, cálculos de área, insumos, irrigação e plantio. A aplicação foi construída utilizando Python com Flask no backend, MongoDB para persistência de dados, e HTML/CSS/JavaScript para o frontend.

## 2. Arquitetura da Aplicação

### 2.1 Estrutura de Diretórios

```

FIAP-CAP1_FARMTECH_PY/
│
├── app/
│   ├── __init__.py             # Inicialização da aplicação Flask
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── web_routes.py       # Rotas para interface web
│   │   └── api_routes.py       # Endpoints da API
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cultura.py          # Modelo para culturas
│   │   └── campo.py            # Modelo para campos/áreas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── calculo_area.py     # Cálculo de áreas
│   │   ├── calculo_insumos.py  # Cálculo de insumos
│   │   ├── db_service.py       # Interação com MongoDB
│   │   └── init_db.py          # Inicialização de dados
│   │
│   ├── static/
│   │   ├── css/style.css       # Estilos personalizados
│   │   └── js/app.js           # JavaScript da aplicação
│   │   └── images/
│   │
│   └── templates/
│       ├── base.html           # Template base
        ├── calculadora.html    # Calculadora Agrícola
│       ├── campo_detalhes.html # Detalhes do campo
│       ├── campo_form.html     # Formulário de campo
│       ├── campos.html         # Lista de campos
│       ├── cultura_detalhes.html # Detalhes da cultura
│       ├── cultura_form.html   # Formulário de cultura
│       ├── index.html          # Página inicial
│       ├── culturas.html       # Lista de culturas
│       ├── modo_simplificado.html   # Modo Simplificado - Interface que simula um terminal (não implementado completamente)
│
├── cli/
│   └── cli_app.py              # Interface de linha de comando
│
├── config.py                   # Configurações da aplicação
├── requirements.txt            # Dependências do projeto
├── Dockerfile                  # Configuração para Docker
├── docker-compose.yml          # Configuração para Docker Compose
└── run.py                      # Ponto de entrada da aplicação

```

### 2.2 Componentes Principais

1. **Backend (Flask)**
    - Fornece APIs RESTful para processamento de dados
    - Gerencia a lógica de negócios e cálculos
    - Interage com o banco de dados MongoDB
2. **Frontend (HTML/CSS/JavaScript)**
    - Interface web para interação com o usuário
    - Visualizações gráficas com Plotly
    - Formulários para entrada de dados
3. **Banco de Dados (MongoDB)**
    - Armazena informações sobre culturas agrícolas
    - Armazena informações sobre campos/áreas de plantio
    - Armazena resultados de cálculos para referência futura
4. **CLI (Interface de Linha de Comando)**
    - Fornece acesso às funcionalidades via terminal
    - Alternativa à interface web para operações rápidas

## 3. Modelos de Dados

### 3.1 Cultura

```json

{
  "_id": "unique_id_cultura",
  "nome_cultura": "Mandioca",
  "nome_cientifico": "Manihot esculenta",
  "descricao": "Descrição da cultura",
  "dados_agronomicos": {
    "densidade_plantio": {
      "espacamento_m": {
        "entre_linhas": 1.0,
        "entre_plantas": 1.0
      },
      "plantas_por_hectare": 10000
    },
    "ciclo_producao_dias": {
      "minimo": 240,
      "maximo": 540
    }
  },
  "clima_solo": {
    "temperatura_ideal_c": {
      "minima": 20,
      "maxima": 27
    },
    "precipitacao_minima_mm": 500,
    "precipitacao_maxima_mm": 800,
    "tipo_solo_ideal": "arenoso ou areno-argiloso",
    "ph_ideal": {
      "minimo": 5.5,
      "maximo": 6.5
    },
    "tolerancia_salinidade": "moderada",
    "estrategias_climaticas": [
      "cobertura morta",
      "plantio em camalhões"
    ]
  },
  "fertilizantes_insumos": {
    "adubacao_NPK_por_hectare_kg": {
      "N": 60,
      "P2O5": 40,
      "K2O": 50
    },
    "adubacao_organica_recomendada": "esterco bovino ou composto orgânico",
    "correcao_solo": {
      "calagem": "calcário dolomítico",
      "gessagem": "opcional"
    },
    "frequencia_adubacao": "Plantio e cobertura aos 3-4 meses"
  }
}

```

### 3.2 Campo

```json

{
  "_id": "unique_id_campo",
  "nome_produtor": "Nome do Produtor",
  "localizacao": {
    "municipio": "Município",
    "regiao": "Região"
  },
  "campo": {
    "tipo_geometria": "retangular",
    "comprimento_m": 100,
    "largura_m": 50,
    "area_total_m2": 5000,
    "area_total_hectare": 0.5,
    "cultura_plantada": "Mandioca",
    "data_plantio": "2025-03-01",
    "dados_insumos": {
      "fertilizante_utilizado": "NPK 6-12-12",
      "quantidade_total_kg": 150,
      "quantidade_por_metro_linear_kg": 0.03,
      "irrigacao": {
        "metodo": "aspersão",
        "volume_litros_por_metro": 0.5,
        "quantidade_ruas": 50,
        "quantidade_total_litros": 2500
      }
    }
  }
}

```

## 4. Funcionalidades Principais

### 4.1 Gestão de Culturas

- **Listar Culturas**: Visualização de todas as culturas cadastradas
- **Detalhes da Cultura**: Informações detalhadas sobre uma cultura específica
- **Adicionar Cultura**: Cadastro de novas culturas com informações agronômicas
- **Editar Cultura**: Modificação de dados de culturas existentes
- **Remover Cultura**: Exclusão de culturas do sistema

### 4.2 Gestão de Campos

- **Listar Campos**: Visualização de todos os campos cadastrados
- **Detalhes do Campo**: Informações detalhadas sobre um campo específico
- **Adicionar Campo**: Cadastro de novos campos com geometrias variadas
- **Editar Campo**: Modificação de dados de campos existentes
- **Remover Campo**: Exclusão de campos do sistema

### 4.3 Calculadoras

### 4.3.1 Calculadora de Área

Suporta cálculos para diferentes geometrias:

- **Retangular**: Comprimento × Largura
- **Triangular**: (Base × Altura) / 2
- **Circular**: π × Raio²
- **Trapezoidal**: ((Base Maior + Base Menor) × Altura) / 2

### 4.3.2 Calculadora de Insumos

- Cálculo de fertilizantes NPK com base na cultura e área
- Estimativa de custos de fertilizantes (*valor padrão R$ 5,00/Kg*)
- Visualização da distribuição de nutrientes (N, P, K)

### 4.3.3 Calculadora de Irrigação

- Cálculo do número de linhas/ruas com base no espaçamento da cultura
- Determinação do volume de água necessário por linha
- Cálculo do volume total de irrigação
- Visualização do layout de irrigação

### 4.3.4 Calculadora de Plantio

- Cálculo da quantidade de plantas com base na densidade e área
- Determinação da quantidade de sementes necessárias considerando taxa de germinação
- Visualização do padrão de plantio
- Informações sobre o período recomendado para plantio

### 4.4 Visualizações

- Gráficos de área para diferentes geometrias
- Gráficos de distribuição de NPK
- Visualização de linhas de irrigação
- Padrões de espaçamento para plantio

### 4.5 Modo Terminal

- Interface de linha de comando para acesso às funcionalidades
- Comandos para listar, visualizar e calcular dados
- Exportação de dados para análise em R

## 5. APIs

### 5.1 API de Culturas

- `GET /api/culturas`: Lista todas as culturas
- `GET /api/culturas/<id>`: Obtém detalhes de uma cultura específica
- `POST /api/culturas`: Adiciona uma nova cultura
- `PUT /api/culturas/<id>`: Atualiza uma cultura existente
- `DELETE /api/culturas/<id>`: Remove uma cultura

### 5.2 API de Campos

- `GET /api/campos`: Lista todos os campos
- `GET /api/campos/<id>`: Obtém detalhes de um campo específico
- `POST /api/campos`: Adiciona um novo campo
- `PUT /api/campos/<id>`: Atualiza um campo existente
- `DELETE /api/campos/<id>`: Remove um campo

### 5.3 API de Cálculos

- `POST /api/calculos/area`: Calcula a área com base na geometria
- `POST /api/calculos/insumos`: Calcula insumos com base na cultura e área
- `POST /api/calculos/plantas`: Calcula a quantidade de plantas com base na cultura e área

## 6. Tecnologias Utilizadas

### 6.1 Backend

- **Python**: Linguagem de programação principal
- **Flask**: Framework web para o backend
- **PyMongo**: Interface para MongoDB
- **NumPy**: Processamento numérico para cálculos

### 6.2 Frontend

- **HTML/CSS/JavaScript**: Tecnologias web padrão
- **Bootstrap**: Framework CSS para interface responsiva
- **Plotly**: Biblioteca para visualizações interativas
- **Fetch API**: Para comunicação com o backend

### 6.3 Armazenamento de Dados

- **MongoDB**: Banco de dados NoSQL para armazenamento flexível de documentos

### 6.4 Implantação

- **Docker**: Contêinerização da aplicação
- **Docker Compose**: Orquestração de múltiplos contêineres

## 7. Guia de Implantação

### 7.1 Requisitos

- Docker e Docker Compose
- Acesso à internet para download de dependências

### 7.2 Passos para Implantação

1. Clone o repositório:
    
    ```
    
    git clone https://github.com/thiagoparaizo/FIAP_CAP1_FarmTech_py.git
    cd farmtech-app
    
    ```
    
2. Execute com Docker Compose:
    
    ```
    
    docker-compose up -d
    
    ```
    
3. Acesse a aplicação:
    
    ```
    
    http://localhost:5000
    
    ```
    

### 7.3 Implantação Manual

1. Instale as dependências:
    
    ```
    
    pip install -r requirements.txt
    
    ```
    
2. Configure o MongoDB:
    
    ```
    
    export MONGO_URI="mongodb://localhost:27017/farmtech"
    
    ```
    
3. Execute a aplicação:
    
    ```
    
    python run.py
    
    ```
    

## 8. Guia de Uso

### 8.1 Interface Web

1. **Página Inicial**:
    - Visão geral das culturas e campos cadastrados
    - Acesso rápido às principais funcionalidades
2. **Gerenciamento de Culturas**:
    - Cadastre culturas com informações agronômicas detalhadas
    - Visualize, edite ou remova culturas existentes
3. **Gerenciamento de Campos**:
    - Cadastre campos com diferentes geometrias
    - Associe campos a culturas específicas
    - Visualize cálculos automáticos de área e insumos
4. **Calculadoras**:
    - Utilize as calculadoras específicas para diferentes necessidades
    - Visualize resultados em gráficos interativos
5. Modo Simplificado (Simulação de Terminal no Browser):
    - Utilização de algumas funcioanlidades a partir de um terminal simulado.
    

### 8.2 Modo Terminal

Acesse a aplicação via terminal:

```bash

python cli/cli_app.py

```

Comandos disponíveis:

- `help`: Exibe ajuda sobre comandos disponíveis
- `list culturas`: Lista culturas cadastradas
- `list campos`: Lista campos cadastrados
- `show cultura [id]`: Mostra detalhes de uma cultura
- `show campo [id]`: Mostra detalhes de um campo
- `calc area [tipo] [params]`: Calcula área
- `calc insumos [cultura] [area]`: Calcula insumos
- `exit`: Sai do programa

## 9. Exemplos de Uso

### 9.1 Cálculo de Área para Campo Retangular

1. Acesse a calculadora de área
2. Selecione o tipo "Retangular"
3. Insira o comprimento (ex: 100m)
4. Insira a largura (ex: 50m)
5. Clique em "Calcular Área"
6. Resultado: 5000 m² ou 0,5 hectares

### 9.2 Cálculo de Insumos para Cultura de Mandioca

1. Acesse a calculadora de insumos
2. Selecione a cultura "Mandioca"
3. Insira a área (ex: 0,5 hectares)
4. Clique em "Calcular Insumos"
5. Resultado: Quantidades de N, P, K e total de fertilizantes

### 9.3 Cálculo de Irrigação

1. Acesse a calculadora de irrigação
2. Selecione a cultura
3. Informe as dimensões do campo
4. Informe o volume de água por metro
5. Clique em "Calcular Irrigação"
6. Resultado: Volume total de água necessário

## 10. Resolução de Problemas

### 10.1 Problemas Comuns

1. **Erro ao salvar cultura/campo**:
    - Verifique se todos os campos obrigatórios foram preenchidos
    - Verifique a conexão com o MongoDB
2. **Erro nos cálculos**:
    - Certifique-se de que os valores inseridos são válidos
    - Verifique se o tipo de geometria está correto
3. **Erro na visualização**:
    - Verifique se a biblioteca Plotly está carregada corretamente
    - Verifique se os dados para visualização são válidos

### 10.2 Logs e Diagnóstico

- Verifique os logs do servidor Flask para detalhes sobre erros
- Use o console do navegador para verificar erros de JavaScript
- Em caso de problemas com Docker, verifique os logs dos contêineres

## 11. Integração com R (Análise Estatística)

Exportação de dados para análise em R, quando usado no modo TERMINAL (cli_app.py):

- Culturas: `culturas_export.csv`
- Campos: `campos_export.csv`
- Insumos: `insumos_export.csv`

Estes arquivos podem ser utilizados para análises estatísticas mais avançadas na linguagem R.
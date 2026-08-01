# 🚗 Pipeline de Engenharia de Dados para Análise de Estoque de Veículos

Projeto de Engenharia de Dados desenvolvido em Python para automatizar a coleta, processamento, armazenamento e visualização de dados de anúncios de veículos.

O pipeline segue a arquitetura em camadas **Bronze, Silver e Gold**, armazenando os dados em um Data Warehouse no **Google BigQuery** e disponibilizando indicadores através do **Google Looker Studio**.

---

## 📌 Objetivo

Desenvolver um pipeline completo de dados capaz de:

- Extrair anúncios de veículos automaticamente;
- Armazenar dados brutos e tratados;
- Construir tabelas analíticas;
- Publicar os dados no Google BigQuery;
- Criar dashboards para análise do estoque.

---

## 🏗️ Arquitetura

```
Fonte de Dados
      │
      ▼
Extração (Python)
      │
      ▼
Bronze (JSON)
      │
      ▼
Silver (Parquet)
      │
      ▼
Gold (Parquet)
      │
      ▼
Google BigQuery
      │
      ▼
Google Looker Studio
```

---

## 📂 Estrutura do Projeto

```
src/
│
├── extract/
│   ├── Extração dos dados
│
├── bronze/
│   ├── Armazenamento dos dados brutos
│
├── silver/
│   ├── Limpeza e padronização
│
├── gold/
│   ├── Construção das tabelas analíticas
│
├── load/
│   ├── Carga para Google BigQuery
│
├── config/
│   ├── Configurações e credenciais
│
└── main.py

tests/
├── Testes de conexão com Google BigQuery
├── Testes da camada Silver
├── Testes da camada Gold
└── Testes de limite da API

queries/
└── Verificação das tabelas carregadas
```

---

## 📊 Pipeline

### Bronze

- Dados originais
- Arquivos JSON
- Sem transformações

### Silver

- Limpeza
- Padronização
- Conversão de tipos
- Enriquecimento dos dados

### Gold

- Modelo analítico
- Tabela fato
- Tabelas dimensão
- KPIs

---

## 📋 Tabelas Geradas

### Fato

- fato_veiculos

### KPIs

- kpi_resumo_geral

### Dimensões

- dim_marcas
- dim_regioes
- dim_estados
- dim_categorias
- dim_faixa_preco
- dim_modelos
- dim_combustivel
- dim_transmissao
- dim_faixa_desconto
- dim_categoria_km
- dim_ano_modelo
- dim_lojas
- dim_cor
- dim_marca_categoria

---

## ☁️ Tecnologias Utilizadas

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Google BigQuery
- Google Cloud
- Pandas GBQ
- Google Looker Studio

---

## ▶️ Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env` e as credenciais do Google Cloud.

Execute:

```bash
python main.py
```

---

## 📈 Resultados

O pipeline produz:

- Camada Bronze (JSON)
- Camada Silver (Parquet)
- Camada Gold (Parquet)
- Tabelas no Google BigQuery
- Dashboard interativo no Google Looker Studio

---

## 🚀 Possíveis Evoluções

- Agendamento com Apache Airflow
- Armazenamento em Cloud Storage
- Orquestração em Docker
- Monitoramento do pipeline
- Validação automática da qualidade dos dados
- Atualizações incrementais

---

## 👨‍💻 Autor

**Pablo Brian**

Engenheiro de Computação

Atuação em Engenharia de Software, Engenharia de Dados, Back-end e Cloud.
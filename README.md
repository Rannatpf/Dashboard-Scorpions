# Scorpions Connect - Dashboard de Churn

Aqui está um modelo de **README.md** profissional e estratégico. Ele foi escrito para destacar suas competências como desenvolvedora e sua capacidade de entrega consultiva para a **Scorpions Connect**, servindo tanto para o seu portfólio no GitHub quanto como evidência para o seu **Relatório de Extensão V**.

---

# 🦂 Scorpions Connect: Data Analytics & Retention Dashboard

Este projeto de inteligência de negócios foi desenvolvido como parte da intervenção tecnológica para a empresa **Scorpions Connect**, com foco em análise de engajamento, retenção de clientes (Churn) e validação de personas estratégicas.

A solução integra uma arquitetura moderna de dados, utilizando **Python**, **Streamlit** e **Google Sheets API** para fornecer *insights* em tempo real para as equipes de Sucesso do Cliente e Financeiro.

---

## 🚀 Funcionalidades Principais

* **KPIs de Negócio:** Monitoramento de Receita Mensal Recorrente (MRR), Volume de Acessos e Taxa de Churn Geral.
* **Análise de Persona:** Segmentação automatizada entre "Persona Mãe" (nichos de alto LTV como Farmácia e Proteção Veicular) vs. Personas Negativas.
* **Health Score Pró-ativo:** Identificação automática de clientes ativos com baixo engajamento (menos de 3.000 acessos) para ações de retenção.
* **Geolocalização:** Mapeamento da expansão nacional da base de clientes pós-aquisição Vendaz.
* **Filtros Dinâmicos:** Segmentação por Estado, Status de Contrato e Canal de Aquisição.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.12
* **Dashboard:**[Streamlit](https://streamlit.io/)
* **Manipulação de Dados:** Pandas
* **Visualização:** Plotly Express
* **Banco de Dados:** Google Sheets via `st-gsheets-connection`
* **Deploy:** Streamlit Community Cloud

---

## 🔒 Segurança e LGPD

O projeto adota rigorosos padrões de segurança para proteger os dados sensíveis da Scorpions Connect:

* **Cloud Secrets:** As credenciais e URLs da base de dados não estão expostas no código. Elas são gerenciadas via camadas de segredos criptografados.
* **Zero Local Data:** Não há persistência de arquivos CSV no repositório, eliminando riscos de vazamento de dados de faturamento.
* **Ambientes Isolados:** Uso de ambientes virtuais (`venv`) para garantir a integridade das dependências.

# 🦂Scorpions Connect: Data Analytics & Retention

Projeto de intervenção tecnológica desenvolvido como parte do **Projeto de Extensão V** do curso de Ciência de Dados.

## 🚀 Funcionalidades

- **Dashboard Interativo:** Monitoramento de MRR e Engajamento via Streamlit.
- **Pipeline de ETL:** Limpeza e normalização automática de dados de faturamento.
- **Análise de Risco:** Identificação proativa de Churn baseada em volumetria.

## 🛠️ Como Instalar

1. Certifique-se de ter o Python 3.10+ instalado.
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `.\venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`

## 🧪 Testes e Qualidade

Para garantir a integridade dos cálculos financeiros e das regras de negócio:

- Execute: `pytest`

Este projeto utiliza Python e Streamlit para transformar logs de volumetria
da Scorpions Connect em indicadores de saúde do cliente.

## Como rodar:

1. Instale as dependências: `pip install -r requirements.txt`
2. Execute: `streamlit run app/main.py`

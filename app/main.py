import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuração da Página
st.set_page_config(page_title="Scorpions Connect - Data Analytics", layout="wide", page_icon="🦂")

# 2. Lógica de Caminho Robusta (Resolve o erro de "No such file or directory")
def encontrar_csv():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # Lista de locais possíveis para o arquivo
    tentativas = [
        os.path.join(diretorio_atual, '..', 'data', 'scorpions_analise_cruzada.csv'), # Local (app/../data)
        os.path.join(diretorio_atual, 'data', 'scorpions_analise_cruzada.csv'),      # Nuvem (data/)
        'data/scorpions_analise_cruzada.csv'                                         # Root relativo
    ]
    for caminho in tentativas:
        if os.path.exists(caminho):
            return caminho
    return None

csv_path = encontrar_csv()

@st.cache_data 
def carregar_dados(caminho):
    if not caminho:
        return None
    
    df = pd.read_csv(caminho)
    
    # Validação da coluna 'canal'
    if 'canal' not in df.columns:
        df['canal'] = "Não Informado" 

    # Conversão de tipos de dados (Garante que cálculos funcionem)
    df['total_acessos'] = pd.to_numeric(df['total_acessos'], errors='coerce').fillna(0)
    df['valor_mensal'] = pd.to_numeric(df['valor_mensal'], errors='coerce').fillna(0)
    
    # Criação da coluna Persona (Lógica de Negócio do Projeto)
    if 'persona' not in df.columns:
        df['persona'] = df['nicho'].apply(
            lambda x: 'Persona Mãe' if str(x).lower() in ['farmacia', 'proteção veicular', 'rh', 'academia'] 
            else 'Persona Negativa'
        )
    return df

# 3. Execução do Dashboard
try:
    df = carregar_dados(csv_path)

    if df is None:
        st.error("🚨 Erro Crítico: O arquivo 'scorpions_analise_cruzada.csv' não foi encontrado.")
        st.info("Verifique se a pasta 'data' foi enviada corretamente para o GitHub.")
        st.stop()

    # --- SIDEBAR (FILTROS) ---
    st.sidebar.image("https://scorpionsconnect.com.br/wp-content/uploads/2021/10/logo-scorpions-connect.png", width=200)
    st.sidebar.title("📌 Filtros Estratégicos")
    
    estados = st.sidebar.multiselect("Filtrar por Estado:", options=df['estado'].unique(), default=df['estado'].unique())
    status = st.sidebar.multiselect("Filtrar por Status:", options=df['status'].unique(), default=df['status'].unique())
    canais = st.sidebar.multiselect("Filtrar por Canal:", options=df['canal'].unique(), default=df['canal'].unique())
    
    df_filtrado = df[
        (df['estado'].isin(estados)) & 
        (df['status'].isin(status)) & 
        (df['canal'].isin(canais))
    ]

    # --- CABEÇALHO ---
    st.title("🦂 Scorpions Connect: Inteligência de Dados")
    st.markdown(f"Análise de **{len(df_filtrado)}** clientes ativos e inativos.")

    # --- LINHA 1: KPIs ---
    mrr_ativo = df_filtrado[df_filtrado['status'] == 'ativo']['valor_mensal'].sum()
    acessos_totais = df_filtrado['total_acessos'].sum()
    churn_count = len(df_filtrado[df_filtrado['status'] == 'cancelado'])
    churn_rate = (churn_count / len(df)) * 100 if len(df) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Ativa (MRR)", f"R$ {mrr_ativo:,.2f}")
    col2.metric("Engajamento (Acessos)", f"{acessos_totais:,.0f}")
    col3.metric("Cancelamentos", f"{churn_count}")
    col4.metric("Taxa de Churn Geral", f"{churn_rate:.1f}%")

    st.divider()

    # --- TABS DE NAVEGAÇÃO ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Engajamento", "💰 Financeiro & Canais", "🌍 Geográfico", "💡 Insights & Risco"])

    with tab1:
        st.subheader("Análise de Persona e Comportamento")
        c1, c2 = st.columns(2)
        with c1:
            fig_persona = px.bar(df_filtrado, x='persona', y='total_acessos', color='status', 
                                 title="Volume de Acessos por Tipo de Persona", barmode='group', template="plotly_dark")
            st.plotly_chart(fig_persona, use_container_width=True)
        with c2:
            fig_nicho = px.box(df_filtrado, x='nicho', y='total_acessos', color='status', 
                               title="Dispersão de Uso por Nicho")
            st.plotly_chart(fig_nicho, use_container_width=True)

    with tab2:
        st.subheader("Relação Valor x Uso e Origem")
        c3, c4 = st.columns(2)
        with c3:
            fig_disp = px.scatter(df_filtrado, x='total_acessos', y='valor_mensal', color='status',
                                  size='valor_mensal', hover_name='cliente', title="Eficiência: Valor Mensal vs. Volume")
            st.plotly_chart(fig_disp, use_container_width=True)
        with c4:
            fig_canal = px.histogram(df_filtrado, x='canal', color='status', barmode='group',
                                     title="Sobrevivência por Canal de Aquisição")
            st.plotly_chart(fig_canal, use_container_width=True)

    with tab3:
        st.subheader("Expansão Geográfica da Scorpions")
        df_geo_count = df_filtrado.groupby('estado').size().reset_index(name='qtd')
        fig_geo = px.bar(df_geo_count, x='estado', y='qtd', color='estado', text_auto=True, title="Nacionalização da Base")
        st.plotly_chart(fig_geo, use_container_width=True)

    with tab4:
        st.header("🧠 Centro de Insights")
        risco = df_filtrado[(df_filtrado['status'] == 'ativo') & (df_filtrado['total_acessos'] < 3000)]
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.info("**Insight Comercial:** Nichos de 'Farmácia' e 'Proteção Veicular' apresentam LTV superior devido à dependência tecnológica.")
            st.success("**Recomendação:** Intensificar prospecção ativa no LinkedIn para os estados de SP e SC.")
        with col_in2:
            st.warning(f"**Alerta de Suporte:** {len(risco)} clientes ativos estão com baixo uso.")
            st.error("**Risco Financeiro:** Clientes com ticket acima de R$ 300 mas baixo uso devem ser priorizados.")

        st.divider()
        st.subheader("🚨 Tabela de Ação Pró-Ativa (Baixo Health Score)")
        st.dataframe(risco[['cliente', 'nicho', 'total_acessos', 'valor_mensal', 'canal']].sort_values(by='total_acessos'), use_container_width=True)

except Exception as e:
    st.error(f"Erro inesperado: {e}")
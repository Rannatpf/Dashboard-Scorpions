import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection


st.set_page_config(
    page_title="Scorpions Connect - Data Analytics", 
    layout="wide", 
    page_icon="🦂"
)

@st.cache_data(ttl=600)
def carregar_dados():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        
        if 'canal' not in df.columns:
            df['canal'] = "Não Informado" 

        df['total_acessos'] = pd.to_numeric(df['total_acessos'], errors='coerce').fillna(0)
        df['valor_mensal'] = pd.to_numeric(df['valor_mensal'], errors='coerce').fillna(0)
        
        if 'persona' not in df.columns:
            df['persona'] = df['nicho'].apply(
                lambda x: 'Persona Mãe' if str(x).lower() in ['farmacia', 'proteção veicular', 'rh', 'academia'] 
                else 'Persona Negativa'
            )
            
        df['status_risco'] = df['total_acessos'].apply(
            lambda x: 'Crítico' if x < 3000 else ('Atenção' if x < 5000 else 'Saudável')
        )
        
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a base de dados: {e}")
        return None

df = carregar_dados()

if df is not None:
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

    st.title("🦂 Scorpions Connect: Inteligência de Dados")
    st.markdown(f"Análise de engajamento e retenção de **{len(df_filtrado)}** clientes cadastrados.")

    mrr_ativo = df_filtrado[df_filtrado['status'] == 'ativo']['valor_mensal'].sum()
    acessos_totais = df_filtrado['total_acessos'].sum()
    churn_total = len(df_filtrado[df_filtrado['status'] == 'cancelado'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Ativa (MRR)", f"R$ {mrr_ativo:,.2f}")
    col2.metric("Engajamento Total", f"{acessos_totais:,.0f} acessos")
    col3.metric("Cancelamentos", f"{churn_total}")
    col4.metric("Taxa de Churn", f"{(churn_total/len(df)*100):.1f}%")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Engajamento", "💰 Financeiro & Canais", "🌍 Geográfico", "💡 Insights & Risco"])

    with tab1:
        st.subheader("Comportamento por Persona e Nicho")
        c1, c2 = st.columns(2)
        with c1:
            fig_persona = px.bar(df_filtrado, x='persona', y='total_acessos', color='status', 
                                 barmode='group', template="plotly_dark")
            st.plotly_chart(fig_persona, use_container_width=True)
        with c2:
            fig_nicho = px.box(df_filtrado, x='nicho', y='total_acessos', color='status')
            st.plotly_chart(fig_nicho, use_container_width=True)

    with tab2:
        st.subheader("Análise de Eficiência Comercial")
        c3, c4 = st.columns(2)
        with c3:
            fig_disp = px.scatter(df_filtrado, x='total_acessos', y='valor_mensal', color='status',
                                  size='valor_mensal', hover_name='cliente')
            st.plotly_chart(fig_disp, use_container_width=True)
        with c4:
            fig_canal = px.histogram(df_filtrado, x='canal', color='status', barmode='group')
            st.plotly_chart(fig_canal, use_container_width=True)

    with tab3:
        st.subheader("Expansão Geográfica")
        df_geo = df_filtrado.groupby('estado').size().reset_index(name='qtd')
        fig_geo = px.bar(df_geo, x='estado', y='qtd', color='estado', text_auto=True)
        st.plotly_chart(fig_geo, use_container_width=True)

    with tab4:
        st.header("🧠 Centro de Monitoramento Pró-Ativo")
        risco = df_filtrado[(df_filtrado['status'] == 'ativo') & (df_filtrado['total_acessos'] < 3000)]
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.info("**Insight Comercial:** Nichos mapeados na Persona Mãe mostram engajamento superior.")
        with col_in2:
            st.warning(f"**Alerta de Churn:** {len(risco)} clientes ativos exigem contato imediato.")

        st.divider()
        st.subheader("🚨 Tabela de Ação para Suporte")
        st.dataframe(risco[['cliente', 'nicho', 'total_acessos', 'valor_mensal', 'canal']].sort_values(by='total_acessos'), use_container_width=True)

else:
    st.warning("Verifique a configuração nos Secrets do Streamlit.")
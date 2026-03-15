import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. Configurações de Interface (Limpa e Profissional)
st.set_page_config(
    page_title="Scorpions Connect - Intelligence Hub", 
    layout="wide",
    page_icon="📊"
)

# Custom CSS para métricas com visual moderno (estilo Dashboard Corporativo)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def carregar_e_tratar_dados():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        
        # --- ENGENHARIA DE DADOS DINÂMICA ---
        # Detecta colunas que são meses (ex: JAN, jan./2025, jan. 2026)
        # Procuramos por '/' ou palavras que lembrem meses para somar a série temporal toda
        cols_temporais = [c for c in df.columns if '/' in str(c) or '202' in str(c)]
        
        # Converte colunas financeiras e temporais para numérico
        cols_numericas = cols_temporais + ['valor_mensal', 'total_mensagens']
        for col in cols_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Recalcula o total de mensagens somando todas as colunas de meses detectadas
        if cols_temporais:
            df['total_mensagens'] = df[cols_temporais].sum(axis=1)

        # Trata coluna de Canal e Persona
        df['canal'] = df.get('canal', "Não Informado").fillna("Não Informado")
        
        if 'persona' not in df.columns:
            df['persona'] = df['nicho'].apply(
                lambda x: 'Persona Mãe (Ideal)' if str(x).lower() in ['farmacia', 'proteção veicular', 'rh', 'academia'] 
                else 'Persona Negativa'
            )
        
        # Lógica de Health Score (Status de Risco)
        df['status_risco'] = df.apply(
            lambda x: 'Crítico' if x['total_mensagens'] < 3000 and x['status'] == 'ativo' 
            else ('Cancelado' if x['status'] == 'cancelado' else 'Saudável'), axis=1
        )
        
        return df, cols_temporais
    except Exception as e:
        st.error(f"Erro na conexão com a base de dados: {e}")
        return None, []

# Execução da carga de dados
df, cols_temporais = carregar_e_tratar_dados()

if df is not None:
    # --- SIDEBAR (Painel de Filtros) ---
    st.sidebar.image("https://scorpionsconnect.com.br/wp-content/uploads/2021/10/logo-scorpions-connect.png", width=180)
    st.sidebar.header("Painel de Controle")
    
    with st.sidebar.expander("Filtros Estratégicos", expanded=True):
        estados = st.multiselect("Estados:", sorted(df['estado'].unique()), default=df['estado'].unique())
        status = st.multiselect("Status Contratual:", df['status'].unique(), default=df['status'].unique())
        persona = st.multiselect("Persona:", df['persona'].unique(), default=df['persona'].unique())

    df_filtrado = df[
        (df['estado'].isin(estados)) & 
        (df['status'].isin(status)) & 
        (df['persona'].isin(persona))
    ]

    # --- CABEÇALHO E MÉTRICAS ---
    st.title("Scorpions Connect: Inteligência de Dados")
    st.markdown(f"Monitoramento estratégico de **{len(df_filtrado)}** contas (Jan/25 - Jan/26).")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Receita (MRR) Ativa", f"R$ {df_filtrado[df_filtrado['status']=='ativo']['valor_mensal'].sum():,.2f}")
    m2.metric("Volumetria Mensagens", f"{df_filtrado['total_mensagens'].sum():,.0f}")
    
    total_clientes = len(df)
    churn_rate = (len(df[df['status']=='cancelado']) / total_clientes * 100) if total_clientes > 0 else 0
    m3.metric("Churn Rate Global", f"{churn_rate:.1f}%")
    
    criticos = len(df_filtrado[df_filtrado['status_risco']=='Crítico'])
    m4.metric("Alertas de Risco", criticos)

    st.divider()

    # --- NAVEGAÇÃO POR ABAS ---
    tab_eng, tab_fin, tab_temp, tab_risco = st.tabs([
        "Perfil de Engajamento", "Financeiro e Canais", "Tendência Temporal", "Gestão de Risco"
    ])

    with tab_eng:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Engajamento por Persona")
            fig = px.bar(df_filtrado, x='persona', y='total_mensagens', color='status', 
                         barmode='group', template="plotly_dark",
                         color_discrete_map={'ativo': '#00CC96', 'cancelado': '#EF553B'})
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Distribuição por Nicho")
            fig_nicho = px.box(df_filtrado, x='nicho', y='total_mensagens', color='persona')
            st.plotly_chart(fig_nicho, use_container_width=True)

    with tab_fin:
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Performance por Canal de Venda")
            fig_pie = px.pie(df_filtrado, names='canal', values='valor_mensal', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        with c4:
            st.subheader("Correlação: Investimento vs Uso")
            fig_scat = px.scatter(df_filtrado, x='total_mensagens', y='valor_mensal', 
                                 size='total_mensagens', color='status', hover_name='cliente')
            st.plotly_chart(fig_scat, use_container_width=True)

    with tab_temp:
        st.subheader("Evolução Mensal de Acessos")
        if cols_temporais:
            # Transformação de dados para formato 'long' para plotar linha temporal
            df_temp = df_filtrado.melt(id_vars=['cliente', 'status'], value_vars=cols_temporais, 
                                      var_name='Mês', value_name='Mensagens')
            df_media_mensal = df_temp.groupby(['Mês', 'status'])['Mensagens'].mean().reset_index()
            # Ordenação lógica dos meses baseada na planilha
            df_media_mensal['Mês'] = pd.Categorical(df_media_mensal['Mês'], categories=cols_temporais, ordered=True)
            fig_line = px.line(df_media_mensal.sort_values('Mês'), x='Mês', y='Mensagens', 
                               color='status', markers=True, template="plotly_dark")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Colunas de série temporal não encontradas na base.")

    with tab_risco:
        st.subheader("Centro de Monitoramento Pró-Ativo")
        risco_df = df_filtrado[df_filtrado['status_risco'] == 'Crítico'].sort_values('total_mensagens')
        
        st.error(f"Identificados {len(risco_df)} clientes ativos abaixo da meta de engajamento (3.000 msgs).")
        st.dataframe(risco_df[['cliente', 'nicho', 'canal', 'total_mensagens', 'valor_mensal']], 
                     use_container_width=True)

else:
    st.warning("Verifique a configuração nos Secrets do Streamlit (URL da planilha).")
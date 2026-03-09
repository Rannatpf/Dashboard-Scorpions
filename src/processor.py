import pandas as pd

def limpar_dados_scorpions(caminho_csv):
    df = pd.read_csv(caminho_csv)

    if df['valor_mensal'].dtype == 'O': 
        df['valor_mensal'] = (
            df['valor_mensal']
            .str.replace('R$', '', regex=False)
            .str.replace('.', '', regex=False) 
            .str.replace(',', '.', regex=False) 
            .str.strip()
            .astype(float)
        )
    
    # Lógica de Risco (Health Score)
    df['status_risco'] = df['total_acessos'].apply(
        lambda x: 'Crítico' if x < 3000 else ('Atenção' if x < 5000 else 'Saudável')
    )
    
    return df
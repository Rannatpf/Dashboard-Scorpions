import pandas as pd
from src.processor import limpar_dados_scorpions

def test_conversao_financeira():
    data = {'cliente': ['Teste'], 'valor_mensal': ['R$ 100,00'], 'total_acessos': [5000], 'nicho': ['RH']}
    df_teste = pd.DataFrame(data)
    df_teste.to_csv('data/temp_test.csv', index=False)
    
    df_result = limpar_dados_scorpions('data/temp_test.csv')
    assert df_result['valor_mensal'].iloc[0] == 100.0
    assert isinstance(df_result['valor_mensal'].iloc[0], float)

def test_classificacao_risco():
    data = {'cliente': ['Risco'], 'valor_mensal': [100.0], 'total_acessos': [500], 'nicho': ['Floricultura']}
    df_teste = pd.DataFrame(data)
    df_teste.to_csv('data/temp_test.csv', index=False)
    
    df_result = limpar_dados_scorpions('data/temp_test.csv')
    assert df_result['status_risco'].iloc[0] == 'Crítico'
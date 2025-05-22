
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from requests.exceptions import HTTPError

# Configurações
token = "eyJhbGciOiJIUzI1NiIsInR5cGVbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTA2NTE5LCJpYXQiOjE3NDc5MTQ0OTMsImp0aSI6ImI4ZmMyM2ExNWY5YjRkMzQ4YmM2YjVlNDg2Y2M3NjlmIiwidXNlcl9pZCI6NjV9.5stcchj5veUJ_7_2ioIPuYlOleUfYLKphYKGk8h3KzE"
headers = {"Authorization": f"JWT {token}"}
url = "https://laboratoriodefinancas.com/api/v1/balanco"

# Pasta de saída
output_dir = Path.home() / 'Desktop'
output_file = output_dir / f"comparativo_indicadores_{datetime.now():%Y%m%d_%H%M}.xlsx"

# Empresas e período
tickers = ["JBSS3", "MRFG3", "BRFS3", "BEEF3"]
periodo = "20244T"

def fetch_balanco(ticker, ano_tri):
    """Tenta buscar o balanço; retorna DataFrame ou None se não autorizado ou sem dados."""
    try:
        resp = requests.get(url, headers=headers, params={"ticker": ticker, "ano_tri": ano_tri})
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            print(f"⚠️ Não autorizado para {ticker}.")
            return None
        else:
            raise
    dados = resp.json().get("dados", [])
    if not dados:
        print(f"⚠️ Sem dados para {ticker} no período {ano_tri}.")
        return None
    return pd.DataFrame(dados[0]["balanco"])

def get_valor(df, *chaves):
    for chave in chaves:
        mask = df['descricao'].str.contains(chave, case=False, na=False)
        if mask.any():
            return df.loc[mask, 'valor'].iloc[0]
    return np.nan

def safe_ratio(num, den, dias=False):
    if pd.isna(num) or pd.isna(den) or den == 0:
        return np.nan
    r = num / den
    return r * 360 if dias else r

def calcula_indicadores(df):
    # Extrai contas necessárias
    AC = get_valor(df, "Ativo Circulante")
    PC = get_valor(df, "Passivo Circulante")
    Estoque = get_valor(df, "Estoque", "Estoques")
    DA = get_valor(df, "Despesas Antecipadas")
    Disponivel = get_valor(df, "Disponibilidades", "Caixa")
    Aplic = get_valor(df, "Aplicações")
    ARLP = get_valor(df, "Ativo Realizável a Longo Prazo")
    PNC = get_valor(df, "Passivo Não Circulante")
    Clientes = get_valor(df, "Clientes", "Contas a receber")
    Fornecedores = get_valor(df, "Fornecedores")
    Receita = get_valor(df, "Receita Líquida", "Receita")
    CMV = get_valor(df, "Custo das Mercadorias Vendidas", "CMV")
    Compras = get_valor(df, "Compras")
    Emprest = get_valor(df, "Empréstimos", "Financiamentos")
    AT = get_valor(df, "Ativo Total")
    PT = get_valor(df, "Passivo Total")
    PL = get_valor(df, "Patrimônio Líquido")
    DF = get_valor(df, "Despesa Financeira Líquida", "Despesas Financeiras")
    BT = get_valor(df, "Benefício Tributário da Dívida", "BT Dívida")
    IR = get_valor(df, "IR Corrente")
    LAIR = get_valor(df, "LAIR")  # Lucro antes IR/CSLL

    # Liquidez, ciclos e capital de giro (não usados na seleção final, mas mantidos para referência)
    # ...

    # Cálculo de WACC simplificado
    Ki = safe_ratio(DF, PC + (PC - Emprest))
    DFL = DF - BT
    Alq_IR_CSLL = safe_ratio(IR, LAIR)
    Wi = safe_ratio(PT, PT + PL)
    We = 1 - (Wi if not pd.isna(Wi) else 0)
    CMPC = Wi * Ki + We * Alq_IR_CSLL

    # EBITDA, NOPAT, ROE e EVA
    EBITDA = safe_ratio(get_valor(df, "Margem EBITDA") * Receita, 1)
    Dep = get_valor(df, "Depreciação", "Amortização")
    EBIT = EBITDA - Dep
    NOPAT = EBIT - IR

    ROE = safe_ratio(get_valor(df, "Lucro Líquido"), PL)
    EVA = NOPAT - (CMPC * AT)

    return {'Ticker': None, 'ROE': ROE, 'EVA': EVA}

# Processamento principal
resultados = []
for tk in tickers:
    bal = fetch_balanco(tk, periodo)
    if bal is None:
        continue
    ind = calcula_indicadores(bal)
    ind['Ticker'] = tk
    resultados.append(ind)

df_res = pd.DataFrame(resultados)

# Exporta para Excel
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df_res.to_excel(writer, sheet_name='Indicadores', index=False)
    wb = writer.book
    ws = writer.sheets['Indicadores']
    header_fmt = wb.add_format({'bold': True, 'bg_color': '#DCE6F1', 'border': 1})
    for col_num, col in enumerate(df_res.columns):
        ws.write(0, col_num, col, header_fmt)
        ws.set_column(col_num, col_num, 15)

print(f"Comparativo salvo em: {output_file}")

# Seleção do melhor: primeiro tenta pelo maior EVA, com fallback para ROE
best = None
df_eva = df_res.dropna(subset=['EVA'])
if not df_eva.empty:
    best = df_eva.loc[df_eva['EVA'].idxmax()]
    crit = 'EVA'
elif 'ROE' in df_res.columns:
    df_roe = df_res.dropna(subset=['ROE'])
    if not df_roe.empty:
        best = df_roe.loc[df_roe['ROE'].idxmax()]
        crit = 'ROE'

if best is None:
    print("# Não foi possível determinar a melhor empresa (sem EVA ou ROE válidos).")
else:
    ticker_best = best['Ticker']
    val_best = best[crit]
    # comentando com jogo da velha
    print(f"# A melhor empresa segundo {crit} é {ticker_best} com {crit} = {val_best:.2f}")


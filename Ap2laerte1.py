import requests
import pandas as pd
import numpy as np

# Caminho de saída do Excel
output_path = r"C:\Users\21701079836\Documents\AnaliseDados\vulc.xlsx"

# Token de acesso
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEyODc0LCJpYXQiOjE3NDUzMjA4NzQsImp0aSI6ImQxM2MxOWNlMDA3YzRjMTRiZDRmYjkxZGE2MGQ4N2RmIiwidXNlcl9pZCI6NjV9.1C50rycumEgTVv3eTK6qUj99vUqvxvtZVyO-wLPOVoc"

# Cabeçalhos da requisição
headers = {
    "Authorization": f"JWT {token}"
}

# Parâmetros da requisição
params = {
    "ticker": "MRFG3",
    "ano_tri": "20244t"
}

# URL da API
url = "https://laboratoriodefinancas.com/api/v1/balanco"

# Requisição
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

# Extração dos dados
dados = response.json().get("dados", [])
if not dados:
    raise ValueError("Nenhum dado retornado pela API.")

balanco = dados[0].get("balanco", [])
df_2024 = pd.DataFrame(balanco)

# Salvando em Excel
df_2024.to_excel(output_path, index=False)
print(f"Dados salvos em: {output_path}")

# Função para extrair valor de uma conta específica
def get_valor(descricao):
    resultado = df_2024[df_2024['descricao'].str.contains(descricao, case=False, na=False)]
    if not resultado.empty:
        return resultado['valor'].values[0]
    else:
        return np.nan

# Extraindo os valores necessários
AC = get_valor("Ativo Circulante")
PC = get_valor("Passivo Circulante")
Estoque = get_valor("Estoques")
Despesas_Antecipadas = get_valor("Despesas Antecipadas")
Disponivel = get_valor("Disponível")
ARLP = get_valor("Ativo Realizável a Longo Prazo")
PNC = get_valor("Passivo Não Circulante")
Clientes = get_valor("Clientes")
Fornecedores = get_valor("Fornecedores")
Receita = get_valor("Receita de Vendas")
CMV = get_valor("Custo das Mercadorias Vendidas")
Compras = get_valor("Compras")
Caixa = get_valor("Caixa")
Aplicacoes = get_valor("Aplicações Financeiras")
Emprestimos = get_valor("Empréstimos e Financiamentos")
Ativo_Total = get_valor("Ativo Total")
Passivo_Total = get_valor("Passivo Total")
PL = get_valor("Patrimônio Líquido")
Ativo_Permanente = get_valor("Ativo Permanente")

# Indicadores financeiros
CCL = AC - PC
LC = AC / PC if PC else np.nan
LS = (AC - Estoque - Despesas_Antecipadas) / PC if PC else np.nan
LI = (Disponivel + Aplicacoes) / PC if PC else np.nan
GS = ARLP / PNC if PNC else np.nan
PMR = (Clientes / Receita) * 360 if Receita else np.nan
PMP = (Fornecedores / Compras) * 360 if Compras else np.nan
CME = (Estoque / CMV) * 360 if CMV else np.nan
Ciclo_Financeiro = PMR + CME - PMP
IL = (Caixa + Aplicacoes) / Emprestimos if Emprestimos else np.nan
Endividamento = Passivo_Total / Ativo_Total if Ativo_Total else np.nan
Comp_Endividamento = PNC / PL if PL else np.nan
Imob_do_PL = Ativo_Permanente / PL if PL else np.nan
# GE - Giro do Estoque
GE = 360 / CME if CME else np.nan

# CO - Ciclo Operacional
CO = CME + PMR if CME and PMR else np.nan

# CF - Ciclo Financeiro
CF = CO - PMP if CO and PMP else np.nan

# CE - Capital de Giro Efetivo
CE = CME

# ACO - Ativo Circulante Operacional
ACO = AC - Caixa - Aplicacoes

# PCO - Passivo Circulante Operacional
PCO = PC - Emprestimos

# NCG - Necessidade de Capital de Giro
NCG = ACO - PCO

# ACF - Ativo Circulante Financeiro
ACF = Caixa + Aplicacoes

# PCF - Passivo Circulante Financeiro
PCF = Emprestimos

# ST - Saldo de Tesouraria
ST = ACF - PCF

# CDG - Capital de Giro
CDG = NCG - PC

# Relação Capitais
Relacao_Capitais = Passivo_Total / PL if PL else np.nan

# Endividamento Geral
Endividamento_Geral = Passivo_Total / (Passivo_Total + PL) if (Passivo_Total + PL) else np.nan

# Solvência
Solvencia = Ativo_Total / Passivo_Total if Passivo_Total else np.nan

# Composição do Endividamento
Composicao_Endividamento = PC / Passivo_Total if Passivo_Total else np.nan


# Exibindo os resultados
print("\nIndicadores Financeiros:")
print(f"Capital Circulante Líquido (CCL): {CCL:,.2f}")
print(f"Liquidez Corrente (LC): {LC:.2f}")
print(f"Liquidez Seca (LS): {LS:.2f}")
print(f"Liquidez Imediata (LI): {LI:.2f}")
print(f"Garantia do Passivo Não Circulante (GS): {GS:.2f}")
print(f"Prazo Médio de Recebimento (PMR): {PMR:.2f} dias")
print(f"Prazo Médio de Pagamento (PMP): {PMP:.2f} dias")
print(f"Ciclo Médio de Estocagem (CME): {CME:.2f} dias")
print(f"Ciclo Financeiro: {Ciclo_Financeiro:.2f} dias")
print(f"Índice de Liquidez (IL): {IL:.2f}")
print(f"Endividamento Total: {Endividamento:.2%}")
print(f"Composição do Endividamento: {Comp_Endividamento:.2f}")
print(f"Imobilização do Patrimônio Líquido: {Imob_do_PL:.2f}")
print("\nIndicadores Financeiros:")
print(f"Capital Circulante Líquido (CCL): {CCL:,.2f}")
print(f"Liquidez Corrente (LC): {LC:.2f}")
print(f"Liquidez Seca (LS): {LS:.2f}")
print(f"Liquidez Imediata (LI): {LI:.2f}")
print(f"Garantia do Passivo Não Circulante (GS): {GS:.2f}")
print(f"Prazo Médio de Recebimento (PMR): {PMR:.2f} dias")
print(f"Prazo Médio de Pagamento (PMP): {PMP:.2f} dias")
print(f"Ciclo Médio de Estocagem (CME): {CME:.2f} dias")
print(f"Giro do Estoque (GE): {GE:.2f}")
print(f"Ciclo Operacional (CO): {CO:.2f} dias")
print(f"Ciclo Financeiro: {Ciclo_Financeiro:.2f} dias")
print(f"Capital de Giro Efetivo (CE): {CE:.2f} dias")
print(f"Índice de Liquidez (IL): {IL:.2f}")
print(f"Endividamento Total: {Endividamento:.2%}")
print(f"Composição do Endividamento: {Comp_Endividamento:.2f}")
print(f"Imobilização do Patrimônio Líquido: {Imob_do_PL:.2f}")
print(f"Ativo Circulante Operacional (ACO): {ACO:.2f}")
print(f"Passivo Circulante Operacional (PCO): {PCO:.2f}")
print(f"Necessidade de Capital de Giro (NCG): {NCG:.2f}")
print(f"Ativo Circulante Financeiro (ACF): {ACF:.2f}")
print(f"Passivo Circulante Financeiro (PCF): {PCF:.2f}")
print(f"Saldo de Tesouraria (ST): {ST:.2f}")
print(f"Capital de Giro (CDG): {CDG:.2f}")
print(f"Relação de Capitais: {Relacao_Capitais:.2f}")
print(f"Endividamento Geral: {Endividamento_Geral:.2%}")
print(f"Solvência: {Solvencia:.2f}")

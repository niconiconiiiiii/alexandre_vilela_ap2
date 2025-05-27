import pandas as pd

#Função achar valor
def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = (df[filtro_conta & filtro_descricao]['valor'].values[0])
    return valor

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = (df[filtro_conta & filtro_descricao]['valor'].values[1])
    return valor

import pandas as pd

# Update the file path to macOS format and use the correct ticker file name
arquivo = '/Users/alexandrelopes/Documents/analise_de_dados/alexandre_e_villela_ap2/dados/mrfg33.xlsx'

# Read the Excel file
df = pd.read_excel(arquivo)

# Function to extract values from the DataFrame (assuming `valor_contabil` is defined elsewhere)
def valor_contabil(df, regex_code, regex_desc):
    # Placeholder for the actual implementation of valor_contabil
    # This function should filter the DataFrame based on regex_code and regex_desc
    pass

# AC and PC
Ativo_C_24 = valor_contabil(df, '^1.0', '^ativo cir')
Passivo_C_24 = valor_contabil(df, '^2.0', '^passivo cir')


#Indices de Liquidez:

#Liquidez Corrente(LS)
L_Corrente_24 = Ativo_C_24/Passivo_C_24
#Liquidez Seca(LS)
Estoque_24 = valor_contabil(df, '^1.0', '^estoque')
Despesa_Antecipada_24 = valor_contabil(df, '^1.0', '^despesa')
L_Seca_24 = (Ativo_C_24-Estoque_24-Despesa_Antecipada_24)/Passivo_C_24
#Liquidez Imediata(LI)
Caixa_24 = valor_contabil(df, '^1.0', '^caixa')
Aplicacao_F_24 = valor_contabil(df, '^1.0', '^aplica')
Disponivel_24 = Caixa_24+Aplicacao_F_24
L_Imediata_24 = Disponivel_24/Passivo_C_24
#Liquidez Geral(LG)
Ativo_RNC_24 = valor_contabil(df, '^1.0*', '^ativo realiz')
Passivo_NC_24 = valor_contabil(df, '^2.0*', '^passivo n.o cir')
L_Geral_24 = (Ativo_C_24+Ativo_RNC_24)/(Passivo_C_24+Passivo_NC_24)


#Capital de Giro e Tesouraria:

#ACF
Imposto_de_renda_AC_24 = valor_contabil(df, '^1.0', '^imposto de renda')
Disponivel_24 = Caixa_24+Aplicacao_F_24
Ativo_CF_24 = Disponivel_24+Imposto_de_renda_AC_24
#ACO
Ativo_CO_24 = Ativo_C_24-Ativo_CF_24
#PCF
Emprestimos_24 = valor_contabil(df, '^2.0', '^empr.stimo')
Provisoes_24 = valor_contabil(df, '^2.0', '^provis.es')
Imposto_de_renda_PC_24 = valor_contabil(df, '^2.0', '^imposto de renda')
Dividendos_24 = valor_contabil_2(df, '^2.0', '^dividendos')
Passivo_CF_24 = (Emprestimos_24+Provisoes_24+Imposto_de_renda_PC_24+Dividendos_24)
#PCO
Passivo_CO_24 = (Passivo_C_24-Passivo_CF_24)
#Capital de Giro(CDG)
Capital_de_Giro_24 = Ativo_C_24 - Passivo_C_24
#Necessidade de Capital de Giro(NCG)
Necessidade_de_CG_24 = Ativo_CO_24-Passivo_CO_24
#ST
Saldo_Tesouraria_24 = Ativo_CF_24-Passivo_CF_24



#Indices de Endividamento:

#RELACAO CT/CP = PASSIVO/PL
Patrimonio_L_24 = valor_contabil(df,'^2.*','patrim.nio')
CtCp_24 = (Passivo_C_24+Passivo_NC_24)/Patrimonio_L_24
#ENDIVIDAMENTO GERAL = PASSIVO/PASSIVO+PL
Endividamento_geral_24 = (Passivo_C_24+Passivo_NC_24)/(Passivo_C_24+Passivo_NC_24+Patrimonio_L_24)
#SOLVENCIA = ATIVO TOTAL/PASSIVO
Ativo_T_24 = valor_contabil(df,'^1.*','ativo total')
Solvencia_24 = Ativo_T_24/(Passivo_C_24+Passivo_NC_24)
#CE(Composição do endividamento) = PC/PASSIVO
Composicao_E_24 = Passivo_C_24/(Passivo_C_24+Passivo_NC_24)

#Em relação aos juros e empréstimos
#Passivo oneroso(deve juros)
POn_24 = (valor_contabil(df, '^2.01', '^empr.stimo'))+(valor_contabil(df, '^2.02', '^empr.stimo'))+(valor_contabil(df, '^2.01', '^deb.ntures'))+(valor_contabil(df, '^2.02', '^deb.ntures'))
#Passivo funcionamento
PFun_24 = (Passivo_C_24+Passivo_NC_24)-POn_24
#Divida liquida(Quanto da divida de emprestimos posso pagar com o caixa)
Divida_liquida_24 = POn_24 - Disponivel_24
#Investimento
Investimento_24 = POn_24 + Patrimonio_L_24
#Capital Oneroso
Capital_Oneroso_24 = Divida_liquida_24+Patrimonio_L_24
#Indice divida liquida/PL
Indice_DLPL_24 = Divida_liquida_24/Patrimonio_L_24
#Indice divida liquida/Capital Oneroso
Indice_DLCO_24 = Divida_liquida_24/Capital_Oneroso_24

#Custo médio ponderado de capital(CMPC)= Wi*Ki+We*Ke
   #Wi(Peso dos fiannciamentos) e We(Peso do capital social)
Wi_24 = POn_24/Investimento_24
We_24 = Patrimonio_L_24/Investimento_24
   #Ki(Desp.Fin.Liq/POn):
      #Alíquota
IR_Corrente_24 = (valor_contabil(df, '^3.0', '^imposto de renda'))*(-1)
Lair_24 = valor_contabil_2(df, '^3.0', 'antes')
Aliquota_24 = IR_Corrente_24/Lair_24
      #Benefício tributário
Despesa_Financeira_24 =  (valor_contabil(df,'^3.*','^despesas financeiras'))*(-1)
Benefício_Tributário_24 = Despesa_Financeira_24*Aliquota_24
      #Despesa financeira líquida
DF_Liquida_24 = Despesa_Financeira_24 - Benefício_Tributário_24
      #Ki(quanto que foi pago em relacao a divida total(em %))
Ki_24 = DF_Liquida_24/POn_24
      #Ke(valor fixo)
Ke_24 = 0,12
      #CMPC
Custo_MPC_24 = (Wi_24*Ki_24)+(We_24*Ke_24)



#Indice de PL = 3Is/PL
investimentos_24 = valor_contabil(df,'^1.*','^invest')
imobilizado_24 = valor_contabil(df,'^1.*','^imobilizado$')
intangivel_24 = valor_contabil(df,'^1.*','^intang*')
Patrimonio_L_24 = valor_contabil(df,'^2.*','patrim.nio')
Indice_PL_24 = (investimentos_24+intangivel_24+imobilizado_24)/Patrimonio_L_24





#2023 4T
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEyOTAwLCJpYXQiOjE3NDUzMjA5MDAsImp0aSI6IjQ1MWIyZWM5YTAxMTQ4YjRiZDYxZDQ4MGI0YmM1OWU1IiwidXNlcl9pZCI6NjB9.kssQqfnXMDQxA_gny7-6Hfoaj5DGhfFjYAh_CwC6Yp8"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'ticker': 'MRFG3',
'ano_tri': '20244T',
}

r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
r.json().keys()
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_23 = pd.DataFrame(balanco)

import pandas as pd
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEyOTAwLCJpYXQiOjE3NDUzMjA5MDAsImp0aSI6IjQ1MWIyZWM5YTAxMTQ4YjRiZDYxZDQ4MGI0YmM1OWU1IiwidXNlcl9pZCI6NjB9.kssQqfnXMDQxA_gny7-6Hfoaj5DGhfFjYAh_CwC6Yp8"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'ticker': '',
'data_ini': '2024-04-01',
'data_fim': '2025-03-31'
}

r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
r.json().keys()
dados = r.json()['dados']
df = pd.DataFrame(dados)

preco_ini = df.iloc[0]['fechamento']
preco_fim = df.iloc[-1]['fechamento']
lucro = preco_fim/preco_ini

print("Preço inicial:", preco_ini)
print("Preço final:", preco_fim)
print("Lucro (fator):", lucro) 
#pesquisar
df_23[df_23['descricao'].str.contains('fechamento', case=False)][['conta','descricao','valor']]
#pesquisar
df_23[df['descricao'].str.contains('l.quido', case=False)][['conta','descricao','valor']]

Ebit = valor_contabil(df, '^3.', 'imposto de renda')

#AC e PC
Ativo_C_23 = valor_contabil(df_23, '^1.0', '^ativo cir')
Passivo_C_23 = valor_contabil(df_23, '^2.0', '^passivo cir')


#Indices de Liquidez:

#Liquidez Corrente(LS)
L_Corrente_23 = Ativo_C_23/Passivo_C_23
#Liquidez Seca(LS)
Estoque_23 = valor_contabil(df_23, '^1.0', '^estoque')
Despesa_Antecipada_23 = valor_contabil(df_23, '^1.0', '^despesa')
L_Seca_23 = (Ativo_C_23-Estoque_23-Despesa_Antecipada_23)/Passivo_C_23 
#Liquidez Imediata(LI)
Caixa_23 = valor_contabil(df_23, '^1.0', '^caixa')
Aplicacao_F_23 = valor_contabil(df_23, '^1.0', '^aplica')
Disponivel_23 = Caixa_23+Aplicacao_F_23
L_Imediata_23 = Disponivel_23/Passivo_C_23
#Liquidez Geral(LG)
Ativo_RNC_23 = valor_contabil(df_23, '^1.0*', '^ativo realiz')
Passivo_NC_23 = valor_contabil(df_23, '^2.0*', '^passivo n.o cir')
L_Geral_23 = (Ativo_C_23+Ativo_RNC_23)/(Passivo_C_23+Passivo_NC_23)


#Capital de Giro e Tesouraria:

#ACF
Imposto_de_renda_AC_23 = valor_contabil(df_23, '^1.0', '^imposto de renda')
Disponivel_23 = Caixa_23+Aplicacao_F_23
Ativo_CF_23 = Disponivel_23+Imposto_de_renda_AC_23
#ACO
Ativo_CO_23 = Ativo_C_23-Ativo_CF_23
#PCF
Emprestimos_23 = valor_contabil(df_23, '^2.0', '^empr.stimo')
Provisoes_23 = valor_contabil(df_23, '^2.0', '^provis.es')
Imposto_de_renda_PC_23 = valor_contabil(df_23, '^2.0', '^imposto de renda')
Dividendos_23 = valor_contabil_2(df_23, '^2.0', '^dividendos')
Passivo_CF_23 = (Emprestimos_23+Provisoes_23+Imposto_de_renda_PC_23+Dividendos_23)
#PCO
Passivo_CO_23 = (Passivo_C_23-Passivo_CF_23)
#Capital de Giro(CDG)
Capital_de_Giro_23 = Ativo_C_23 - Passivo_C_23
#Necessidade de Capital de Giro(NCG)
Necessidade_de_CG_23 = Ativo_CO_23-Passivo_CO_23
#ST
Saldo_Tesouraria_23 = Ativo_CF_23-Passivo_CF_23



#Indices de Endividamento:

#RELACAO CT/CP = PASSIVO/PL
Patrimonio_L_23 = valor_contabil(df_23,'^2.*','patrim.nio')
CtCp_23 = (Passivo_C_23+Passivo_NC_23)/Patrimonio_L_23
#ENDIVIDAMENTO GERAL = PASSIVO/PASSIVO+PL
Endividamento_geral_23 = (Passivo_C_23+Passivo_NC_23)/(Passivo_C_23+Passivo_NC_23+Patrimonio_L_23)
#SOLVENCIA = ATIVO TOTAL/PASSIVO
Ativo_T_23 = valor_contabil(df_23,'^1.*','ativo total')
Solvencia_23 = Ativo_T_23/(Passivo_C_23+Passivo_NC_23)
#CE(Composição do endividamento) = PC/PASSIVO
Composicao_E_23 = Passivo_C_23/(Passivo_C_23+Passivo_NC_23)

#Em relação aos juros e empréstimos
#Passivo oneroso(deve juros)
POn_23 = (valor_contabil(df_23, '^2.01', '^empr.stimo'))+(valor_contabil(df_23, '^2.02', '^empr.stimo'))+(valor_contabil(df_23, '^2.01', '^deb.ntures'))+(valor_contabil(df_23, '^2.02', '^deb.ntures'))
#Passivo funcionamento
PFun_23 = (Passivo_C_23+Passivo_NC_23)-POn_23
#Divida liquida(Quanto da divida de emprestimos posso pagar com o caixa)
Divida_liquida_23 = POn_23 - Disponivel_23
#Investimento
Investimento_23 = POn_23 + Patrimonio_L_23
#Capital Oneroso
Capital_Oneroso_23 = Divida_liquida_23+Patrimonio_L_23
#Indice divida liquida/PL
Indice_DLPL_23 = Divida_liquida_23/Patrimonio_L_23
#Indice divida liquida/Capital Oneroso
Indice_DLCO_23 = Divida_liquida_23/Capital_Oneroso_23

#Custo médio ponderado de capital(CMPC)= Wi*Ki+We*Ke
   #Wi(Peso dos fiannciamentos) e We(Peso do capital social)
Wi_23 = POn_23/Investimento_23
We_23 = Patrimonio_L_23/Investimento_23
   #Ki(Desp.Fin.Liq/POn):
      #Alíquota
IR_Corrente_23 = (valor_contabil(df_23, '^3.0', '^imposto de renda'))*(-1)
Lair_23 = valor_contabil_2(df_23, '^3.0', 'antes')
Aliquota_23 = IR_Corrente_23/Lair_23
      #Benefício tributário
Despesa_Financeira_23 =  (valor_contabil(df_23,'^3.*','^despesas financeiras'))*(-1)
Benefício_Tributário_23 = Despesa_Financeira_23*Aliquota_23
      #Despesa financeira líquida
DF_Liquida_23 = Despesa_Financeira_23 - Benefício_Tributário_23
      #Ki(quanto que foi pago em relacao a divida total(em %))
Ki_23 = DF_Liquida_23/POn_23
      #Ke(valor fixo)
Ke_23 = 0,12
      #CMPC
Custo_MPC_23 = (Wi_23*Ki_23)+(We_23*Ke_23)



#Indice de PL = 3Is/PL
investimentos_23 = valor_contabil(df_23,'^1.*','^invest')
imobilizado_23 = valor_contabil(df_23,'^1.*','^imobilizado$')
intangivel_23 = valor_contabil(df_23,'^1.*','^intang*')
Patrimonio_L_23 = valor_contabil(df_23,'^2.*','patrim.nio')
Indice_PL_23 = (investimentos_23+intangivel_23+imobilizado_23)/Patrimonio_L_23




#Ciclos

#PME = (estoque med*360)/CMV
estoque_med = (Estoque_23+Estoque_24)/2
Custo_MV = valor_contabil(df,'^3.*','custo')
PM_Estocagem = ((estoque_med*360)/Custo_MV)*(-1)
#PMRV= (clientes med*360/Receita liquida))
clientes_23 = valor_contabil(df_23,'^1.*','clientes')
clientes_24 = valor_contabil(df,'^1.*','clientes')
clientes_med = (clientes_23+clientes_24)/2
Receita_liquida = valor_contabil(df,'^3.*','receita')
PM_Recebimento_V = (clientes_med*360)/Receita_liquida
#PMPF(fornecedor med*360/(Compra = Estoque Final - Estoque Inicial +CMV))
fornecedor_23 = valor_contabil(df_23,'^2.*','fornecedor')
fornecedor_24 = valor_contabil(df,'^2.*','fornecedor')
fornecedor_med = (fornecedor_23+fornecedor_24)/2
compra = Estoque_24 - Estoque_23 + Custo_MV
PM_Pagamento_F = ((fornecedor_med*360)/compra)*(-1)
#CO
Ciclo_Operacional = PM_Estocagem + PM_Recebimento_V
#CF
Ciclo_Financeiro = Ciclo_Operacional   - PM_Pagamento_F
#CE
Ciclo_Economico = PM_Estocagem

#===================================================================================
#===================================================================================
#===================================================================================
#===================================================================================

import pandas as pd

#Função achar valor
def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = (df[filtro_conta & filtro_descricao]['valor'].values[0])
    return valor

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = (df[filtro_conta & filtro_descricao]['valor'].values[1])
    return valor

#2024 4T
arquivo = 'C:\\Users\\CRDalas\\Desktop\\Programacao\\Análise de Dados\\Trabalho_Cont\\dados\\vulc.xlsx'
df = pd.read_excel(arquivo)
#pesquisar
df[df['descricao'].str.contains('deb.ntures', case=False)][['conta','descricao','valor']]


#AC e PC
Ativo_C_24 = valor_contabil(df, '^1.0', '^ativo cir')
Passivo_C_24 = valor_contabil(df, '^2.0', '^passivo cir')


#Indices de Liquidez:

#Liquidez Corrente(LS)
L_Corrente_24 = Ativo_C_24/Passivo_C_24
#Liquidez Seca(LS)
Estoque_24 = valor_contabil(df, '^1.0', '^estoque')
Despesa_Antecipada_24 = valor_contabil(df, '^1.0', '^despesa')
L_Seca_24 = (Ativo_C_24-Estoque_24-Despesa_Antecipada_24)/Passivo_C_24
#Liquidez Imediata(LI)
Caixa_24 = valor_contabil(df, '^1.0', '^caixa')
Aplicacao_F_24 = valor_contabil(df, '^1.0', '^aplica')
Disponivel_24 = Caixa_24+Aplicacao_F_24
L_Imediata_24 = Disponivel_24/Passivo_C_24
#Liquidez Geral(LG)
Ativo_RNC_24 = valor_contabil(df, '^1.0*', '^ativo realiz')
Passivo_NC_24 = valor_contabil(df, '^2.0*', '^passivo n.o cir')
L_Geral_24 = (Ativo_C_24+Ativo_RNC_24)/(Passivo_C_24+Passivo_NC_24)


#Capital de Giro e Tesouraria:

#ACF
Imposto_de_renda_AC_24 = valor_contabil(df, '^1.0', '^imposto de renda')
Disponivel_24 = Caixa_24+Aplicacao_F_24
Ativo_CF_24 = Disponivel_24+Imposto_de_renda_AC_24
#ACO
Ativo_CO_24 = Ativo_C_24-Ativo_CF_24
#PCF
Emprestimos_24 = valor_contabil(df, '^2.0', '^empr.stimo')
Provisoes_24 = valor_contabil(df, '^2.0', '^provis.es')
Imposto_de_renda_PC_24 = valor_contabil(df, '^2.0', '^imposto de renda')
Dividendos_24 = valor_contabil_2(df, '^2.0', '^dividendos')
Passivo_CF_24 = (Emprestimos_24+Provisoes_24+Imposto_de_renda_PC_24+Dividendos_24)
#PCO
Passivo_CO_24 = (Passivo_C_24-Passivo_CF_24)
#Capital de Giro(CDG)
Capital_de_Giro_24 = Ativo_C_24 - Passivo_C_24
#Necessidade de Capital de Giro(NCG)
Necessidade_de_CG_24 = Ativo_CO_24-Passivo_CO_24
#ST
Saldo_Tesouraria_24 = Ativo_CF_24-Passivo_CF_24



#Indices de Endividamento:

#RELACAO CT/CP = PASSIVO/PL
Patrimonio_L_24 = valor_contabil(df,'^2.*','patrim.nio')
CtCp_24 = (Passivo_C_24+Passivo_NC_24)/Patrimonio_L_24
#ENDIVIDAMENTO GERAL = PASSIVO/PASSIVO+PL
Endividamento_geral_24 = (Passivo_C_24+Passivo_NC_24)/(Passivo_C_24+Passivo_NC_24+Patrimonio_L_24)
#SOLVENCIA = ATIVO TOTAL/PASSIVO
Ativo_T_24 = valor_contabil(df,'^1.*','ativo total')
Solvencia_24 = Ativo_T_24/(Passivo_C_24+Passivo_NC_24)
#CE(Composição do endividamento) = PC/PASSIVO
Composicao_E_24 = Passivo_C_24/(Passivo_C_24+Passivo_NC_24)

#Em relação aos juros e empréstimos
#Passivo oneroso(deve juros)
POn_24 = (valor_contabil(df, '^2.01', '^empr.stimo'))+(valor_contabil(df, '^2.02', '^empr.stimo'))+(valor_contabil(df, '^2.01', '^deb.ntures'))+(valor_contabil(df, '^2.02', '^deb.ntures'))
#Passivo funcionamento
PFun_24 = (Passivo_C_24+Passivo_NC_24)-POn_24
#Divida liquida(Quanto da divida de emprestimos posso pagar com o caixa)
Divida_liquida_24 = POn_24 - Disponivel_24
#Investimento
Investimento_24 = POn_24 + Patrimonio_L_24
#Capital Oneroso
Capital_Oneroso_24 = Divida_liquida_24+Patrimonio_L_24
#Indice divida liquida/PL
Indice_DLPL_24 = Divida_liquida_24/Patrimonio_L_24
#Indice divida liquida/Capital Oneroso
Indice_DLCO_24 = Divida_liquida_24/Capital_Oneroso_24

#Custo médio ponderado de capital(CMPC)= Wi*Ki+We*Ke
   #Wi(Peso dos fiannciamentos) e We(Peso do capital social)
Wi_24 = POn_24/Investimento_24
We_24 = Patrimonio_L_24/Investimento_24
   #Ki(Desp.Fin.Liq/POn):
      #Alíquota
IR_Corrente_24 = (valor_contabil(df, '^3.0', '^imposto de renda'))*(-1)
Lair_24 = valor_contabil_2(df, '^3.0', 'antes')
Aliquota_24 = IR_Corrente_24/Lair_24
      #Benefício tributário
Despesa_Financeira_24 =  (valor_contabil(df,'^3.*','^despesas financeiras'))*(-1)
Benefício_Tributário_24 = Despesa_Financeira_24*Aliquota_24
      #Despesa financeira líquida
DF_Liquida_24 = Despesa_Financeira_24 - Benefício_Tributário_24
      #Ki(quanto que foi pago em relacao a divida total(em %))
Ki_24 = DF_Liquida_24/POn_24
      #Ke(valor fixo)
Ke_24 = 0,12
      #CMPC
Custo_MPC_24 = (Wi_24*Ki_24)+(We_24*Ke_24)



#Indice de PL = 3Is/PL
investimentos_24 = valor_contabil(df,'^1.*','^invest')
imobilizado_24 = valor_contabil(df,'^1.*','^imobilizado$')
intangivel_24 = valor_contabil(df,'^1.*','^intang*')
Patrimonio_L_24 = valor_contabil(df,'^2.*','patrim.nio')
Indice_PL_24 = (investimentos_24+intangivel_24+imobilizado_24)/Patrimonio_L_24





#2023 4T
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEyOTAwLCJpYXQiOjE3NDUzMjA5MDAsImp0aSI6IjQ1MWIyZWM5YTAxMTQ4YjRiZDYxZDQ4MGI0YmM1OWU1IiwidXNlcl9pZCI6NjB9.kssQqfnXMDQxA_gny7-6Hfoaj5DGhfFjYAh_CwC6Yp8"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'ticker': 'MRFG3',
'ano_tri': '20234T',
}

r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
r.json().keys()
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_23 = pd.DataFrame(balanco)



#pesquisar
df_23[df_23['descricao'].str.contains('antes', case=False)][['conta','descricao','valor']]

#AC e PC
Ativo_C_23 = valor_contabil(df_23, '^1.0', '^ativo cir')
Passivo_C_23 = valor_contabil(df_23, '^2.0', '^passivo cir')


#Indices de Liquidez:

#Liquidez Corrente(LS)
L_Corrente_23 = Ativo_C_23/Passivo_C_23
#Liquidez Seca(LS)
Estoque_23 = valor_contabil(df_23, '^1.0', '^estoque')
Despesa_Antecipada_23 = valor_contabil(df_23, '^1.0', '^despesa')
L_Seca_23 = (Ativo_C_23-Estoque_23-Despesa_Antecipada_23)/Passivo_C_23 
#Liquidez Imediata(LI)
Caixa_23 = valor_contabil(df_23, '^1.0', '^caixa')
Aplicacao_F_23 = valor_contabil(df_23, '^1.0', '^aplica')
Disponivel_23 = Caixa_23+Aplicacao_F_23
L_Imediata_23 = Disponivel_23/Passivo_C_23
#Liquidez Geral(LG)
Ativo_RNC_23 = valor_contabil(df_23, '^1.0*', '^ativo realiz')
Passivo_NC_23 = valor_contabil(df_23, '^2.0*', '^passivo n.o cir')
L_Geral_23 = (Ativo_C_23+Ativo_RNC_23)/(Passivo_C_23+Passivo_NC_23)


#Capital de Giro e Tesouraria:

#ACF
Imposto_de_renda_AC_23 = valor_contabil(df_23, '^1.0', '^imposto de renda')
Disponivel_23 = Caixa_23+Aplicacao_F_23
Ativo_CF_23 = Disponivel_23+Imposto_de_renda_AC_23
#ACO
Ativo_CO_23 = Ativo_C_23-Ativo_CF_23
#PCF
Emprestimos_23 = valor_contabil(df_23, '^2.0', '^empr.stimo')
Provisoes_23 = valor_contabil(df_23, '^2.0', '^provis.es')
Imposto_de_renda_PC_23 = valor_contabil(df_23, '^2.0', '^imposto de renda')
Dividendos_23 = valor_contabil_2(df_23, '^2.0', '^dividendos')
Passivo_CF_23 = (Emprestimos_23+Provisoes_23+Imposto_de_renda_PC_23+Dividendos_23)
#PCO
Passivo_CO_23 = (Passivo_C_23-Passivo_CF_23)
#Capital de Giro(CDG)
Capital_de_Giro_23 = Ativo_C_23 - Passivo_C_23
#Necessidade de Capital de Giro(NCG)
Necessidade_de_CG_23 = Ativo_CO_23-Passivo_CO_23
#ST
Saldo_Tesouraria_23 = Ativo_CF_23-Passivo_CF_23



#Indices de Endividamento:

#RELACAO CT/CP = PASSIVO/PL
Patrimonio_L_23 = valor_contabil(df_23,'^2.*','patrim.nio')
CtCp_23 = (Passivo_C_23+Passivo_NC_23)/Patrimonio_L_23
#ENDIVIDAMENTO GERAL = PASSIVO/PASSIVO+PL
Endividamento_geral_23 = (Passivo_C_23+Passivo_NC_23)/(Passivo_C_23+Passivo_NC_23+Patrimonio_L_23)
#SOLVENCIA = ATIVO TOTAL/PASSIVO
Ativo_T_23 = valor_contabil(df_23,'^1.*','ativo total')
Solvencia_23 = Ativo_T_23/(Passivo_C_23+Passivo_NC_23)
#CE(Composição do endividamento) = PC/PASSIVO
Composicao_E_23 = Passivo_C_23/(Passivo_C_23+Passivo_NC_23)

#Em relação aos juros e empréstimos
#Passivo oneroso(deve juros)
POn_23 = (valor_contabil(df_23, '^2.01', '^empr.stimo'))+(valor_contabil(df_23, '^2.02', '^empr.stimo'))+(valor_contabil(df_23, '^2.01', '^deb.ntures'))+(valor_contabil(df_23, '^2.02', '^deb.ntures'))
#Passivo funcionamento
PFun_23 = (Passivo_C_23+Passivo_NC_23)-POn_23
#Divida liquida(Quanto da divida de emprestimos posso pagar com o caixa)
Divida_liquida_23 = POn_23 - Disponivel_23
#Investimento
Investimento_23 = POn_23 + Patrimonio_L_23
#Capital Oneroso
Capital_Oneroso_23 = Divida_liquida_23+Patrimonio_L_23
#Indice divida liquida/PL
Indice_DLPL_23 = Divida_liquida_23/Patrimonio_L_23
#Indice divida liquida/Capital Oneroso
Indice_DLCO_23 = Divida_liquida_23/Capital_Oneroso_23

#Custo médio ponderado de capital(CMPC)= Wi*Ki+We*Ke
   #Wi(Peso dos fiannciamentos) e We(Peso do capital social)
Wi_23 = POn_23/Investimento_23
We_23 = Patrimonio_L_23/Investimento_23
   #Ki(Desp.Fin.Liq/POn):
      #Alíquota
IR_Corrente_23 = (valor_contabil(df_23, '^3.0', '^imposto de renda'))*(-1)
Lair_23 = valor_contabil_2(df_23, '^3.0', 'antes')
Aliquota_23 = IR_Corrente_23/Lair_23
      #Benefício tributário
Despesa_Financeira_23 =  (valor_contabil(df_23,'^3.*','^despesas financeiras'))*(-1)
Benefício_Tributário_23 = Despesa_Financeira_23*Aliquota_23
      #Despesa financeira líquida
DF_Liquida_23 = Despesa_Financeira_23 - Benefício_Tributário_23
      #Ki(quanto que foi pago em relacao a divida total(em %))
Ki_23 = DF_Liquida_23/POn_23
      #Ke(valor fixo)
Ke_23 = 0,12
      #CMPC
Custo_MPC_23 = (Wi_23*Ki_23)+(We_23*Ke_23)



#Indice de PL = 3Is/PL
investimentos_23 = valor_contabil(df_23,'^1.*','^invest')
imobilizado_23 = valor_contabil(df_23,'^1.*','^imobilizado$')
intangivel_23 = valor_contabil(df_23,'^1.*','^intang*')
Patrimonio_L_23 = valor_contabil(df_23,'^2.*','patrim.nio')
Indice_PL_23 = (investimentos_23+intangivel_23+imobilizado_23)/Patrimonio_L_23




#Ciclos

#PME = (estoque med*360)/CMV
estoque_med = (Estoque_23+Estoque_24)/2
Custo_MV = valor_contabil(df,'^3.*','custo')
PM_Estocagem = ((estoque_med*360)/Custo_MV)*(-1)
#PMRV= (clientes med*360/Receita liquida))
clientes_23 = valor_contabil(df_23,'^1.*','clientes')
clientes_24 = valor_contabil(df,'^1.*','clientes')
clientes_med = (clientes_23+clientes_24)/2
Receita_liquida = valor_contabil(df,'^3.*','receita')
PM_Recebimento_V = (clientes_med*360)/Receita_liquida
#PMPF(fornecedor med*360/(Compra = Estoque Final - Estoque Inicial +CMV))
fornecedor_23 = valor_contabil(df_23,'^2.*','fornecedor')
fornecedor_24 = valor_contabil(df,'^2.*','fornecedor')
fornecedor_med = (fornecedor_23+fornecedor_24)/2
compra = Estoque_24 - Estoque_23 + Custo_MV
PM_Pagamento_F = ((fornecedor_med*360)/compra)*(-1)
#CO
Ciclo_Operacional = PM_Estocagem + PM_Recebimento_V
#CF
Ciclo_Financeiro = Ciclo_Operacional   - PM_Pagamento_F
#CE
Ciclo_Economico = PM_Estocagem
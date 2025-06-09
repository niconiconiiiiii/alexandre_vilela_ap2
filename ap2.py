import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
pio.renderers.default = "browser"
import dash
from dash import dcc, html, Input, Output
pio.templates.default = "plotly_dark"


def balanco(ticker, trimestre):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM5MDkxLCJpYXQiOjE3NDgzNDcwODIsImp0aSI6IjAyNzZjMTQ3Y2I1ZTQ1OWViYjI1YzY1MDgyMDViMThkIiwidXNlcl9pZCI6NjV9.onCBVUskjQJHWCBJ2P-T27zfydezZwtLfPR7bYUFwNU"
    headers = {'Authorization': 'JWT {}'.format(token)}
    empresa = f"{ticker}"
    data = f"{trimestre}"

    params = {
    'ticker': empresa,
    'ano_tri': data,
    }

    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    r.json().keys()
    dados = r.json()['dados'][0]
    balanco = dados['balanco']
    df = pd.DataFrame(balanco)
    return df

def preco_corrigido(ticker, dataini, datafim):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM5MDkxLCJpYXQiOjE3NDgzNDcwODIsImp0aSI6IjAyNzZjMTQ3Y2I1ZTQ1OWViYjI1YzY1MDgyMDViMThkIiwidXNlcl9pZCI6NjV9.onCBVUskjQJHWCBJ2P-T27zfydezZwtLfPR7bYUFwNU"
    headers = {'Authorization': 'JWT {}'.format(token)}
    empresa = f"{ticker}"
    data_ini = f"{dataini}"
    data_fim = f"{datafim}"
    params = {
    'ticker': empresa,
    'data_ini': data_ini,
    'data_fim': data_fim
    }
    if ticker=='ibov':
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos',params=params, headers=headers)
    else:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
    r.json().keys()
    dados = r.json()['dados']
    df = pd.DataFrame(dados)
    return df

def valor_acao(df):
    preco_ini = df.iloc[0]['fechamento']
    preco_fim = df.iloc[-1]['fechamento']
    lucro_acao = preco_fim/preco_ini
    return {
        'preco_ini' : preco_ini,
        'preco_fim' : preco_fim,
        'lucro_acao': lucro_acao
    }

def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = (df[filtro_conta & filtro_descricao]['valor'].values[0])
    return valor

def valor_contabil_2(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = sum(df[filtro_conta & filtro_descricao]['valor'].values)
    return valor

def indices_basicos(df):
    Ativo_C = valor_contabil(df, '^1.0', '^ativo cir')
    Estoque = valor_contabil(df, '^1.0', '^estoque')
    Despesa_Antecipada = valor_contabil(df, '^1.0', '^despesa')
    Caixa = valor_contabil(df, '^1.0', '^caixa')
    Aplicacao_F = valor_contabil(df, '^1.0', '^aplica')
    Disponivel = Caixa + Aplicacao_F
    Ativo_RNC = valor_contabil(df, '^1.0*', '^ativo realiz')
    Ativo_NR = valor_contabil(df,'^1.*','^invest') + valor_contabil(df,'^1.*','^imobilizado$') + valor_contabil(df,'^1.*','^intang*')
    Passivo_C = valor_contabil(df, '^2.0', '^passivo cir')
    Passivo_NC = valor_contabil(df, '^2.0*', '^passivo n.o cir')
    Patrimonio_L = valor_contabil(df,'^2.*','patrim.nio')
    POn = (valor_contabil(df, '^2.01', '^empr.stimo'))+(valor_contabil(df, '^2.02', '^empr.stimo'))+(valor_contabil(df, '^2.01', '^deb.ntures'))+(valor_contabil(df, '^2.02', '^deb.ntures'))
    Imposto_de_renda_AC = valor_contabil(df, '^1.0', '^imposto de renda')
    Emprestimos = valor_contabil(df, '^2.0', '^empr.stimo')
    Provisoes = valor_contabil(df, '^2.0', '^provis.es')
    Imposto_de_renda_PC = valor_contabil(df, '^2.0', '^imposto de renda')
    Dividendos = valor_contabil_2(df, '^2.0', '^dividendos')
    Ativo_T = valor_contabil(df,'^1.*','ativo total')
    Investimento = POn + Patrimonio_L
    IR_Corrente = (valor_contabil(df, '^3.0', '^imposto de renda'))*(-1)
    Lair = valor_contabil_2(df, '^3.0', 'antes')
    Despesa_Financeira =  (valor_contabil(df,'^3.*','^despesas financeiras'))*(-1)
    investimentos = valor_contabil(df,'^1.*','^invest')
    imobilizado = valor_contabil(df,'^1.*','^imobilizado$')
    intangivel = valor_contabil(df,'^1.*','^intang*')
    Custo_MV = valor_contabil(df,'^3.*','custo')
    Clientes = valor_contabil(df,'^1.*','clientes')
    Receita_liquida = valor_contabil(df,'^3.*','receita')
    Fornecedor = valor_contabil(df,'^2.*','fornecedor')
    Ebit = valor_contabil(df, '^3.0', 'Resultado Antes do Resultado')
    Amortizacao = valor_contabil(df, '^6.0', 'Amortiza')
    Lucro_Liquido = valor_contabil(df, '^3.', 'Consolidado')
    Ke = 0.1725
    
    return {
        'Ativo_C'            : Ativo_C,
        'Estoque'            : Estoque,
        'Despesa_Antecipada' : Despesa_Antecipada,
        'Caixa'              : Caixa,
        'Aplicacao_F'        : Aplicacao_F,
        'Disponivel'         : Disponivel,
        'Ativo_RNC'          : Ativo_RNC,
        'Ativo_NR'           : Ativo_NR,
        'Passivo_C'          : Passivo_C,
        'Passivo_NC'         : Passivo_NC,
        'Patrimonio_L'       : Patrimonio_L,
        'POn'                : POn,
        'Imposto_de_renda_AC': Imposto_de_renda_AC,
        'Emprestimos'        : Emprestimos,
        'Provisoes'          : Provisoes,
        'Imposto_de_renda_PC': Imposto_de_renda_PC,
        'Dividendos'         : Dividendos,
        'Ativo_T'            : Ativo_T,
        'Investimento'       : Investimento,
        'IR_Corrente'        : IR_Corrente,
        'Lair'               : Lair,
        'Despesa_Financeira' : Despesa_Financeira,
        'investimentos'      : investimentos,
        'imobilizado'        : imobilizado,
        'intangivel'         : intangivel,
        'Custo_MV'           : Custo_MV,
        'Clientes'           : Clientes,
        'Receita_liquida'    : Receita_liquida,
        'Fornecedor'         : Fornecedor,
        'Ebit'               : Ebit,
        'Amortizacao'        : Amortizacao,
        'Lucro_Liquido'      : Lucro_Liquido,
        'Ke'                 : Ke
    }


def indices_dividas(indices_basicos):
    Divida_Terceiros = indices_basicos["POn"]
    Divida_Acionistas = indices_basicos["Patrimonio_L"]
    Lucro_Liquido = indices_basicos["Lucro_Liquido"]

    return {
        'Divida_Terceiros' : Divida_Terceiros,
        'Divida_Acionistas': Divida_Acionistas,
        'Lucro_Liquido'    : Lucro_Liquido
    }

def indices_liquidez(indices_basicos):
    Ativo_C = indices_basicos["Ativo_C"]
    Passivo_C = indices_basicos["Passivo_C"]
    Estoque = indices_basicos["Estoque"]
    Despesa_Antecipada = indices_basicos["Despesa_Antecipada"]
    Disponivel = indices_basicos["Disponivel"]
    Ativo_RNC = indices_basicos["Ativo_RNC"]
    Passivo_NC = indices_basicos["Passivo_NC"]
    

    L_Corrente = Ativo_C / Passivo_C
    L_Seca = (Ativo_C - Estoque - Despesa_Antecipada) / Passivo_C
    L_Imediata = Disponivel / Passivo_C
    L_Geral = (Ativo_C + Ativo_RNC) / (Passivo_C + Passivo_NC)


    return {
        'L_Corrente': L_Corrente,
        'L_Seca'    : L_Seca,
        'L_Imediata': L_Imediata,
        'L_Geral'   : L_Geral,
    }

def indices_giro_tesouraria(indices_basicos):
    Ativo_C = indices_basicos["Ativo_C"]
    Passivo_C = indices_basicos["Passivo_C"]
    Disponivel = indices_basicos["Disponivel"]
    Imposto_de_renda_AC = indices_basicos["Imposto_de_renda_AC"]
    Emprestimos = indices_basicos["Emprestimos"]
    Provisoes = indices_basicos["Provisoes"]
    Imposto_de_renda_PC = indices_basicos["Imposto_de_renda_PC"]
    Dividendos = indices_basicos["Dividendos"]

    Ativo_CF = Disponivel + Imposto_de_renda_AC
    Ativo_CO = Ativo_C - Ativo_CF
    Passivo_CF = (Emprestimos + Provisoes + Imposto_de_renda_PC + Dividendos)
    Passivo_CO = (Passivo_C - Passivo_CF)
    #Capital de Giro
    Capital_de_Giro = Ativo_C - Passivo_C
    #Necessidade de Capital de Giro
    Necessidade_de_CG = Ativo_CO - Passivo_CO
    #Saldo Tesouraria
    Saldo_Tesouraria = Ativo_CF - Passivo_CF

    return {
        'Capital_de_Giro'   : Capital_de_Giro,
        'Necessidade_de_CG' : Necessidade_de_CG,
        'Saldo_Tesouraria'  : Saldo_Tesouraria,
    }

def indices_endividamento(indices_basicos):
    Passivo_C = indices_basicos["Passivo_C"]
    Passivo_NC = indices_basicos["Passivo_NC"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]
    Ativo_T = indices_basicos["Ativo_T"]

    CtCp = (Passivo_C + Passivo_NC) / Patrimonio_L
    Endividamento_geral = (Passivo_C + Passivo_NC) / (Passivo_C + Passivo_NC + Patrimonio_L)
    Solvencia = Ativo_T / (Passivo_C + Passivo_NC)
    Composicao_E = Passivo_C / (Passivo_C + Passivo_NC)

    return {
        'CtCp'               : CtCp,
        'Endividamento_geral': Endividamento_geral,
        'Solvencia'          : Solvencia,
        'Composicao_E'       : Composicao_E,
    }

def indices_emprestimos(indices_basicos):
    Passivo_C = indices_basicos["Passivo_C"]
    Passivo_NC = indices_basicos["Passivo_NC"]
    Disponivel = indices_basicos["Disponivel"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]
    POn = indices_basicos["POn"]

    PFun = (Passivo_C+Passivo_NC)-POn
    Divida_liquida = POn - Disponivel
    Capital_Oneroso = Divida_liquida+Patrimonio_L
    Indice_DLPL = Divida_liquida/Patrimonio_L
    Indice_DLCO = Divida_liquida/Capital_Oneroso
    
    return {
        'PFun'            : PFun,
        'Indice_DLCO'     : Indice_DLCO,
        'Indice_DLPL'     : Indice_DLPL,
    }

def indices_juros(indices_basicos):
    POn = indices_basicos["POn"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]
    Investimento = indices_basicos["Investimento"]
    IR_Corrente = indices_basicos["IR_Corrente"]
    Lair = indices_basicos["Lair"]
    Despesa_Financeira = indices_basicos["Despesa_Financeira"]

   #Custo médio ponderado de capital(CMPC)= Wi*Ki+We*Ke
   #Wi(Peso dos fiananciamentos) e We(Peso do capital social)
    Wi = POn / Investimento
    We = Patrimonio_L / Investimento
    Aliquota = IR_Corrente / Lair
    Benefício_Tributário = Despesa_Financeira * Aliquota
    DF_Liquida = Despesa_Financeira - Benefício_Tributário
    #Ki(quanto que foi pago em relacao a divida total(em %))
    Ki = DF_Liquida / POn
    Ke = 0.1725
    Custo_MPC = (Wi * Ki) + (We * Ke)

    return {
        'Custo_MPC' : Custo_MPC
    }

def indice_nao_realizavel(indices_basicos):
    investimentos = indices_basicos["investimentos"]
    imobilizado = indices_basicos["imobilizado"]
    intangivel = indices_basicos["intangivel"]
    Patrimonio_L = indices_basicos["Patrimonio_L"]

    Indice_PL = (investimentos + intangivel + imobilizado) / Patrimonio_L

    return {
        'Indice_PL' : Indice_PL
    }

def indices_ciclos(basicos_23, basicos_24):
    Clientes_23 = basicos_23['Clientes']
    Fornecedor_23 = basicos_23['Fornecedor']
    Estoque_23 = basicos_23['Estoque']
    Custo_MV_24 = basicos_24['Custo_MV']
    Clientes_24 = basicos_24['Clientes']
    Receita_liquida_24 = basicos_24['Receita_liquida']
    Fornecedor_24 = basicos_24['Fornecedor']
    Estoque_24 = basicos_24['Estoque']
    
    #PME
    Estoque_med = (Estoque_23+Estoque_24)/2
    PM_Estocagem = ((Estoque_med*360)/Custo_MV_24)*(-1)
    #PMRV= (clientes med*360/Receita liquida))
    Clientes_med = (Clientes_23+Clientes_24)/2
    PM_Recebimento_V = (Clientes_med*360)/Receita_liquida_24
    #PMPF(fornecedor med*360/(Compra = Estoque Final - Estoque Inicial +CMV))
    Fornecedor_med = (Fornecedor_23+Fornecedor_24)/2
    compra = Estoque_24 - Estoque_23 + Custo_MV_24
    PM_Pagamento_F = ((Fornecedor_med*360)/compra)*(-1)
    #CO
    Ciclo_Operacional = PM_Estocagem + PM_Recebimento_V
    #CF
    Ciclo_Financeiro = Ciclo_Operacional - PM_Pagamento_F
    #CE
    Ciclo_Economico = PM_Estocagem
    return {
        'PM_Estocagem'     : PM_Estocagem,
        'PM_Recebimento_V' : PM_Recebimento_V,
        'PM_Pagamento_F'   : PM_Pagamento_F,
        'Ciclo_Operacional': Ciclo_Operacional,
        'Ciclo_Financeiro' : Ciclo_Financeiro,
        'Ciclo_Economico'  : Ciclo_Economico
    }

def indices_rentabilidade(indices_basicos):
    Investimento = indices_basicos['Investimento']
    Ebit = indices_basicos['Ebit']
    Amortizacao = indices_basicos['Amortizacao']
    IR_Corrente = indices_basicos['IR_Corrente']
    Lucro_Liquido = indices_basicos['Lucro_Liquido']
    Patrimonio_L = indices_basicos['Patrimonio_L']

    #Lucros antes da amortizacao e depois do imposto de renda
    Ebitda = Ebit + Amortizacao
    Nopat = Ebit - IR_Corrente
    #Retorno de Investimento(de financiamentos e capital social)
    Roi = Nopat/Investimento
    #Retorno do patrimonio(apenas capital social)
    Roe = Lucro_Liquido/Patrimonio_L
    #Grau de Alavancagem financeira
    Gaf = Roe/Roi

    return {
        'Ebitda': Ebitda,
        'Nopat' : Nopat,
        'Roi'   : Roi,
        'Roe'   : Roe,
        'Gaf'   : Gaf
    }

def indices_valor_agregado(indices_basicos, indices_juros, indices_rentabilidade):
    Custo_MPC = indices_juros['Custo_MPC']
    Investimento = indices_basicos['Investimento']
    Roe = indices_rentabilidade['Roe']
    Ke = indices_basicos['Ke']
    Lucro_Liquido = indices_basicos['Lucro_Liquido']
    Eva = Lucro_Liquido-(Investimento*Custo_MPC)
    Spread = Roe-Ke
    return {
        'Eva'    : Eva,
        'Spread' : Spread,
        'Roe'    : Roe
    }

def print_dict(name, ticker, trimestre, data):
    print(f"{name} — {ticker} — {trimestre}")
    for key, value in data.items():
        print(f"  {key}: {value}")
    print()

def print_dict_2(name, ticker, dataini, datafim, data):
    print(f"{name} — {ticker} — {dataini}/{datafim}")
    for key, value in data.items():
        print(f"  {key}: {value}")
    print()

def rodar_dashboard_completo(preco_corrigido_func, balanco_func, tickers, tickers_balanco, datas_ini, data_fim, trimestres):
    
    # Pré-carrega dados de preços
    dados_precos = {}
    for ticker in tickers:
        dados_precos[ticker] = {}
        for dataini in datas_ini:
            df = preco_corrigido_func(ticker, dataini, data_fim)
            df['data'] = pd.to_datetime(df['data'])
            df = df.sort_values('data')
            df['preco_norm'] = df['fechamento'] / df['fechamento'].iloc[0] * 100
            dados_precos[ticker][dataini] = df

    # Pré-carrega dados de balanço para o gráfico de rosca
    dados_balanco = {}
    for ticker in tickers_balanco:
        dados_balanco[ticker] = {}
        for trimestre in trimestres:
            df = balanco_func(ticker, trimestre)
            basicos = indices_basicos(df)
            dividas = indices_dividas(basicos)
            dados_balanco[ticker][trimestre] = dividas

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Div([
        html.H1("Dashboard Financeiro", style={'textAlign': 'center', 'marginBottom': '5px'}),
        html.H4("Análise de Ações – MRFG3, JBSS3, BEEF3, BRFS3, IBOV",
                 style={'textAlign': 'center', 'color': '#CCCCCC', 'marginTop': '0px'})
    ], style={'backgroundColor': '#303030', 'padding': '10px', 'borderRadius': '8px'}),
        # Seção de Preços Normalizados
        html.Div([
        html.H2("1. Preços Normalizados — Múltiplos Tickers"),
        html.Div([
            html.Label("Escolha os tickers:"),
            dcc.Dropdown(
                id='ticker-dropdown',
                options=[{'label': t, 'value': t} for t in tickers],
                value=[tickers[0]],
                multi=True,
                clearable=False,
                style={'width': '48%'}
            ),
            html.Label("Escolha o período inicial:"),
            dcc.Dropdown(
                id='periodo-dropdown',
                options=[{'label': d, 'value': d} for d in datas_ini],
                value=datas_ini[0],
                clearable=False,
                style={'width': '48%', 'marginTop': '10px'}
            )
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        dcc.Graph(id='grafico-precos')
    ], style={'marginBottom': '30px', 'padding': '10px', 'backgroundColor': '#1f1f1f', 'borderRadius': '8px'}),

        
        # Seção de Análise de Dívidas
        html.Div([
        html.H2("2. Composição Financeira (Dívidas vs Lucro)"),
        html.Div([
            html.Label("Escolha o ticker:"),
            dcc.Dropdown(
                id='ticker-ros-dropdown',
                options=[{'label': t, 'value': t} for t in tickers_balanco],
                value=tickers_balanco[0],
                clearable=False,
                style={'width': '48%'}
            ),
            html.Label("Escolha o trimestre:"),
            dcc.Dropdown(
                id='trimestre-dropdown',
                options=[{'label': t, 'value': t} for t in trimestres],
                value=trimestres[0],
                clearable=False,
                style={'width': '48%', 'marginTop': '10px'}
            )
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        dcc.Graph(id='grafico-rosca')
    ], style={'padding': '10px', 'backgroundColor': '#1f1f1f', 'borderRadius': '8px'}),
        ])
    

    # Callback para o gráfico de preços
    @app.callback(
        Output('grafico-precos', 'figure'),
        Input('ticker-dropdown', 'value'),
        Input('periodo-dropdown', 'value')
    )
    def atualizar_grafico_precos(tickers_selecionados, periodo_selecionado):
        fig = go.Figure()
        data_fim = datetime.now().strftime('%Y-%m-%d')  # Data atual como padrão
        
        if isinstance(tickers_selecionados, str):
            tickers_selecionados = [tickers_selecionados]

        for ticker in tickers_selecionados:
            try:
                df = preco_corrigido(ticker, periodo_selecionado, data_fim)
                df['data'] = pd.to_datetime(df['data'])
                df = df.sort_values('data')
                
                preco_inicial = df['fechamento'].iloc[0]
                df['preco_norm'] = (df['fechamento'] / preco_inicial) * 100
                
                fig.add_trace(go.Scatter(
                    x=df['data'],
                    y=df['preco_norm'],
                    name=f'{ticker}',
                    line=dict(width=2),
                    hovertemplate='Data: %{x|%d/%m/%Y}<br>Valor: %{y:.1f} (base 100)'
                ))
            
            except Exception as e:
                print(f"Erro ao processar {ticker}: {str(e)}")

        fig.update_layout(
            title=f'Performance Relativa (Base 100) desde {periodo_selecionado}',
            xaxis_title='Data',
            yaxis_title='Valor Normalizado',
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    

    # Callback para o gráfico de rosca 
    @app.callback(
        Output('grafico-rosca', 'figure'),
        Input('ticker-ros-dropdown', 'value'),
        Input('trimestre-dropdown', 'value')
    )
    
    def atualizar_grafico_rosca(ticker_selecionado, trimestre_selecionado):
        dividas = dados_balanco[ticker_selecionado][trimestre_selecionado]
        
        # Apenas os dois componentes 
        labels = ['Dívida Terceiros', 'Dívida Acionistas']
        values = [
            dividas['Divida_Terceiros'],
            dividas['Divida_Acionistas']
        ]
        
        # Cores ajustadas (vermelho para dívida, azul para patrimônio líquido)
        colors = ['#FF6347', '#013A63']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.5,
            marker_colors=colors,
            textinfo='percent+value',
            insidetextorientation='radial',
            texttemplate='%{label}<br>%{value:,.0f}<br>(%{percent})'
        )])
        
        fig.update_layout(
            title=f'Estrutura de Capital: {ticker_selecionado} ({trimestre_selecionado})',
            annotations=[dict(
                text=f"Endividamento<br>Total:<br>{sum(values):,.0f}",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )],
            template='plotly_dark',
            margin=dict(t=60, b=30)  # Ajuste de margens
        )
        
        return fig

    app.run(debug=False)


def main():

    list_ticker = []
    list_ticker.append("MRFG3")
    list_ticker.append("JBSS3")
    list_ticker.append("BEEF3")
    list_ticker.append("BRFS3")
    

    list_tri = []
    list_tri.append("20234T")
    list_tri.append("20244T")
      
    list_df = []
    list_dividas = []
    list_liquidez = []
    list_giro_tesouraria = []
    list_endividamento = []
    list_emprestimos = []
    list_juros = []
    list_nao_realizavel = []
    list_ciclos = []
    list_rentabilidade = []
    list_valor_agregado = []

    ticker_repetidos = []

    for ticker in list_ticker:
        list_basicos = []
        for trimestre in list_tri:
            ticker_repetidos.append(ticker)
            df = balanco(ticker, trimestre)
            list_df.append(df)

            basicos = indices_basicos(df)
            dividas = indices_dividas(basicos)
            liquidas = indices_liquidez(basicos)
            giro = indices_giro_tesouraria(basicos)
            endividamento = indices_endividamento(basicos)
            emprestimo = indices_emprestimos(basicos)
            juros = indices_juros(basicos)
            nao_realizavel = indice_nao_realizavel(basicos)
            rentabilidade = indices_rentabilidade(basicos)
            valor_agregado = indices_valor_agregado(basicos, juros, rentabilidade)

            list_basicos.append(basicos)
            list_dividas.append(dividas)
            list_liquidez.append(liquidas)
            list_giro_tesouraria.append(giro)
            list_endividamento.append(endividamento)
            list_emprestimos.append(emprestimo)
            list_juros.append(juros)
            list_nao_realizavel.append(nao_realizavel)
            list_rentabilidade.append(rentabilidade)
            list_valor_agregado.append(valor_agregado)

            print_dict("Índices Básicos",        ticker, trimestre, basicos)
            print_dict("Índices de Liquidez",     ticker, trimestre, liquidas)
            print_dict("Giro de Tesouraria",      ticker, trimestre, giro)
            print_dict("Índice de Endividamento", ticker, trimestre, endividamento)
            print_dict("Empréstimos",             ticker, trimestre, emprestimo)
            print_dict("Índice de Juros",         ticker, trimestre, juros)
            print_dict("Não Realizável",          ticker, trimestre, nao_realizavel)
            print_dict("Rentabilidade",          ticker, trimestre, rentabilidade)
            print_dict("Valor Agregado",          ticker, trimestre, valor_agregado)

        
        ciclos = indices_ciclos(list_basicos[0], list_basicos[1])
        list_basicos.clear()

        list_ciclos.append(ciclos)
       
        # imprime ciclos
        header = f"Ciclos — {ticker} — {list_tri[0]} & {list_tri[1]}"
        print(header)
        for key, value in ciclos.items():
            print(f"  {key}: {value}")
        print()
    df_valor_agregado = pd.DataFrame(list_valor_agregado)
    df_valor_agregado['Ticker'] = ticker_repetidos
    print(df_valor_agregado)
    df_dividas = pd.DataFrame(list_dividas)
    df_dividas['Ticker'] = ticker_repetidos
    print(df_dividas)
    

    list_ticker_2 = []
    list_ticker_2.append("MRFG3")
    list_ticker_2.append("JBSS3")
    list_ticker_2.append("BEEF3")
    list_ticker_2.append("BRFS3")
    list_ticker_2.append("ibov")

    list_df2 = []
    list_data_fim = []
    list_data_fim.append('2025-03-31')
    list_data_ini = []
    list_data_ini.append('2023-04-01')
    list_data_ini.append('2019-04-01')
    list_data_ini.append('2014-04-01')

    list_valor_acao = []
    for ticker in list_ticker_2:
        for datafim in list_data_fim:
            for dataini in list_data_ini:
                df = preco_corrigido(ticker, dataini, datafim)
                list_df2.append(df)
                valores_acao = valor_acao(df)

                list_valor_acao.append(valores_acao)
                print_dict_2("Valores da Ação", ticker, dataini, datafim, valores_acao)
    

    rodar_dashboard_completo(
    preco_corrigido_func=preco_corrigido,
    balanco_func=balanco,
    tickers=list_ticker_2,
    tickers_balanco=list_ticker,
    datas_ini=list_data_ini,
    data_fim=list_data_fim[0],
    trimestres=list_tri
)

  
main()

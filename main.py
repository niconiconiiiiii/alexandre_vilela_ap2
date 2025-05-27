from modulos import (dataframe, valor_contabil, valor_contabil_2, indices_basicos, indices_liquidez,
                      indices_giro_tesouraria, indices_endividamento, indices_emprestimos, 
                      indices_juros, indice_nao_realizavel, indices_ciclos, indices_rentabilidade,
                        indices_valor_agregado, print_dict)

import pandas as pd
def main():

    list_ticker = []
    list_ticker.append("JBSS3")
    list_ticker.append("MRFG3")
    list_ticker.append("BRFS3")
    list_ticker.append("BEEF3")
    
    

    list_tri = []
    list_tri.append("20234T")
    list_tri.append("20244T")
    
    list_df = []
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
            df = dataframe(ticker, trimestre)
            list_df.append(df)

            basicos = indices_basicos(df)
            liquidas = indices_liquidez(basicos)
            giro = indices_giro_tesouraria(basicos)
            endividamento = indices_endividamento(basicos)
            emprestimo = indices_emprestimos(basicos)
            juros = indices_juros(basicos)
            nao_realizavel = indice_nao_realizavel(basicos)
            rentabilidade = indices_rentabilidade(basicos)
            valor_agregado = indices_valor_agregado(basicos, juros, rentabilidade)

            list_basicos.append(basicos)

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
     
    #Dataframe
    df_valor_agregado = pd.DataFrame(list_valor_agregado)
    df_valor_agregado['Ticker'] = ticker_repetidos
    print(df_valor_agregado)

main()


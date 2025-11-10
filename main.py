import pandas as pd
import numpy as np
import sys
from typing import List, Optional, Tuple

# --- 1. Importar funções dos seus outros arquivos ---

try:
    # Traz a função que processa e imprime o Cronbach
    from cronbach_alpha import processar_csv_cronbach

    # Traz as DUAS funções de correlacao.py
    from correlacao import analisar_correlacao_pearson, classificar_correlacao

except ImportError as e:
    print(f"Erro: Não foi possível encontrar 'cronbach_alpha.py' ou 'correlacao.py'.")
    print(f"Detalhe: {e}")
    print(
        "Por favor, certifique-se que todos os arquivos .py estão no mesmo diretório."
    )
    sys.exit(1)


# --- 2. Funções de Execução ---


def executar_formatacao() -> bool:
    """
    Lógica de 'formatar_respostas.py'.
    Limpa 'respostas.csv' e salva 'respostas_formatadas.csv'.
    Retorna True se sucesso, False se falhar.
    """
    print("--- 1. Formatando Dados ---")
    arquivo_original = "respostas.csv"
    arquivo_saida = "respostas_formatadas.csv"

    try:
        df = pd.read_csv(arquivo_original, encoding="utf-8", sep=",", low_memory=False)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{arquivo_original}' não encontrado.")
        return False

    # Lógica de limpeza do seu script
    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.duplicated()]

    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    colunas_validas = [
        c for c in df.columns if df[c].dropna().isin([1, 2, 3, 4, 5]).any()
    ]
    df_limpo = df[colunas_validas].copy()
    df_limpo = df_limpo.dropna(how="all")
    df_limpo = df_limpo.reset_index(drop=True)

    df_limpo.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")
    print(f"Dados limpos salvos em '{arquivo_saida}'.")
    return True


def executar_cronbach():
    """
    Executa a análise de Alpha de Cronbach.
    """
    print("--- 2. Análise de Confiabilidade (Alpha de Cronbach) ---")
    try:
        # Chama a função importada de 'cronbach_alpha.py'
        processar_csv_cronbach("respostas_formatadas.csv")
    except Exception as e:
        print(f"Erro ao executar análise Cronbach: {e}")
    print("-" * 40 + "\n")


def executar_correlacao():
    """
    Executa a análise de Correlação de Pearson.
    (Usa as funções de 'correlacao.py' para mostrar a classificação)
    """
    print("--- 3. Análise de Correlação (Pearson) ---")
    arquivo_entrada = "respostas_formatadas.csv"
    num_pares_mostrar = 5

    try:
        df = pd.read_csv(arquivo_entrada)

        # Cria a legenda (como no seu script original)
        colunas_originais = df.columns.tolist()
        colunas_curtas = [f"Item {i+1}" for i in range(len(colunas_originais))]
        legenda = {c: l for c, l in zip(colunas_curtas, colunas_originais)}

        df_renomeado = df.copy()
        df_renomeado.columns = colunas_curtas

        # Chama a função importada de 'correlacao.py'
        matriz_corr, top_pos, top_neg = analisar_correlacao_pearson(
            df_renomeado, colunas=None, num_pares=num_pares_mostrar
        )

        # Imprime os resultados de forma limpa
        print(f"\n--- Top {num_pares_mostrar} Pares Positivos ---")
        top_pos_df = top_pos.reset_index()
        top_pos_df.columns = ["Item A", "Item B", "Correlacao"]
        # --- Adiciona a classificação ---
        top_pos_df["Classificacao"] = top_pos_df["Correlacao"].apply(
            classificar_correlacao
        )
        print(top_pos_df.to_string(float_format="%.2f", index=False))

        print(f"\n--- Top {num_pares_mostrar} Pares Negativos ---")
        top_neg_df = top_neg.reset_index()
        top_neg_df.columns = ["Item A", "Item B", "Correlacao"]
        top_neg_df["Classificacao"] = top_neg_df["Correlacao"].apply(
            classificar_correlacao
        )
        print(top_neg_df.to_string(float_format="%.2f", index=False))

        print("\n--- Legenda dos Itens ---")
        for item, descricao in legenda.items():
            print(f"{item}: {descricao}")

    except Exception as e:
        print(f"Erro ao executar análise de Correlação: {e}")
    print("-" * 40 + "\n")


# --- 3. Execução Principal ---


def main():
    """
    Função principal que orquestra todas as etapas.
    (Com saídas de console mais claras)
    """

    print("\n" + "=" * 50)
    print("   INICIANDO SCRIPT DE ANÁLISE DE DADOS")
    print("=" * 50 + "\n")

    # Etapa 1: Formatar
    if executar_formatacao():

        print("\n" + "=" * 50)
        print("   INICIANDO ANÁLISES ESTATÍSTICAS")
        print("=" * 50 + "\n")

        # Etapa 2: Rodar Cronbach
        executar_cronbach()

        # Etapa 3: Rodar Correlação
        executar_correlacao()

        print("=" * 50)
        print("   === ANÁLISES CONCLUÍDAS === ")
        print("=" * 50 + "\n")

    else:
        print("\n" + "=" * 50)
        print("   ERRO NA FORMATAÇÃO. O SCRIPT FOI INTERROMPIDO.")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    main()

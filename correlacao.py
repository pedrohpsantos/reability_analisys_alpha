import pandas as pd
import numpy as np
from typing import List, Optional, Tuple


def analisar_correlacao_pearson(
    df: pd.DataFrame, colunas: Optional[List[str]] = None, num_pares: int = 5
) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Calcula a matriz de correlação de Pearson e encontra os pares
    mais correlacionados (positiva e negativamente).

    Args:
        df (pd.DataFrame): DataFrame com os dados.
        colunas (Optional[List[str]]): Lista de colunas para usar. Se None, usa todas as numéricas.
        num_pares (int): O número de pares para retornar (top positivos e top negativos).

    Returns:
        Tuple[pd.DataFrame, pd.Series, pd.Series]:
            1. A matriz de correlação completa.
            2. Uma série com os 'num_pares' mais correlacionados positivamente.
            3. Uma série com os 'num_pares' mais correlacionados negativamente.
    """
    if colunas:
        df_analise = df[colunas].copy()
    else:
        # Se nenhuma coluna for especificada, usa todas que forem numéricas
        df_analise = df.select_dtypes(include=[np.number]).copy()

    # Correlação não funciona com valores ausentes
    df_analise = df_analise.dropna(how="any")

    if df_analise.shape[1] < 2:
        raise ValueError("A análise de correlação requer pelo menos 2 itens (colunas).")

    # --- 1. Calcular a Matriz de Correlação ---
    matriz_corr = df_analise.corr(method="pearson")

    # --- 2. Preparar Pares ---

    # Mascarar o triângulo superior (para evitar duplicatas) e a diagonal (k=0)
    mask = np.triu(np.ones(matriz_corr.shape, dtype=bool), k=0)
    corr_sem_duplicatas = matriz_corr.mask(mask)

    # Empilhar (stack) para transformar de matriz para uma série de pares (MultiIndex)
    corr_pares = corr_sem_duplicatas.stack()

    # --- 3. Encontrar Top Pares Positivos e Negativos ---

    # Top Positivos: Ordena do maior para o menor
    top_positivos = corr_pares.sort_values(ascending=False).head(num_pares)

    # Top Negativos: Ordena do menor para o maior
    top_negativos = corr_pares.sort_values(ascending=True).head(num_pares)

    # Retorna os três resultados
    return matriz_corr, top_positivos, top_negativos


# --- Função para classificação ---
def classificar_correlacao(r: float) -> str:
    """Classifica a força e direção de um coeficiente de correlação 'r'."""
    abs_r = abs(r)

    if abs_r >= 0.9:
        forca = "Muito Forte"
    elif abs_r >= 0.7:
        forca = "Forte"
    elif abs_r >= 0.4:
        forca = "Moderada"
    elif abs_r >= 0.2:
        forca = "Fraca"
    else:
        forca = "Muito Fraca"

    if r > 0:
        return f"Positiva {forca}"
    elif r < 0:
        return f"Negativa {forca}"
    else:
        return "Nula"


# --- Bloco de Execução Principal (Com formatação limpa e legenda) ---
if __name__ == "__main__":

    print("Executando Análise de Correlação de Pearson...")

    arquivo_entrada = "respostas_formatadas.csv"

    try:
        # 1. Carregar o arquivo
        df = pd.read_csv(arquivo_entrada)

        # 2. Criar a legenda e os nomes curtos
        colunas_originais = df.columns.tolist()
        colunas_curtas = [f"Item {i+1}" for i in range(len(colunas_originais))]
        legenda = {
            col_curta: col_longa
            for col_curta, col_longa in zip(colunas_curtas, colunas_originais)
        }

        # 3. Renomear o DataFrame para análise
        df_renomeado = df.copy()
        df_renomeado.columns = colunas_curtas

        # 4. Definir quantos top pares mostrar
        num_pares_mostrar = 5

        # 5. Executar a análise no DataFrame renomeado
        matriz_corr, top_pos, top_neg = analisar_correlacao_pearson(
            df_renomeado, colunas=None, num_pares=num_pares_mostrar
        )

        # 6. Mostrar os resultados

        # --- Tabela de Pares POSITIVOS ---
        print(
            f"\n--- Top {num_pares_mostrar} Pares Mais Correlacionados (Positivos) ---"
        )
        top_pos_df = top_pos.reset_index()
        top_pos_df.columns = ["Item A", "Item B", "Correlacao"]
        top_pos_df["Classificacao"] = top_pos_df["Correlacao"].apply(
            classificar_correlacao
        )
        print(top_pos_df.to_string(float_format="%.2f", index=False))

        # --- Tabela de Pares NEGATIVOS ---
        print(
            f"\n--- Top {num_pares_mostrar} Pares Mais Correlacionados (Negativos) ---"
        )
        top_neg_df = top_neg.reset_index()
        top_neg_df.columns = ["Item A", "Item B", "Correlacao"]
        # ADICIONA A CLASSIFICAÇÃO
        top_neg_df["Classificacao"] = top_neg_df["Correlacao"].apply(
            classificar_correlacao
        )
        print(top_neg_df.to_string(float_format="%.2f", index=False))

        # --- Matriz Completa ---
        print("\n--- Matriz de Correlação Completa ---")
        print(matriz_corr.round(2).to_string())

        # --- Legenda ---
        print("\n--- Legenda dos Itens ---")
        for item, descricao in legenda.items():
            print(f"{item}: {descricao}")

        print("\nAnálise concluída.")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado.")
        print("Por favor, certifique-se que o arquivo está no mesmo diretório.")
    except ValueError as ve:
        print(f"Erro na análise: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

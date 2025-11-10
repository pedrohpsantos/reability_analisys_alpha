import pandas as pd
import numpy as np
from typing import Union, List, Optional


# -----------------------------------------------
# FUNÇÃO PRINCIPAL - Cálculo do Alpha de Cronbach
# -----------------------------------------------


def calcular_alpha_cronbach_detalhado(
    dados: Union[pd.DataFrame, np.ndarray, List[List]],
    colunas_escala: Optional[List[str]] = None,
):
    if isinstance(dados, (np.ndarray, list)):
        dados = pd.DataFrame(dados)
    elif not isinstance(dados, pd.DataFrame):
        raise ValueError("Os dados devem ser um DataFrame, numpy array ou lista")

    if colunas_escala:
        df = dados[colunas_escala].copy()
    else:
        df = dados.select_dtypes(include=[np.number]).copy()

    df = df.dropna()

    X = df.values
    k = X.shape[1]

    # Variâncias individuais dos itens (Será usado na tabela)
    variancias = np.var(X, axis=0, ddof=1)

    # Variância da soma total dos scores
    var_total = np.var(np.sum(X, axis=1), ddof=1)

    # Cálculo do Alpha
    alpha = (k / (k - 1)) * (1 - (np.sum(variancias) / var_total))

    # Lista para guardar o "Alpha se o item for deletado"
    alphas_sem_item = []

    for i in range(k):
        # --- Cálculo do Alpha se o item 'i' for deletado ---

        # Cria uma view do array X sem a coluna 'i'
        X_sem_item = np.delete(X, i, axis=1)

        # Variâncias dos itens restantes
        variancias_itens_sem = np.var(X_sem_item, axis=0, ddof=1)

        # Variância da soma dos scores dos itens restantes
        soma_variancia_sem = np.var(np.sum(X_sem_item, axis=1), ddof=1)

        # Número de itens restantes
        k_sem_item = k - 1

        # Calcula o Alpha para o subconjunto de itens
        alpha_sem = ((k_sem_item) / (k_sem_item - 1)) * (
            1 - (np.sum(variancias_itens_sem) / soma_variancia_sem)
        )
        alphas_sem_item.append(alpha_sem)

    # Compila o DataFrame de estatísticas
    estatisticas = pd.DataFrame(
        {
            "Média": np.mean(X, axis=0),
            "Desvio_Padrão": np.std(X, axis=0, ddof=1),
            "Variância": variancias,
            "Alpha_se_Deletado": alphas_sem_item,
        }
    )

    estatisticas = estatisticas.set_index(pd.Index([f"Item {i+1}" for i in range(k)]))
    return alpha, estatisticas


# -------------------------------------------
# CLASSIFICAÇÃO DO VALOR DE ALPHA
# -------------------------------------------


def classificar_alpha(alpha: float) -> str:
    if alpha >= 0.95:
        return "Excelente (possível redundância)"
    elif alpha >= 0.90:
        return "Excelente"
    elif alpha >= 0.80:
        return "Boa"
    elif alpha >= 0.70:
        return "Aceitável"
    elif alpha >= 0.60:
        return "Questionável"
    elif alpha >= 0.50:
        return "Fraca"
    else:
        return "Inaceitável"


# -------------------------------------------
# EXECUÇÃO DETALHADA - SAÍDA LIMPA
# -------------------------------------------


def processar_csv_cronbach(caminho_csv: str, colunas: Optional[List[str]] = None):
    df = pd.read_csv(caminho_csv)
    alpha, estatisticas = calcular_alpha_cronbach_detalhado(df, colunas)
    classificacao = classificar_alpha(alpha)

    print(f"Alpha de Cronbach: {alpha:.2f}")
    print(f"Classificação: {classificacao}\n")
    print("--- Estatísticas dos Itens ---")
    print(estatisticas.round(2))


# -------------------------------------------
# EXECUÇÃO
# -------------------------------------------

if __name__ == "__main__":
    caminho_arquivo = "respostas_formatadas.csv"

    try:
        processar_csv_cronbach(caminho_arquivo)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

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
    variancias = np.var(X, axis=0, ddof=1)
    var_total = np.var(np.sum(X, axis=1), ddof=1)
    alpha = (k / (k - 1)) * (1 - (np.sum(variancias) / var_total))

    correlacoes_item_total = []
    alphas_sem_item = []

    for i in range(k):
        item = X[:, i]
        total_sem_item = np.sum(np.delete(X, i, axis=1), axis=1)
        correl = np.corrcoef(item, total_sem_item)[0, 1]
        correlacoes_item_total.append(correl)

        variancias_itens_sem = np.var(np.delete(X, i, axis=1), axis=0, ddof=1)
        soma_variancia_sem = np.var(np.sum(np.delete(X, i, axis=1), axis=1), ddof=1)
        alpha_sem = ((k - 1) / (k - 2)) * (
            1 - (np.sum(variancias_itens_sem) / soma_variancia_sem)
        )
        alphas_sem_item.append(alpha_sem)

    estatisticas = pd.DataFrame(
        {
            "Média": np.mean(X, axis=0),
            "Desvio_Padrão": np.std(X, axis=0, ddof=1),
            "Correlação_Item_Total": correlacoes_item_total,
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
    print(estatisticas.round(2))


# -------------------------------------------
# EXECUÇÃO
# -------------------------------------------

if __name__ == "__main__":
    caminho_arquivo = "respostas_formatadas.csv"
    processar_csv_cronbach(caminho_arquivo)

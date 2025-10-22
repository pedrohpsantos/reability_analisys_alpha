import pandas as pd

# Caminho do arquivo bruto
arquivo_original = "respostas.csv"

# Lê o CSV (usa encoding e tratamento de colunas)
df = pd.read_csv(arquivo_original, encoding="utf-8", sep=",", low_memory=False)

print("=== Limpeza iniciada ===")
print(f"Linhas originais: {len(df)} | Colunas originais: {len(df.columns)}")

# Remove colunas 100% vazias
df = df.dropna(axis=1, how="all")

# Remove linhas completamente vazias
df = df.dropna(how="all")

# Remove colunas duplicadas (mesmo nome repetido)
df = df.loc[:, ~df.columns.duplicated()]

# Converte todas as possíveis colunas em números (ignora texto, datas, consentimento etc.)
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Mantém apenas colunas com pelo menos alguns valores válidos (entre 1 e 5)
colunas_validas = [c for c in df.columns if df[c].dropna().isin([1, 2, 3, 4, 5]).any()]
df_limpo = df[colunas_validas].copy()

# Remove linhas sem respostas válidas
df_limpo = df_limpo.dropna(how="all")

# Reseta o índice
df_limpo = df_limpo.reset_index(drop=True)

print(f"Colunas mantidas após limpeza: {len(df_limpo.columns)}")
print(f"Linhas mantidas após limpeza: {len(df_limpo)}")

# Salva o novo arquivo limpo
arquivo_saida = "respostas_formatadas.csv"
df_limpo.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

print("\nArquivo limpo salvo como 'respostas_formatadas.csv'.")
print("Agora o arquivo está pronto para o cálculo do Alpha de Cronbach.")

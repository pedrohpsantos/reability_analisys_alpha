# Reliability Analysis Alpha

Um conjunto de ferramentas Python para análise de confiabilidade usando o Alpha de Cronbach, especialmente projetado para análise de questionários e escalas psicométricas.

## 📋 Sobre o Projeto

Este projeto fornece uma implementação completa e detalhada do cálculo do Alpha de Cronbach, incluindo:
- Cálculo do coeficiente de confiabilidade
- Análise item por item
- Classificação automática da confiabilidade
- Pré-processamento de dados de questionários

## 🚀 Funcionalidades

### Principais Features:
- **Cálculo detalhado do Alpha de Cronbach** com estatísticas completas
- **Classificação automática** da confiabilidade (Excelente, Boa, Aceitável, etc.)
- **Análise item por item** incluindo correlações item-total
- **Sugestões de melhoria** através do "Alpha se deletado"
- **Limpeza automática de dados** para questionários

### Estatísticas Fornecidas:
- Média e desvio padrão por item
- Correlação item-total
- Alpha de Cronbach se o item fosse removido
- Classificação da confiabilidade

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pedrohpsantos/reability_analisys_alpha.git
cd reability_analisys_alpha
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Uso Básico

```python
from cronbach_alpha import calcular_alpha_cronbach_detalhado, classificar_alpha
import pandas as pd

# Carregue seus dados
df = pd.read_csv('seus_dados.csv')

# Calcule o Alpha de Cronbach
alpha, estatisticas = calcular_alpha_cronbach_detalhado(df)

# Veja o resultado
print(f"Alpha de Cronbach: {alpha:.3f}")
print(f"Classificação: {classificar_alpha(alpha)}")
print("\nEstatísticas por item:")
print(estatisticas)
```

### Processamento de Questionários

1. **Prepare seus dados**: Coloque o arquivo CSV com as respostas como `respostas.csv`

2. **Execute a limpeza dos dados**:
```bash
python formatar_respostas.py
```

3. **Calcule o Alpha de Cronbach**:
```bash
python cronbach_alpha.py
```

### Exemplo de Uso com Colunas Específicas

```python
# Para analisar apenas colunas específicas
colunas_escala = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
alpha, stats = calcular_alpha_cronbach_detalhado(df, colunas_escala)
```

## 📊 Interpretação dos Resultados

### Classificação do Alpha de Cronbach:
- **≥ 0.95**: Excelente (possível redundância)
- **≥ 0.90**: Excelente
- **≥ 0.80**: Boa
- **≥ 0.70**: Aceitável
- **≥ 0.60**: Questionável
- **≥ 0.50**: Fraca
- **< 0.50**: Inaceitável

### Como Interpretar as Estatísticas:
- **Correlação Item-Total**: Valores baixos (< 0.30) podem indicar itens problemáticos
- **Alpha se Deletado**: Se for maior que o Alpha geral, considere remover o item

## 📁 Estrutura do Projeto

```
reability_analisys_alpha/
├── cronbach_alpha.py      # Módulo principal com cálculos do Alpha
├── formatar_respostas.py  # Script para limpeza de dados
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

## 🔧 Dependências

- `pandas`: Manipulação de dados
- `numpy`: Cálculos numéricos
- `typing-extensions`: Tipagem estática

## 📋 Formato dos Dados

O script `formatar_respostas.py` espera:
- Arquivo CSV com respostas em escala Likert (1-5)
- Primeira linha com cabeçalhos
- Encoding UTF-8

O script automaticamente:
- Remove colunas e linhas vazias
- Converte dados para numérico
- Filtra apenas respostas válidas (1-5)
- Remove duplicatas

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**Pedro Santos** - [pedrohpsantos](https://github.com/pedrohpsantos)

---

*Desenvolvido para facilitar análises de confiabilidade em pesquisas acadêmicas e profissionais.*
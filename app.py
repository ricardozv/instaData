# app.py
import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Função para carregar os dados do JSON
def load_data():
    with open('data/instagram_posts.json', 'r') as f:
        posts_data = json.load(f)
    return posts_data

# Função para calcular a taxa de engajamento
def calculate_engagement_rate(df, followers):
    df['engagement_rate'] = (df['likes'] + df['comments']) / followers * 100
    return df

# Carregar os dados
posts_data = load_data()

# Criar DataFrame
df = pd.DataFrame(posts_data)

# Converter a coluna de datas para datetime
df['date'] = pd.to_datetime(df['date'])

# Calcular a taxa de engajamento
followers_count = 5046
df = calculate_engagement_rate(df, followers_count)

# Configurar a página do Streamlit
st.title('Dashboard de Análise do Instagram')

# Análise Descritiva
st.header('Análise Descritiva')
descriptive_stats = df[['likes', 'comments', 'engagement_rate']].describe()
descriptive_stats = descriptive_stats.rename(index={
    'count': 'Contagem',
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Mínimo',
    '25%': '25%',
    '50%': 'Mediana',
    '75%': '75%',
    'max': 'Máximo'
})
descriptive_stats.columns = ['Curtidas', 'Comentários', 'Taxa de Engajamento']

# Exibir estatísticas descritivas
st.write(descriptive_stats.drop(index='Contagem'))

# Explicação dos Dados
st.markdown("### Explicação dos Dados")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **Curtidas**: Número médio de curtidas que cada postagem recebeu.
    - **Comentários**: Número médio de comentários que cada postagem recebeu.
    - **Taxa de Engajamento**: Proporção média de interações (curtidas + comentários) em relação ao número de seguidores, expressa em porcentagem.
    - **Desvio Padrão**: Medida da variação ou dispersão das curtidas, comentários e taxa de engajamento.
    """)

with col2:
    st.markdown("""
    - **Mínimo**: Menor valor registrado para curtidas, comentários e taxa de engajamento.
    - **25%**: Valor abaixo do qual 25% das observações podem ser encontradas.
    - **Mediana (50%)**: Valor central que separa a metade superior da metade inferior dos dados.
    - **75%**: Valor abaixo do qual 75% das observações podem ser encontradas.
    - **Máximo**: Maior valor registrado para curtidas, comentários e taxa de engajamento.
    """)

# Análise de Engajamento
st.header('Análise de Engajamento')
st.line_chart(df.set_index('date')['engagement_rate'])

# Explicação do gráfico de taxa de engajamento
st.markdown("""
### Explicação do Gráfico de Engajamento

O gráfico de linha acima mostra a variação da taxa de engajamento ao longo do tempo. A taxa de engajamento é calculada como a soma das curtidas e comentários de uma postagem, dividida pelo número total de seguidores, e multiplicada por 100 para expressar o valor em porcentagem. Esse gráfico ajuda a identificar padrões de engajamento, como picos e quedas, e pode fornecer insights sobre quais tipos de postagens ou momentos de publicação geram mais interação.
""")

# Análise Temporal
st.header('Análise Temporal')
df['hour'] = df['date'].dt.hour
df['weekday'] = df['date'].dt.weekday

st.subheader('Taxa de Engajamento por Hora do Dia')
engagement_by_hour = df.groupby('hour')['engagement_rate'].mean()
st.line_chart(engagement_by_hour)

st.subheader('Taxa de Engajamento por Dia da Semana')
engagement_by_weekday = df.groupby('weekday')['engagement_rate'].mean()
engagement_by_weekday.index = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
engagement_by_weekday = engagement_by_weekday.reindex(['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'])
st.bar_chart(engagement_by_weekday)

# Explicação do gráfico de taxa de engajamento por dia da semana
st.markdown("""
### Explicação do Gráfico de Taxa de Engajamento por Dia da Semana

O gráfico acima mostra a taxa de engajamento média das postagens em cada dia da semana. A taxa de engajamento é calculada como a soma das curtidas e comentários de uma postagem, dividida pelo número total de seguidores, e multiplicada por 100 para expressar o valor em porcentagem. Esse gráfico ajuda a identificar quais dias da semana têm maior ou menor engajamento, permitindo ajustar a estratégia de postagem para maximizar a interação.
""")

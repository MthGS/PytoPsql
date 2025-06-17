import streamlit as st
import pandas as pd
import sqlalchemy
from urllib.parse import quote_plus

# Configuração da página
st.set_page_config(
    page_title="Análise de Times",
    page_icon="🏟️",
    layout="wide"
)

# --- Funções de Conexão e Carga de Dados (pode ser copiado do seu app.py) ---
# O cache do Streamlit é inteligente e compartilhará os dados entre as páginas
@st.cache_resource
def init_connection():
    db_url = st.secrets["postgres"]
    password_encoded = quote_plus(db_url['password'])
    connection_str = (
        f"postgresql+psycopg2://{db_url['user']}:{password_encoded}"
        f"@{db_url['host']}:{db_url['port']}/{db_url['dbname']}"
    )
    return sqlalchemy.create_engine(connection_str)

@st.cache_data(ttl=600)
def load_data(_engine):
    query = 'SELECT * FROM testecap1.all_players ORDER BY "Rank" ASC;'
    return pd.read_sql(query, _engine)

# --- Início da Página ---
st.title("🏟️ Análise de Times")

# Carrega todos os dados uma única vez
engine = init_connection()
df_players = load_data(engine)

if not df_players.empty:
    # 1. PEGAR A LISTA DE TIMES ÚNICOS (MÁGICA DO PANDAS)
    # Ordenamos a lista de times alfabeticamente
    teams = sorted(df_players["Team"].unique())
    
    # 2. CRIAR UM FILTRO PARA O USUÁRIO SELECIONAR UM TIME
    selected_team = st.selectbox("Selecione um time para ver os jogadores:", teams)
    
    # 3. FILTRAR O DATAFRAME COM BASE NA SELEÇÃO
    df_filtered = df_players[df_players["Team"] == selected_team]
    
    # 4. EXIBIR OS RESULTADOS
    st.header(f"Jogadores do {selected_team}")
    
    # Exibe a tabela apenas com as colunas mais importantes para esta visualização
    columns_to_show = ["Rank", "Name", "OVR", "Position", "Age", "Nation"]
    st.dataframe(df_filtered[columns_to_show], use_container_width=True, hide_index=True)
else:
    st.error("Não foi possível carregar os dados. Verifique a conexão.")

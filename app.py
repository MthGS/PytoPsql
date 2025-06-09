import streamlit as st
import pandas as pd
import sqlalchemy
from urllib.parse import quote_plus # Importa a função necessária

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Dashboard de Jogadores FC 24",
    page_icon="⚽",
    layout="wide"
)

# Função para inicializar a conexão com o banco de dados.
# Usa o sistema de "Secrets" do Streamlit para obter as credenciais de forma segura.
# Utiliza o cache para que a conexão seja criada apenas uma vez.
@st.cache_resource
def init_connection():
    """
    Inicializa a conexão com o banco de dados PostgreSQL.
    Retorna um objeto de conexão do SQLAlchemy.
    """
    try:
        # Monta a string de conexão usando os segredos
        db_url = st.secrets["postgres"]

        # Codifica a senha para lidar com caracteres especiais (como @, #, :)
        password_encoded = quote_plus(db_url['password'])

        connection_str = (
            f"postgresql+psycopg2://{db_url['user']}:{password_encoded}"
            f"@{db_url['host']}:{db_url['port']}/{db_url['dbname']}"
        )
        engine = sqlalchemy.create_engine(connection_str)
        return engine
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para carregar os dados da tabela 'all_players'.
# Usa o cache para que os dados sejam carregados apenas uma vez, tornando a app rápida.
@st.cache_data(ttl=600)  # TTL (Time to Live) de 10 minutos
def load_data(_engine):
    """
    Carrega os dados da tabela all_players do schema testecap1.
    Retorna um DataFrame do Pandas.
    """
    if _engine is not None:
        try:
            query = 'SELECT * FROM testecap1.all_players ORDER BY "Rank" ASC;'
            df = pd.read_sql(query, _engine)
            return df
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
            return pd.DataFrame() # Retorna um DataFrame vazio em caso de erro
    return pd.DataFrame()

# --- Início da Aplicação ---

st.title("⚽ Dashboard de Jogadores - EA FC 24")
st.markdown("Dados carregados diretamente do banco de dados PostgreSQL.")

# Inicializa a conexão
engine = init_connection()

# Se a conexão for bem-sucedida, carrega e exibe os dados
if engine:
    df_players = load_data(engine)
    
    if not df_players.empty:
        st.success("Conexão com o banco de dados estabelecida e dados carregados com sucesso!")
        
        # Exibe o DataFrame na tela
        st.dataframe(df_players, use_container_width=True)
        st.info(f"Total de {len(df_players)} jogadores carregados.")
    else:
        st.warning("Nenhum dado foi retornado do banco de dados. A tabela pode estar vazia.")
else:
    st.error("Não foi possível estabelecer conexão com o banco de dados. Verifique as credenciais no arquivo 'secrets.toml' e se o servidor PostgreSQL está acessível.")


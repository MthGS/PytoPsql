import sqlalchemy
from urllib.parse import quote_plus
import pandas as pd

# --- COLOQUE SUAS CREDENCIAIS AQUI ---
DB_USER = "postgres"
DB_PASSWORD_RAW = "abc@123" # Senha original
DB_HOST = "127.0.0.1" # ou o host público, se estiver na nuvem
DB_PORT = 5432
DB_NAME = "teste_database"
# ----------------------------------------

try:
    print("Tentando conectar ao banco de dados...")

    # Codifica a senha, caso ela tenha caracteres especiais
    password_encoded = quote_plus(DB_PASSWORD_RAW)

    connection_str = (
        f"postgresql+psycopg2://{DB_USER}:{password_encoded}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = sqlalchemy.create_engine(connection_str)

    with engine.connect() as connection:
        print("Conexão estabelecida com sucesso!")

        # Testa a leitura de dados
        print("Tentando carregar dados da tabela...")
        query = 'SELECT * FROM testecap1.all_players LIMIT 5;' # Pega só 5 linhas para testar
        df = pd.read_sql(query, connection)
        print("Dados carregados com sucesso!")
        print(df.head())

except Exception as e:
    print("\n--- FALHA NA CONEXÃO ---")
    print(f"Ocorreu um erro: {e}")
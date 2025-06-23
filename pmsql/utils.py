import psycopg2 # type: ignore

def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = psycopg2.connect(
            dbname='',
            host='',
            user='',
            password='',
        )
        return conn
    except Exception as e:
        print(f'Erro ao conectar ao servidor: {e}')
        return None


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()
        print('Desconectado do servidor.')


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos;')
    produtos = cursor.fetchall()

    if len(produtos) > 0:
        print('Listando produtos...')
        print('===================')
        for produto in produtos:
            print(f'ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Estoque: {produto[3]}')
            print('-------------------')
    else:
        print('Nenhum produto encontrado.')
    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    cursor = conn.cursor()
    nome = input('Digite o nome do produto: ')
    preco = float(input('Digite o preço do produto: '))
    estoque = int(input('Digite a quantidade em estoque: '))
    cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque})")
    conn.commit()
##rowcount é o número de linhas afetadas pela última operação
    if cursor.rowcount == 1:
        print(f'Produto {nome} foi inserido com sucesso!')
    else:
        print('Erro ao inserir o produto.')
    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    cursor = conn.cursor()

    id_produto = int(input('Digite o ID do produto a ser atualizado: '))
    nome = input('Digite o novo nome do produto: ')
    preco = float(input('Digite o novo preço do produto: '))
    estoque = int(input('Digite a nova quantidade em estoque: '))
    cursor.execute(f"UPDATE produtos SET nome = '{nome}', preco = {preco}, estoque = {estoque} WHERE id = {id_produto}")
    conn.commit()

    if cursor.rowcount == 1:
        print(f'Produto {nome} com ID {id_produto} foi atualizado com sucesso!')
    else:
        print('Erro ao atualizar o produto. Verifique se o ID existe.')
    desconectar(conn)


def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()
    cursor = conn.cursor()

    id_produto = int(input('Digite o ID do produto a ser deletado: '))
    cursor.execute(f"DELETE FROM produtos WHERE id = {id_produto}")
    conn.commit()
    if cursor.rowcount == 1:
        print(f'Produto com ID {id_produto} foi deletado com sucesso!')
    else:
        print('Erro ao deletar o produto. Verifique se o ID existe.')
    desconectar(conn)


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')


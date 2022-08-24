from infra.config import DBConnectionHandler

def atualiza_preco_venda_db(moeda, valor):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'UPDATE preco_venda SET preco_venda = {valor} WHERE Currency = "{moeda}"')
        db_conn.commit()
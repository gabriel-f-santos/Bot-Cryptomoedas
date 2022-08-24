from infra.config import DBConnectionHandler

def atualiza_preco_compra_db(moeda, valor):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'UPDATE preco_compra SET preco_compra = {valor} WHERE Currency = "{moeda}"')
        db_conn.commit()
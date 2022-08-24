from infra.config import DBConnectionHandler

def atualiza_rentabilidade_db(moeda, rentabilidade):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'UPDATE rentabilidade SET rentabilidade = {rentabilidade} WHERE Currency = "{moeda}"')
        db_conn.commit()
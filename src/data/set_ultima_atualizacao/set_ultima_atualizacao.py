from infra.config import DBConnectionHandler

def atualiza_posicao(moeda, open=True):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'UPDATE position SET position = {open} WHERE Currency = "{moeda}"')
        db_conn.commit()
from infra.config import DBConnectionHandler

def get_preco_compra_db(moeda):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'SELECT preco_compra FROM preco_compra WHERE Currency = "{moeda}" ORDER BY market_date DESC limit 1')
        pos = cursor.fetchone()
        if pos == 'None' or pos == None:
            cursor.execute(f'INSERT INTO preco_compra (Currency, preco_compra) VALUES ("{moeda}", {0})')
            db_conn.commit()
            pos = 0
        return float(pos)
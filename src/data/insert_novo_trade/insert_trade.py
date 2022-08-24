from infra.config import DBConnectionHandler

def insert_trade_db(moeda, quantidade, side, preco):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        db_order = f'''INSERT INTO orders (Currency, quantity, market, price) 
                VALUES("{moeda}",{quantidade},"{side}",{preco})'''
        cursor.execute(db_order)
        db_conn.commit()
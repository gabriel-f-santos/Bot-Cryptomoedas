from infra.config import DBConnectionHandler

replace = ['(',')',',','./data/','csv','.','[',']']
replace_number = ['(',')',',','[',']']

def clean_up_sql_out(text,isnumber):
    if isnumber == 1:
        for s in replace_number:
            text = str(text).replace(s,'')      
    else:
        for s in replace:
            text = str(text).replace(s,'')
    return text

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
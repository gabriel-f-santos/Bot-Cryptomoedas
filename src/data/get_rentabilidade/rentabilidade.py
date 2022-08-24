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

def get_rentabilidade_db(moeda):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'SELECT rentabilidade FROM rentabilidade WHERE Currency = "{moeda}" ORDER BY market_date DESC limit 1')
        pos = cursor.fetchone()
        pos = clean_up_sql_out(pos,0)
        if pos == 'None' or pos == None:
            cursor.execute(f'INSERT INTO rentabilidade (Currency, rentabilidade) VALUES ("{moeda}", {0})')
            db_conn.commit()
            pos = 0
        return float(pos)
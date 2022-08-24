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

def get_posicao(moeda):
    with DBConnectionHandler() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(f'SELECT position FROM position WHERE Currency = "{moeda}" ORDER BY market_date DESC limit 1')
        pos = cursor.fetchone()
        print(f"pos {pos}")
        pos = clean_up_sql_out(pos,0)
        if pos == 'None' or pos == None:
            cursor.execute(f'INSERT INTO position (Currency, position) VALUES ("{moeda}",False)')
            pos = False
            db_conn.commit()
        return int(pos)
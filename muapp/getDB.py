import sqlite3


def get_db():# 
    
    conn = sqlite3.connect('./db.sqlite3') # SQLite 데이터베이스 연결  
    cursor = conn.cursor() # 커서 생성
    query = f"SELECT * FROM muapp_clothes" # SQL 쿼리 작성
    cursor.execute(query) # 쿼리 실행
    data = cursor.fetchall() # 결과 가져오기 [('경기도', '화성시', '봉담읍')]
    #res_loc = f"{address[0][0]} {address[0][1]}" #경기도 화성시
    conn.close() # 연결 닫기

    return data

print(get_db())

def get_clothes_list():
    data = get_db()
    clothes_list=[]

    for i in range(len(data)):
        clothes_list.append({
            'img' : data[i][7],
            'type' : data[i][1]  + " / " + data[i][2],
            'name' : data[i][5],
            'upload_date' : data[i][6],
        })

        
    return clothes_list

print(get_clothes_list())
import requests
import json
import datetime,math, sqlite3

def dfsXyConv(code, v1, v2): 
    PI, tan, log, cos, pow, floor, sin, sqrt, atan, atan2 = math.pi, math.tan, math.log, math.cos, math.pow, math.floor, math.sin, math.sqrt, math.atan, math.atan2

    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0  # 격자 간격(km)
    SLAT1 = 30.0  # 투영 위도1(degree)
    SLAT2 = 60.0  # 투영 위도2(degree)
    OLON = 126.0  # 기준점 경도(degree)
    OLAT = 38.0  # 기준점 위도(degree)
    XO = 43  # 기준점 X좌표(GRID)
    YO = 136  # 기준점 Y좌표(GRID)

    DEGRAD = PI / 180.0
    RADDEG = 180.0 / PI

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = tan(PI * 0.25 + slat2 * 0.5) / tan(PI * 0.25 + slat1 * 0.5)
    sn = log(cos(slat1) / cos(slat2)) / log(sn)
    sf = tan(PI * 0.25 + slat1 * 0.5)
    sf = pow(sf, sn) * cos(slat1) / sn
    ro = tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / pow(ro, sn)

    rs = {}
    if code == 'toXY':
        rs['lat'] = v1
        rs['lon'] = v2
        ra = tan(PI * 0.25 + (v1) * DEGRAD * 0.5)
        ra = re * sf / pow(ra, sn)
        theta = v2 * DEGRAD - olon
        if theta > PI:
            theta -= 2.0 * PI
        if theta < -PI:
            theta += 2.0 * PI
        theta *= sn
        rs['x'] = floor(ra * sin(theta) + XO + 0.5)
        rs['y'] = floor(ro - ra * cos(theta) + YO + 0.5)
    else:
        rs['x'] = v1
        rs['y'] = v2
        xn = v1 - XO
        yn = ro - v2 + YO
        ra = sqrt(xn * xn + yn * yn)
        if sn < 0.0:
            ra = -ra
        alat = pow((re * sf / ra), (1.0 / sn))
        alat = 2.0 * atan(alat) - PI * 0.5
        if abs(xn) <= 0.0:
            theta = 0.0
        else:
            if (abs(yn) <= 0.0) :
                theta = PI * 0.5
                if (xn < 0.0): theta = -theta
                else: theta = atan2(xn, yn)
        alon = theta / sn + olon
        rs.lat = alat * RADDEG
        rs.lon = alon * RADDEG
    return rs

    # module.exports = {
    #   toXY: (lat, lon) => dfsXyConv('toXY', lat, lon),
    #   fromXY: (x, y) => dfsXyConv('latlon', x, y)
    # }

def get_loc_api_data(): #현재 위치 가져오는 구글API, IP를 기준으로 가져옴.
    loc_serviceKey = 'AIzaSyC7VJJjA3IZGewIvQ5uSzUxpqQwfqoxjxI'
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={loc_serviceKey}"
    options = {'considerIp': True,}
    response = requests.post(url,options)
    data = response.json()
    return data['location']



def get_loc_data():# 현재 위치를 바탕으로 db에서 주소 이름 찾는 코드
    lat = get_loc_api_data()['lat']
    lng = get_loc_api_data()['lng']
    rs = dfsXyConv('toXY', lat, lng)
    X,Y = rs['x'],rs['y']

    
    conn = sqlite3.connect('D:\grad-job\django\db.sqlite3') # SQLite 데이터베이스 연결    *** 경로 수정해야함!!!!! 
    cursor = conn.cursor() # 커서 생성
    query = f"SELECT address1, address2, address3 FROM weather_api WHERE gridX = {X} and gridY = {Y}" # SQL 쿼리 작성
    cursor.execute(query) # 쿼리 실행
    results = cursor.fetchall() # 결과 가져오기
    print(results) # [('경기도', '화성시', '봉담읍')]

    conn.close() # 연결 닫기
    


##########################################################
get_loc_data()
# print()
# print()
# response = requests.post(url,options)
# data = response.json()
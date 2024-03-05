import datetime
import math
import sqlite3
from django.shortcuts import render
import requests


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

    #<사용법>
    # module.exports = {
    #   toXY: (lat, lon) => dfsXyConv('toXY', lat, lon),
    #   fromXY: (x, y) => dfsXyConv('latlon', x, y)
    # }

def get_weather_api_data(): #날씨 데이터 가져올 수 있는 API
    service_key = 'ooH%2FvlpPYqrSdkp8Upqz6g%2FJ7KWVBVtEJ%2FQ6MzBpkZzgkP%2FivR3R506uj4hq7YOI65VcUm5MxTf6GNgOP0ffiA%3D%3D'
    data_type = 'JSON'
    num_of_rows = '250'  # 500은 되어야 TMN, TMX가 뜸
    today = datetime.datetime.now()
    base_date = f"{today.year}{today.month:02d}{today.day:02d}"
    base_time = '0200'
    nx = '57' #화성시 xy 임시로 넣어둠
    ny = '119'

    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={service_key}&dataType={data_type}&numOfRows={num_of_rows}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}" #단기예보
    response = requests.get(url)
    data = response.json()

    return data['response']['body']['items']['item'] 


def convertfcstTime():
    curTime = datetime.datetime.now()
    if curTime.hour < 3:
        curTime = '0300'
    else:
        curTime = curTime.strftime("%H00")
    
    return curTime

def convertfcstvaue(skycode,value):
    if skycode == 'SKY':
        if value == '1':
            skyvalue = '맑음'
        elif value == '3':
            skyvalue = '구름 많음'
        elif value == '4':
            skyvalue = '흐림'
    elif skycode == 'PTY':
        if value == '1':
            skyvalue = '비'
        elif value == '2':
            skyvalue = '비/눈'
        elif value == '3':
            skyvalue = '눈'
        elif value == '4':
            skyvalue ='소나기'

    return skyvalue

def get_weather_data(): # weatehr 데이터 가공해서 list로 내보내는 코드
    data = get_weather_api_data()
    curTime = convertfcstTime()
    sky = 0
    alertRain = 0
    humidity = '-'

    for i in data:
        if i['category']=='TMN': #최저기온
            minTmp = i['fcstValue']
        if i['category']=='TMX': #최고기온
            maxTmp = i['fcstValue']
        if i['category']=='PTY' and i['fcstValue']!= '0': #강수여부
            alertRain = '오늘은 비/눈 소식이 있습니다.'

        if i['fcstTime'] == curTime: #현재시간을 기준으로 한 날씨상태
            if i['category']=='TMP': #현재기온
                curTmp = i['fcstValue']
            if i['category']=='REH': #습도
                humidity = i['fcstValue']
            if i['category']=='PTY' and i['fcstValue']!= '0': #강수형태-비가 올때
                sky = convertfcstvaue('PTY',i['fcstValue'])
            if sky == 0: #강수 형태 - 비가 안 올때
                if i['category']=='SKY': #하늘상태
                    sky = convertfcstvaue('SKY',i['fcstValue'])

    weatherCondition = {
        'minTmp' : minTmp,
        'maxTmp' : maxTmp ,
        'alertRain' : alertRain ,
        'curTmp' : curTmp ,
        'humidity' : humidity ,
        'sky' : sky ,
    }           
    
    return weatherCondition


def get_loc_api_data(): #현재 위치 가져오는 구글API, IP를 기준으로 가져옴.
    loc_serviceKey = 'YOUR KEY'
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
    
    conn = sqlite3.connect('./db.sqlite3') # SQLite 데이터베이스 연결  
    cursor = conn.cursor() # 커서 생성
    query = f"SELECT address1, address2, address3 FROM weather_api WHERE gridX = {X} and gridY = {Y}" # SQL 쿼리 작성
    cursor.execute(query) # 쿼리 실행
    address = cursor.fetchall() # 결과 가져오기 [('경기도', '화성시', '봉담읍')]
    res_loc = f"{address[0][0]} {address[0][1]}" #경기도 화성시
    conn.close() # 연결 닫기

    return res_loc

def get_time():
    res_date = datetime.datetime.now().strftime("%m/%d %H:%M")
    return res_date


def get_icon():
    weather = get_weather_data()
    if weather['sky'] == '맑음':
        icon = "bi bi-brightness-high"
    elif weather['sky'] == '구름 많음':
        icon = "bi bi-cloudy-fill"
    elif weather['sky'] == '흐림':
        icon = "bi bi-cloud-sun-fill"
    elif weather['sky'] == '비':
        icon = "bi bi-cloud-rain"
    elif weather['sky'] == '비/눈':
        icon = "bi bi-cloud-sleet-fill"
    elif weather['sky'] == '눈':
        icon = "bi bi-cloud-snow-fill"
    elif weather['sky'] == '소나기':
        icon = "bi bi-cloud-rain-heavy-fill"
    else: #오류처리
        icon = '0'
    
    return icon


##########################################################
# get_weather_api_data()
# print(get_weather_data())
# print()

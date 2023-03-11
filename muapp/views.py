from django.shortcuts import render
from django.http import HttpResponse
from .api import get_loc_data, get_time, get_weather_data, get_icon
import sqlite3
import requests
import datetime
import math, json, sqlite3

# Create your views here.

# def 404(request):
#     return render(request,"404.html")

def index(request):
    location = get_loc_data()
    date = get_time()
    weather = get_weather_data()
    icon = get_icon()
    results= {
        'location' : location,
        'date' : date,
        'minTmp' : weather['minTmp'],
        'maxTmp' : weather['maxTmp'] ,
        'alertRain' : weather['alertRain'] ,
        'curTmp' : weather['curTmp'] ,
        'humidity' : weather['humidity'] ,
        'sky' : weather['sky'] ,
        'icon' : icon,
        }
    return render(request,"index.html",results)

def blog(request):
    return render(request,"blog.html")

def feature(request):
    return render(request,"feature.html")

def product(request):
    return render(request,"product.html")

def about(request):
    return render(request,"about.html")

def login(request):
    return render(request,"login.html")


def login(request):
    return render(request,"login.html")


<<<<<<< HEAD
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

def get_weather_api_data(): #날씨 데이터 가져올 수 있는 API
    service_key = 'ooH%2FvlpPYqrSdkp8Upqz6g%2FJ7KWVBVtEJ%2FQ6MzBpkZzgkP%2FivR3R506uj4hq7YOI65VcUm5MxTf6GNgOP0ffiA%3D%3D'
    data_type = 'JSON'
    num_of_rows = '250'  # 500은 되어야 TMN, TMX가 뜸
    today = datetime.datetime.now()
    base_date = f"{today.year}{today.month:02d}{today.day:02d}"
    base_time = str(today.hour)+'00'
    nx = '57' #화성시 xy 임시로 넣어둠
    ny = '119'

    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={service_key}&dataType={data_type}&numOfRows={num_of_rows}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"

    response = requests.get(url)
    data = response.json()

    return data['response']['body']['items']['item'] #3/10 갑자기 에러남 먼데

def get_loc_api_data(): #현재 위치 가져오는 구글API, IP를 기준으로 가져옴.
    loc_serviceKey = 'AIzaSyC7VJJjA3IZGewIvQ5uSzUxpqQwfqoxjxI'
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={loc_serviceKey}"
    options = {'considerIp': True,}
    response = requests.post(url,options)
    data = response.json()
    return data['location']
# print('날씨:', get_loc_api_data()['lat'])

def get_loc_data():# 현재 위치를 바탕으로 db에서 주소 이름 찾는 코드
    lat = get_loc_api_data()['lat']
    lng = get_loc_api_data()['lng']
    rs = dfsXyConv('toXY', lat, lng)
    X,Y = rs['x'],rs['y']

    
    conn = sqlite3.connect('D:\grad-job\django\db.sqlite3') # SQLite 데이터베이스 연결  
    cursor = conn.cursor() # 커서 생성
    query = f"SELECT address1, address2, address3 FROM weather_api WHERE gridX = {X} and gridY = {Y}" # SQL 쿼리 작성
    cursor.execute(query) # 쿼리 실행
    address = cursor.fetchall() # 결과 가져오기
    #print(address) # [('경기도', '화성시', '봉담읍')]

    conn.close() # 연결 닫기

    return address

#def weatherToHtml():
    ## 날씨 아이콘 띄울 수 있는 초단기예보 받아오기 
        # const weatherState = (ptyCode, skyCode) => {
        #     switch (ptyCode) {
        #     case 1: case 4: return 'rainy'
        #     case 2: return 'snowAndRainy'
        #     case 3: return 'snow'
        #     }
        #     switch (skyCode) {
        #     case 1: return 'clear'
        #     case 3: return 'partlyClear'
        #     case 4: return 'cloudy'
        #     }
        # } 
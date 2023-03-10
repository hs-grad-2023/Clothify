import math

def dfsXyConv(code, v1, v2):
    PI, tan, log, cos, pow, floor, sin, sqrt, atan, abs, atan2 = math.pi, math.tan, math.log, math.cos, math.pow, math.floor, math.sin, math.sqrt, math.atan, math.abs, math.atan2

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
import geoip2.database
def check_city(data):
    checked_data = []
    gR = geoip2.database.Reader('GeoLite2-City.mmdb')
    for item in data:
        c = item.strip().split(':')
        try:
            cy = str(gR.city(c[0]).country.iso_code)
            if cy == 'None':
                cy = 'unknow'
        except Exception as e:
            cy = 'unknow'
        checked_data.append(item.strip() + ' ' + cy)
    return checked_data

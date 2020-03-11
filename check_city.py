import geoip2.database
def check_city(data):
    checked_data = []
    geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
    for item in data:
        c = item.strip().split(':')
        try:
            cy = str(geoipReader.city(c[0]).country.iso_code)
            if cy == 'None':
                cy = 'unknow'
                item[1] = cy
        except Exception as e:
            item[1] = 'unknow'
        checked_data.append(item)
    return checked_data

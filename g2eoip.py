#!python3
import geoip2.database
import sys
# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
# Replace "city" with the method corresponding to the database
# that you are using, e.g., "country".
ip = '128.101.101.101'
ip = sys.argv[1]
response = reader.city(ip)
print(ip)
print(response)
print('iso code:'+ response.country.iso_code)
print('country name:'+ response.country.name)
print('country names:' + response.country.names['zh-CN'])
print(response.subdivisions.most_specific.name+response.subdivisions.most_specific.names['zh-CN'])
print(response.subdivisions.most_specific.iso_code)
print('city name:'+ str(response.city.name) +str(response.city.names['zh-CN']))
print('post code:'+ str(response.postal.code))
print('latitude:'+ str(response.location.latitude))
print('longitude:'+ str(response.location.longitude))
reader.close()

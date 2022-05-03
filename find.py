import geocoder

g = geocoder.ip('me')
print(g.json)

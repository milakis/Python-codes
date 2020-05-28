
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import vincenty
import pgeocode

""""
This part of the code defines the distance of different areas in London from a certain point 
(in this case, the Buckingham Palace) by the latitude and the longitude 
"""

# import data and add London to the Area column
df = pd.read_stata(' ')
df['Area'] = df['Area'].astype(str) + ' London'

# generate coordinates
geolocator = Nominatim(user_agent=" ")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
df['location'] = df['Area'].apply(geocode)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

# generate distance from the Buckingham Palace
position = np.linspace(0, 1346, num=1347)
df['distance'] = 0
Buck_palace = (51.500841300000005, -0.14298782562962786)
for p in position:
    df['distance'][p] = vincenty(Buck_palace, df['point'][p]).km

# save
del df['location']
del df['point']
df.to_stata(' ')

"""
This part of the code defines the minimum distance of the Swiss Bern Canton from all the zip codes
of the other cantons in Switzerland. 
"""

# the swiss zip codes could be downloaded from the official website https://opendata.swiss/de/dataset/plz_verzeichnis
df = pd.read_excel('plz_verzeichnis_v2.xlsx')

# divide the sample between the Bern canton and the others
be = df[df['kanton'] == "BE"]
nbe = df[df['kanton'] != "BE"]

# prepare the values and empty arrays for the loop
dist = pgeocode.GeoDistance('CH')
zc = be['postleitzahl'].reset_index(drop=True)
zc = list(dict.fromkeys(zc))
nzc = nbe['postleitzahl'].reset_index(drop=True)
nzc = list(dict.fromkeys(nzc))
numbers = np.linspace(0, len(zc), len(zc), endpoint = False).astype(int)
values = np.linspace(0, 0, len(nzc), endpoint = False)
vec=np.linspace(0, 0, len(zc), endpoint = False)

# for every zip code in the non-Bern cantons calculate the distance from every zip code in the Bern canton
# and choose the minimum value
for m in range(len(nzc)):
    num = nzc[m]
    for i in range(len(zc)):
        z = zc[i]
        n = numbers[i]
        vec[n] = dist.query_postal_code(num, z)
    mi = min(vec)
    values[m] = mi

# save the result
df = pd.DataFrame({'zip_code': nzc, 'distance': values}, columns=['zip_code', 'min_distance'])
df.to_csv(' ')
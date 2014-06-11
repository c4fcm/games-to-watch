import json
import requests
import util.filecache as filecache

def reverse_geocode(lat,lng):
    '''
    Cache these results to reduce load on their server, and hopefully stay under the use limit radar
    '''
    payload = {
        'format': 'json',
        'latitude': round(float(lat),3),
        'longitude': round(float(lng),3),
        'showall': True
    }
    cache_key = filecache.md5_key( str(payload['latitude'])+str(payload['longitude']) )
    if filecache.contains(cache_key):
        response = filecache.get(cache_key)
        location = json.loads(response)
        location['cache'] = True
    else:
        response = requests.get("http://data.fcc.gov/api/block/find", params=payload)
        filecache.put(cache_key, response.content)
        location = response.json()
        location['cache'] = False
    return location

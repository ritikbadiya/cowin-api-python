import requests
import json
import pandas as pd
import time
import difflib


browser_header={"Accept-Language": "en_US","User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}



def states():
    url='https://cdn-api.co-vin.in/api/v2/admin/location/states'
    res=requests.get(url,headers=browser_header)
    return res



def load_distt():
    md={}
    for i in range(37):
        url='https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(i)
        res=requests.get(url,headers=browser_header)
        distt=res.json()['districts']
        md.update({i['district_name'].lower():i['district_id'] for i in distt})
    return md
distts=load_distt()



def get_by_dist_name(dist):
    dist_id=distts[difflib.get_close_matches(dist, distts.keys())[0]]
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    parameters = {'district_id':dist_id,'date':time.strftime("%d:%m:%Y", time.localtime())}
    res=requests.get(url,params=parameters,headers=browser_header)
    return res



def get_by_pin(pin):
    parameters = {'pincode':pin,'date':time.strftime("%d:%m:%Y", time.localtime())}
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    res=requests.get(url,params=parameters,headers=browser_header)
    return res

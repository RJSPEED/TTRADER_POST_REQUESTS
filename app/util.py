import hashlib
import requests
import json

#http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=AAPL
#http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=Apple

"""
'[{"Symbol":"AAPL","Name":"Apple Inc","Exchange":"NASDAQ"},
{"Symbol":"APLE","Name":"","Exchange":"NYSE"},
{"Symbol":"APLE","Name":"Apple Hospitality REIT Inc","Exchange":"Cboe BZX"},
{"Symbol":"VXAPL","Name":"CBOE Apple VIX Index","Exchange":"Market Data Express"}]'
"""

""" fake prices to lookup for unit testing purposes """
FAKE_PRICES = {
        'stok': 3.50,
        'stokx': 1.50,
        'tsla': 15.50,
        'ms': 90.50
    }

def hash_password(password):
    hasher = hashlib.sha512()
    hasher.update(password.encode())
    return hasher.hexdigest()
    
def get_price(ticker): 
    url_str = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=" + ticker 
    stock = requests.get(url_str)
    stock_data = json.loads(stock.text)
    #Response for invalid ticker is a 1 item dict
    if len(stock_data) > 1:
        return stock_data['LastPrice']

def get_ticker(co_name): 
    url_str = "http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=" + co_name
    stock = requests.get(url_str)
    stock_data = json.loads(stock.text)
    #Response for invalid Company name is empty dict
    if len(stock_data) > 0:
        return stock_data

    #if ticker in FAKE_PRICES.keys():
    #    return FAKE_PRICES[ticker]
    
from decimal import *
import httplib
import urllib
import json
import hashlib
import hmac
import time
BTC_api_key = ""
BTC_api_secret = ""
#fo = open("memory.txt", "r+")
#fo.write(str(nonce));
#nonce = fo.read()
#nonce = int(nonce)
tickerbtcusd = dict()
tickerltcusd = dict()
tickerltcbtc = dict()
tradehist = dict()
getinfo = dict()
btcusdlast = 0#= dict()
ltcusdlast = 0#= dict()
ltcbtclast = 0#= dict()
class client:
    def tickerbtcusd(self):
        global tickerbtcusd
        global btcusdlast
        conn = httplib.HTTPSConnection("btc-e.com")
        params = {"method":"ticker",}
        params = urllib.urlencode(params)
        H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded","Key":BTC_api_key,"Sign":sign}
        conn.request("POST", "/api/2/btc_usd/ticker", params, headers)
        response = conn.getresponse()
        tickerbtcusd = json.load(response)
        a = tickerbtcusd["ticker"]
        btcusdlast = a.get("last")
        #print "BTC/USD::Buy Price: ", a.get("buy")," Sell Price: ",a.get("sell")," last price: ",a.get("last")
        conn.close()
    def tickerltcusd(self):
        global tickerltcusd
        global ltcusdlast
        conn = httplib.HTTPSConnection("btc-e.com")
        params = {"method":"ticker"}
        params = urllib.urlencode(params)
        H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded","Key":BTC_api_key,"Sign":sign}
        conn.request("POST", "/api/2/ltc_usd/ticker", params, headers)
        response = conn.getresponse()
        tickerltcusd = json.load(response)
        a = tickerltcusd["ticker"]
        ltcusdlast = a.get("last")
        #print "LTC/USD::Buy Price: ", a.get("buy")," Sell Price: ",a.get("sell")," last price: ",a.get("last")
        conn.close()
    def tickerltcbtc(self):
        global tickerltcbtc
        global ltcbtclast
        conn = httplib.HTTPSConnection("btc-e.com")
        params = {"method":"ticker"}
        params = urllib.urlencode(params)
        H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded","Key":BTC_api_key,"Sign":sign}
        conn.request("POST", "/api/2/ltc_btc/ticker", params, headers)
        response = conn.getresponse()
        tickerltcbtc = json.load(response)
        a = tickerltcbtc["ticker"]
        ltcbtclast = a.get("last")
        #print "LTC/BTC::Buy Price: ", a.get("buy")," Sell Price: ",a.get("sell")," last price: ",a.get("last")
        conn.close()
    def tradehistory(self):
        global tradehist
        global nonce
        conn = httplib.HTTPSConnection("btc-e.com")
        params = {"method":"TradeHistory","nonce": nonce,}
        params = urllib.urlencode(params)
        H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded","Key":BTC_api_key,"Sign":sign}
        conn.request("POST", "/tapi", params, headers)
        nonce = nonce + 1
        fo = open("memory.txt", "r+")
        fo.write(str(nonce));
        response = conn.getresponse()
        tradehist = json.load(response)
        print "Success is", bool(tradehist["success"])
        conn.close()
        if tradehist["success"]==1:
            a = tradehist
            b = a["return"]
            x = b.items()
            c = x[0]
            print c

    def getinfo(self):
        global nonce
        global getinfo
        conn = httplib.HTTPSConnection("btc-e.com")
        params = {"method":"getInfo","nonce": nonce}
        params = urllib.urlencode(params)
        H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
        H.update(params)
        sign = H.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded","Key":BTC_api_key,"Sign":sign}
        conn.request("POST", "/tapi", params, headers)
        nonce = nonce + 1
        fo = open("memory.txt", "r+")
        fo.write(str(nonce));
        response = conn.getresponse()
        getinfo = json.load(response)
        print "Success is", bool(getinfo["success"])
        conn.close()
        if getinfo["success"]==1:
            a = getinfo["return"]
            b = a.get("funds")
            print "Balance Btc: ",b.get("btc"), " Balance Ltc: ", b.get("ltc")

client = client()
if(1==1):
    print "-----------------------------------------------------------------------"
    #client.getinfo()
    #client.tradehistory()
    change_in_time_oldbu = 0
    change_in_time_oldlu = 0
    change_in_time_oldlb = 0
    change_in_time_first_btcusd = btcusdlast
    change_in_time_first_ltcusd = ltcusdlast
    change_in_time_first_ltcbtc = ltcbtclast
    while(True):
        client.tickerbtcusd()
        time.sleep(1)
        client.tickerltcusd()
        time.sleep(1)
        client.tickerltcbtc()
        time.sleep(1)
        change_in_time_newbu = btcusdlast
        globalxbu = change_in_time_newbu-change_in_time_first_btcusd
        globalybu = change_in_time_newbu-change_in_time_oldbu
        if ((change_in_time_newbu>change_in_time_oldbu)|(change_in_time_newbu<change_in_time_oldbu)):
                print time.strftime("[%I:%M:%S]", time.localtime()),"Bitcoin: ","Global:",globalxbu,"Current:",globalybu,"Last: ",btcusdlast
                print "-----------------------------------------------------------------------"
        change_in_time_oldbu = change_in_time_newbu

        change_in_time_newlu = ltcusdlast
        globalxlu = change_in_time_newlu-change_in_time_first_ltcusd
        globalylu = change_in_time_newlu-change_in_time_oldlu
        if ((change_in_time_newlu>change_in_time_oldlu)|(change_in_time_newlu<change_in_time_oldlu)):
            print time.strftime("[%I:%M:%S]", time.localtime()),"Litecoin: ","Global:",globalxlu,"Current:",globalylu,"Last: ",ltcusdlast
            print "-----------------------------------------------------------------------"
        change_in_time_oldlu = change_in_time_newlu

        change_in_time_newlb = ltcbtclast
        globalxlb = change_in_time_newlb-change_in_time_first_ltcbtc
        globalylb = change_in_time_newlb-change_in_time_oldlb
        if ((change_in_time_newlb>change_in_time_oldlb)|(change_in_time_newlb<change_in_time_oldlb)):
            print time.strftime("[%I:%M:%S]", time.localtime()),"LtcBtc: ","Global:",globalxlb,"Current:",globalylb,"Last: ",ltcbtclast
            print "-----------------------------------------------------------------------"
        change_in_time_oldlb = change_in_time_newlb
        time.sleep(5)






















import requests
import json
import os
import time
from datetime import datetime


class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
                'start':'1',
                'limit':'100',
                'convert':'USD'
            }
        self.headers = {
                'Accepts':'application/json',
                'X-CMC_PRO_API_KEY':'c7bf991f-ea63-422f-a383-332d0e2166e9',
        }



    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, params=self.params, headers=self.headers).json()
        return r['data']



CurrenciesData = Bot()


while(True):
    now=datetime.now()
    currencies = CurrenciesData.fetchCurrenciesData()
    report={
            "1" : [],
            "2" : {
                "a" : [],
                "b" : []
         },
            "3" : [],
            "4" : [],
            "5" : []
        }
    crypto_volume_max = None
    for currency in currencies:
        if not crypto_volume_max or currency['quote']['USD']['volume_24h'] > crypto_volume_max['quote']['USD']['volume_24h']:
            crypto_volume_max=currency
    print(f"\nLa criptovaluta con il volume maggiore delle ultime 24 ore è: \n{crypto_volume_max['name']}({crypto_volume_max['symbol']}) con un volume pari a {crypto_volume_max['quote']['USD']['volume_24h']} $")
    report["1"].append(f"La criptovaluta con il volume maggiore delle ultime 24 ore: {crypto_volume_max['name']}({crypto_volume_max['symbol']}) con un volume pari a {crypto_volume_max['quote']['USD']['volume_24h']} $")

    print(f"\nLe migliori criptovalute per incremento percentuale nelle ultime 24h sono:\n")
    report["2"]["a"].append(f"Le migliori criptovalute per incremento percentuale nelle ultime 24h sono:")
    best_crypto = None
    i = 0
    n = 1
    for currency in currencies:
        if not best_crypto or currency['quote']['USD']['percent_change_24h']>best_crypto['quote']['USD']['percent_change_24h']:
            best_crypto=currency
        if currency['quote']['USD']['percent_change_24h'] >= i:
            print(f"{currency['name']} ({currency['symbol']}) con un incremento di {currency['quote']['USD']['percent_change_24h']} %")
            report["2"]["a"].append(f"{currency['name']} ({currency['symbol']}) con un incremento di {currency['quote']['USD']['percent_change_24h']} %")
            n = n + 1
        if n > 10: break

    print(f"\nLe peggiori criptovalute per decremento percentuale nelle ultime 24h sono:\n")
    report["2"]["b"].append(f"Le peggiori criptovalute per decremento percentuale nelle ultime 24h sono:")
    worst_crypto = None
    n = 1
    for currency in currencies:
        if not worst_crypto or currency['quote']['USD']['percent_change_24h'] > worst_crypto['quote']['USD']['percent_change_24h']:
            worst_crypto = currency
        if currency['quote']['USD']['percent_change_24h'] <= i:
            print(f"{currency['name']} ({currency['symbol']}) con un decremento di {currency['quote']['USD']['percent_change_24h']} %")
            report["2"]["b"].append(f"{currency['name']} ({currency['symbol']}) con un decremento di {currency['quote']['USD']['percent_change_24h']} %")
            n = n + 1
        if n > 10: break

    best_twenty_order = []
    n = 1
    for currency in currencies:
        if n < 20:
            best_twenty_order.append(currency['quote']['USD']['price'])
            n = n + 1
    print(f"\nPer acquistare una unità di ogni criptovaluta delle prime 20 criprovalute sono necessari:\n{sum(best_twenty_order)} $")
    report["3"].append(f"Per acquistare una unita di ogni criptovaluta delle prime 20 criprovalute sono necessari: {sum(best_twenty_order)} $")


    best_volume_crypto_order = []
    for currency in currencies:
        if currency['quote']['USD']['volume_24h']>76000000:
            best_volume_crypto_order.append(currency['quote']['USD']['price'])
    print(f"\nPer acquistare una unità di ogni criptovaluta con un volume delle ultime 24 ore superiore a 76.000.000 $ sono necessari:\n{sum(best_volume_crypto_order)} $")
    report["4"].append(f"Per acquistare una unita di ogni criptovaluta con un volume delle ultime 24 ore superiore a 76.000.000 $ sono necessari: {sum(best_volume_crypto_order)} $")


    price = []
    percentage_change=[]
    n = 1
    for currency in currencies:
        if n<20:
            price.append(currency['quote']['USD']['price'])
            percentage_change.append(float(currency['quote']['USD']['price']*float(currency['quote']['USD']['percent_change_24h'])/100))
            profit = ((sum(percentage_change)/sum(price))*100)
            n = n + 1
    print(f"\nLa percentuale di guadagno/perdita acquistando una unità di ciascuna delle prime 20 criptovalute nella giornata di ieri corrisponde a:\n{profit} %")
    report["5"].append(f"La percentuale di guadagno/perdita acquistando una unita di ciascuna delle prime 20 criptovalute nella giornata di ieri corrisponde a: {profit} %")

    with open("today.json", "w") as file:
        json.dump(report, file, indent=4)

    Current_Date = datetime.today().strftime('%d-%b-%Y')
    os.rename(r"/Users/vincenzo.gautieri/PycharmProjects/pythonProject/today.json", r"/Users/vincenzo.gautieri/PycharmProjects/pythonProject/Report "+str(Current_Date)+ ".json")


    hour = 24
    minutes = 60 * hour
    seconds = 60 * minutes
    time.sleep(seconds)
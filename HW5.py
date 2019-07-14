from zeep import Client
import datetime
from pymongo import MongoClient
import pprint

m_client = MongoClient('mongodb://127.0.0.1:27017')
db = m_client['cbr']
cbr = db.cbr

def get_exchange_rate(currency, date):
    url = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
    client = Client(url)
    rate = client.service.GetCursOnDate(date)
    list_rate = rate._value_1._value_1
    for item in list_rate:
        for k,v in item.items():
            if v.VchCode == currency:
                return item['ValuteCursOnDate']['Vcurs']

def get_rates_over_period (currency, date1, date2):
    exchange_rates = []
    delta = (date2 - date1).days
    for i in range(delta+1):
        date = date1 + datetime.timedelta(days=i)
        rate = float(get_exchange_rate(currency, date))
        rate_dict = {'date': date, 'currency': currency, 'rate': rate}
        exchange_rates.append(rate_dict)

    return exchange_rates

def database_write(data):
    cbr.insert_many(data)

def get_dates(date1, date2):
    return list(cbr.find({'$and':
                           [{'date': {'$gte': date1}}, {'date':  {'$lte': date2}}]
              }))


date2 = datetime.datetime.today()
date1 = datetime.datetime(year=date2.year, month=date2.month-2, day=date2.day)
print(date2, date1)

database_write(get_rates_over_period('EUR', date1, date2))

def get_result(date1, date2):
    rates = get_dates(date1, date2)
    max_diff = -1000
    i = 0
    for day in rates:
        i +=1
        for j in range(i, len(rates)):
            if rates[j]['rate'] - day['rate'] > max_diff:
                max_diff = rates[j]['rate'] - day['rate']
                buy_date = day['date']
                sell_date = rates[j]['date']
            else:
                continue
    currency = rates[0]['currency']
    return {'buy_date': buy_date, 'sell_date': sell_date, 'return': max_diff, 'currency': currency}

date_querry2 = datetime.datetime.today()
date_querry1 = datetime.datetime(year=date2.year, month=date2.month, day=date2.day-10)

result = get_result(date_querry1, date_querry2)

print(f'Валюту {result["currency"]} выгодно было купить {result["buy_date"].date()}, '
      f'а продать {result["sell_date"].date()}. Прибыль: {result["return"]}')

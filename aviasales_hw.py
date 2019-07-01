import requests
import pprint
import json

req_city = requests.get("http://api.travelpayouts.com/data/ru/cities.json")
data_city = json.loads(req_city.text)


dict_city = {}
for city in data_city:
    dict_city[city['name']] = city['code']

origin_city = input('Введите город вылета: ')
dest_city = input('Введите город прилета: ')

req_ticket = requests.get(f'http://min-prices.aviasales.ru/calendar_preload?origin={dict_city[origin_city.capitalize()]}&\
destination={dict_city[dest_city.capitalize()]}&one_way=true')


data_ticket = json.loads(req_ticket.text)['best_prices']

data_ticket_sorted = sorted(data_ticket, key = lambda x: x['value'])

print(f'Город вылета: {(data_ticket_sorted[0]["origin"])} \n'
      f'Город прилета: {data_ticket_sorted[0]["destination"]} \n '
      f'Дата вылета: {data_ticket_sorted[0]["depart_date"]} \n '
      f'Цена: {data_ticket_sorted[0]["value"]} руб.')




















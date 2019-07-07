from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
import pprint
import re

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['hh']
hh = db.hh

position = 'программист'
language = input('Введите язык программирования: ')
num_pages = input('Введите количество страниц: ')

def create_link (position, language, num_page):
    link = 'https://hh.ru/search/vacancy?text=' + position.lower() + ' ' + \
           language + '&page=' + str(num_page)
    return link

def create_div_list (link):
    headers_ = {'User-Agent': 'Mozilla/5.0'}
    html = requests.get(link, headers=headers_).text
    parsed_html = bs(html, 'lxml')
    vacancy_div = parsed_html.findAll("div", class_="vacancy-serp-item")
    return vacancy_div

def get_exchange_rates():
    link = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    html = requests.get(link).text
    parsed_html = bs(html, 'lxml')

    currencies_html = parsed_html.findAll('valute')

    currencies_list = []
    rates_list = []
    for currency in currencies_html:
        currencies_list.append(currency.find('charcode').string)
        rates_list.append(float(currency.find('value').string.replace(',', '.')) /
                          float(currency.find('nominal').string))

    currencies_rates = {currencies_list[i]: rates_list[i] for i in range(len(currencies_list))}
    return currencies_rates

currency_dict = {'грн': 'UAH', 'EUR': 'EUR', 'USD': 'USD', 'KZT': 'KZT'}

for i in range(int(num_pages)):
    link = create_link(position, language, i+1)
    vacancy_div = create_div_list(link)

    for div in vacancy_div:

        try:
            salary = div.find('div', class_='vacancy-serp-item__compensation').string
            salary = salary.replace('\xa0', '')

            salary_list = re.findall(r'[\d]+', salary)
            if 'от' in salary:
                salary_min = salary_list[0]
                salary_max = 0
            elif 'до' in salary:
                salary_min = 0
                salary_max = salary_list[0]
            else:
                salary_min = salary_list[0]
                salary_max = salary_list[1]
            currency = re.findall(r'([а-яА-яa-zA-Z]{3})\.|([а-яА-яa-zA-Z]{3})', salary)
            currency = list(filter(None, currency[0]))

        except:
            salary_min = 0
            salary_max = 0

        exchange_rates = get_exchange_rates()

        if currency[0] != 'руб':
            salary_min_rub = float(salary_min) * exchange_rates[currency_dict[currency[0]]]
        else:
            salary_min_rub = float(salary_min)

        vacancy_data = {
            'vacancy': div.find('a').string,
            'link': div.find('a')['href'],
            'salary_min': float(salary_min),
            'salary_max': float(salary_max),
            'currency': currency[0],
            'salary_min in RUB': salary_min_rub
        }

        hh.insert(vacancy_data)

def get_vacancies(min_salary):
    for vacancy in hh.find({'salary_min in RUB': {'$gt': min_salary}}):
        pprint.pprint(vacancy)
        print()

get_vacancies(100000)
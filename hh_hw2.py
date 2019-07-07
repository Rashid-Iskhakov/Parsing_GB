from bs4 import BeautifulSoup as bs
import requests

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

for i in range(int(num_pages)):
    link = create_link(position, language, i+1)
    vacancy_div = create_div_list(link)

    print(f'Страница {i+1}')

    for div in vacancy_div:
        vacancy_name = div.find('a').string
        vacancy_link = div.find('a')['href']

        try:
            salary = div.find('div', class_='vacancy-serp-item__compensation').string
        except:
            salary = 'З/п не указана'

        print(vacancy_name, '-', salary, '\n', vacancy_link)

    print()
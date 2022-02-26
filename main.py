import requests
import bs4
import re
from pprint import pprint

def response(url):
    HEADERS = {
        'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
        'Accept-Language': 'ru-RU,ru;q=0.9', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Cache-Control': 'max-age=0',
        'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'sec-ch-ua-mobile': '?0'}
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup

def pars_post(soup,keywords):
    div = soup.find_all('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow')
    for txt in div:

        for key in keywords:
            result = re.search(fr'{key.lower()}', f'{txt.get_text().lower()}')
            if result != None:
                return True

def pars_previev (keywords):
    articles = response('https://habr.com/ru/news').find_all('article', class_="tm-articles-list__item")
    final = []
    for art in articles:
        date = str([date for date in art.find('span', class_="tm-article-snippet__datetime-published")])[50:67]
        title = art.find('h2').text
        url = 'https://habr.com' + str(art.find('a', class_='tm-article-snippet__title-link').get('href'))
        post = pars_post(response(url), keywords)
        for key in keywords:
            result = re.search(fr'{key.lower()}', f'{art.get_text().lower()}')
            if result != None or post:
                final.append([date, title, url])
                break

    pprint(final)


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
pars_previev(KEYWORDS)
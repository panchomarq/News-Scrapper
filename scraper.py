import requests
import lxml.html as html
import os
import datetime
from urllib.parse import urljoin


HOME_URL = "https://www.elnacional.com/"
XPATH_LINK_ARTICLE = '//div[@class="item-details"]/h3[@class="entry-title td-module-title"]/a/@href'
XPATH_LINK_TITLE = '//header[@class="td-post-title" or @class="entry-title td-module-title"]/h1[@class="entry-title"]/text()'
XPATH_SUMMARY = '//header[@class="td-post-title"]/p/text()'
XPATH_BODY = '//div[@class="td-post-content"]/p/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                tittle = parsed.xpath(XPATH_LINK_TITLE)[0]
                tittle = tittle.replace('\"','')
                tittle = tittle.replace('?','')
                tittle = tittle.replace('¿','')
                #Cambio en los dos puntos del los títulos
                tittle = tittle.replace(':','--')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with  open(f'{today}/{tittle}.txt', 'w', encoding='utf-8') as f:
                f.write(tittle)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_ARTICLE)
            print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()

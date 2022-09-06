import requests
import bs4
import re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36'}

base_url = 'https://habr.com'
url = base_url + '/ru/all/'

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def responce_get(urls, headers):
    """Поиск статей по содержимому страницы сайта"""
    response = requests.get(url=urls, headers=headers)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    return articles


def find_link(articles, base_urls):
    """Поиск ссылок на статьи с главной страницы"""
    href = articles.find(class_='tm-article-snippet__title-link').attrs['href']
    links = base_urls + href
    return links


def keyword_search(articles, keywords):
    """Поиск ключевых слов по всему тексту статьи"""
    for article in articles:
        hubs = article.find_all(attrs={"class":"tm-article-snippet__hubs-item-link"})
        hubs = set(hub.find('span').text.lower() for hub in hubs)
        if set(keywords) & hubs:  # Сравниваем множества найденных и ключевых слов на пересечение
            title = article.find('h1').find('span').text  # Получаем заголовок искомой статьи
            hub_datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
            result = hub_datetime + ' - ' + title + ' - ' + link  # Собираем дату, заголовок и ссылку в "кучу"
            print(result)  # Выводим результат
            return result


if __name__ == '__main__':

    hubs = responce_get(url, HEADERS)   # Получаем данные с сайта
    for hub in hubs:  # Проходим по preview статей
        link = find_link(hub, base_url)  # Получаем ссылки на статьи
        hub_articles = responce_get(link, HEADERS)
        keyword_search(hub_articles, KEYWORDS)  # Проверяем содержимое статей по ключевым словам

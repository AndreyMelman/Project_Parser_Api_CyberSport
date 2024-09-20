import aiohttp
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from core.config import settings



class News:

    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers


    # Функция парсинга новостного сайта
    async def load_articles(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as response:
                # Получаем URL нашего сайта
                response = await session.get(url=self.url, headers=self.headers)
                # Получаем HTML-файл
                soup = BeautifulSoup(await response.text(), "lxml")
                # Получаем кусок HTML-файла с которого будем парсить новости
                articles_items = soup.find_all(
                    "div",
                    class_="rounded-block root_d51Rr with-hover no-padding no-margin",
                )

                # Создаем словарь для записи новостей
                news_dict = {}

                for article in articles_items:
                    article_title = article.find("h3", class_="title_nSS03").text

                    article_url = (
                        f"https://www.cybersport.ru{article.find('a')['href']}"
                    )

                    article_img1 = article.find("img")
                    if article_img1 and "src" in article_img1.attrs:
                        article_img = article_img1["src"]
                    else:
                        article_img = ''

                    date_obj = article.find("time").get("datetime")[:-6]
                    article_date = datetime.strptime(date_obj, "%Y-%m-%dT%H:%M:%S")
                    article_date_time1 = article_date + timedelta(hours=3)
                    article_date_time = article_date_time1.strftime("%Y-%m-%d %H:%M:%S")

                    article_category = article.find("a", class_="tag_9QLmg").text

                    article_id = int(article_date.timestamp())

                    news_dict[article_id] = {
                        "article_title": article_title,
                        "article_date_time": article_date,
                        "article_url": article_url,
                        "article_img": article_img,
                        "article_category": article_category,
                    }

                return news_dict


parser = News(
    settings.parse.url,
    settings.parse.headers,
)











# class News:
#
#     def __init__(self, url: str, headers: dict[str, str]) -> None:
#         self.url = url
#         self.headers = headers
#
#     # Функция парсинга новостного сайта
#     async def load_articles(self) -> dict:
#         # Получаем URL нашего сайта
#         response = requests.get(url=self.url, headers=self.headers)
#         # Получаем HTML-файл
#         soup = BeautifulSoup(response.content, "lxml")
#         # Получаем кусок HTML-файла с которого будем парсить новости
#         articles_items = soup.find_all(
#             "div",
#             class_="rounded-block root_d51Rr with-hover no-padding no-margin",
#         )
#
#         # Создаем словарь для записи новостей
#         news_dict = {}
#
#         for article in articles_items:
#             article_title = article.find("h3", class_="title_nSS03").text
#
#             article_url = f"https://www.cybersport.ru{article.find('a')['href']}"
#
#             article_img1 = article.find("img")
#             if article_img1 and "src" in article_img1.attrs:
#                 article_img = article_img1["src"]
#             else:
#                 article_img = ''
#
#             date_obj = article.find("time").get("datetime")[:-6]
#             article_date = datetime.strptime(date_obj, "%Y-%m-%dT%H:%M:%S")
#             article_date_time1 = article_date + timedelta(hours=3)
#             article_date_time = article_date_time1.strftime("%Y-%m-%d %H:%M:%S")
#
#             article_category = article.find("a", class_="tag_9QLmg").text
#
#             article_id = str(int(article_date.timestamp()))
#
#             news_dict[int(article_id)] = {
#                 "article_title": article_title,
#                 "article_date_time": article_date,
#                 "article_url": article_url,
#                 "article_img": article_img,
#                 "article_category": article_category,
#             }
#
#         return news_dict
#
#
# parser = News(
#     settings.parse.url,
#     settings.parse.headers,
# )
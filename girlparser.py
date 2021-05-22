import shutil
import requests
import urllib.parse
from bs4 import BeautifulSoup as BS4
from urllib.parse import urlparse, urljoin
import random


def get_page(page):
    # lookFor=1 - girl
    # lookFor=4 - man
    link = "https://beboo.ru/search?iaS=0&status=all&countryId=110&regionId=-1&townId=-1&lookFor=1&reason=0&endAge=30&startAge=18&aS%5B25%5D%5B0%5D=0&aS%5B41%5D%5B0%5D=0&aS%5B26%5D%5B0%5D=0&aS%5B28%5D%5B0%5D=0&aS%5B29%5D%5B0%5D=0&aS%5B32%5D%5B0%5D=0&aS%5B30%5D%5B0%5D=0&aS%5B31%5D%5B0%5D=0&aS%5B33%5D%5B0%5D=0&aS%5B19%5D%5B0%5D=0&aS%5B23%5D%5B0%5D=0&aS%5B24%5D%5B0%5D=0&height=0&weight=0&page=" + page

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

    params = {"page": page}

    request = requests.get(link, headers=headers, params=params)

    return request.text


def is_404(html):
    page = BS4(html, "html.parser")

    if len(page.select("span.user-photo img")) < 0:
        return True
        return False


def get_imgs_from_page(page):
    html = get_page(page)

    images = []

    if is_404(html) == True:
        return False

    img_node = BS4(html, "html.parser")
    # search-result > div:nth-child(1) > a.user-link > span.user-photo > img
    imgs = img_node.select("span.user-photo img")

    for img in imgs:
        innerlist = []
        for i in imgs:
            innerlist.append(i["src"])
        images.append(innerlist)
        return images


def save_image(folder, link):
    image = requests.get(link, stream=True)

    filename = random.randint(1, 100000000000)

    # Формируем путь до файла вида: папка/имя_файла.jpg
    path_to_file = f"{folder}/{filename}.jpg"
    print(f"Сохранили фото: {path_to_file}")
    # Сохраняем фото в файл
    with open(path_to_file, "wb") as file_obj:
        shutil.copyfileobj(image.raw, file_obj)


def download_images(folder, page):
    # Получаем все ссылки из выдачи по запросу
    images = get_imgs_from_page(page)
    # Сохраняем все ссылки
    for image in images:
        for i in image:
            try:
                u = i.replace("180x180", "320x320")
                save_image(folder, u)

            except Exception as error:
                print(f"Проблема с записью файла: {error}")

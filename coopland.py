import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tg import *
import os
from dotenv import load_dotenv
from time import sleep
import textwrap
load_dotenv()

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6066.0 Safari/537.36'}

def download_picture(link_photo,path):
    response = requests.get(link_photo,verify=False, headers=headers)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)

picture_folder_path = "./photos"

os.makedirs(picture_folder_path, exist_ok=True)

chat_id = os.getenv('CHAT_ID')
token = os.getenv('TOKEN')


picture_name = "photo_coopland"

url = 'https://coop-land.ru/helpguides/new/'
while True:
    with open('last_posted_text_coopland.txt', 'r', encoding ='UTF-8') as my_file:
        last_posted_news = my_file.read()

    response = requests.get(url,verify=False, headers=headers)
    response.raise_for_status()  


    soup = BeautifulSoup(response.text, features="html.parser")
    header = soup.find('h2', class_="title").text


    article_content_div = soup.find('div', class_="article-content")
    description = article_content_div.find('div',class_="preview-text").text


    news_link = article_content_div.find('a')['href']

    article_clr_div = soup.find('div', class_="article clr")
    relative_photo_link = article_clr_div.find('img')['data-src']
    


    photo_link = (f'https://coop-land.ru{relative_photo_link}')
    path_to_photo = Path(picture_folder_path, f"{picture_name}.png")
    download_picture(photo_link,path_to_photo)


    text = f'''
    {header}

    {description}

    Ссылка на источник: {news_link}

    '''
    text = textwrap.dedent(text)
    if last_posted_news != text:
        send_pictures(token, chat_id, text,[path_to_photo])
        with open('last_posted_text_coopland.txt', 'w', encoding ='UTF-8') as my_file:
            my_file.write(text)


    sleep(15)


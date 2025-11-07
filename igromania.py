import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tg import *
import os
from dotenv import load_dotenv
from time import sleep
import textwrap
load_dotenv()




URL = 'https://www.igromania.ru/news/'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6066.0 Safari/537.36'}





headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.1.178 Yowser/2.5 Safari/537.36'}

def download_picture_igromania(link_photo,path):
    response = requests.get(link_photo,verify=False, headers=headers)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)


chat_id = os.getenv('CHAT_ID')
token = os.getenv('TOKEN')

picture_folder_path = "./photos"

os.makedirs(picture_folder_path, exist_ok=True)

picture_name_igromania = "photo_igromania"

url = 'https://www.igromania.ru/news/'
while True:
    with open('last_posted_text_igromania.txt', 'r', encoding ='UTF-8') as my_file:
        last_posted_news = my_file.read()

    response = requests.get(url,verify=False, headers=headers)
    response.raise_for_status()  

    soup = BeautifulSoup(response.text, features='html.parser')
    header = soup.find('a', class_='ShelfCard_cardLink__mSxdR')
    post_link = f'https://www.igromania.ru{header["href"]}'
    post_header = header.text

    news_page = requests.get(post_link, )
    news_page.raise_for_status()
    soup_new = BeautifulSoup(news_page.text, features='html.parser')
    post_img = soup_new.find('img', class_='MaterialCommonImage_picture__Z_3EU' )
    photo_link = post_img['src']

    news_link = soup.find('a', class_="ShelfCard_cardLink__mSxdR")
    news_linker = f"https://www.igromania.ru{news_link['href']}"

    description = soup.find('div', class_='ShelfCard_cardDescription__Tnd7y').text

    if description == None:
        description = ""


    
    path_to_photo = Path(picture_folder_path, f"{picture_name_igromania}.png")
    download_picture_igromania(photo_link,path_to_photo)


    text = f'''
    {post_header}

    {description}

    Ссылка на источник: {news_linker}

    '''
    text = textwrap.dedent(text)
    if last_posted_news != text:
        send_pictures(token, chat_id, text,[path_to_photo])
        with open('last_posted_text_igromania.txt', 'w', encoding ='UTF-8') as my_file:
            my_file.write(text)


    sleep(60)


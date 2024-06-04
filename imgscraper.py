import os
import shutil
import requests
import time
from bs4 import BeautifulSoup
import json

def getdata(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(f"Error getting data from {url}: {e}")
        return None

def download_image(img_url, folder_path, searchq, count):
    try:
        img_data = requests.get(img_url).content
        img_filename = os.path.join(folder_path, f"{searchq}_{count}.jpg")
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Image {count + 1} downloaded and saved as {img_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {img_url}: {e}")

def download_images(searchq_yes, searchq_no):
    yes_path = f"content/train/{searchq_yes}/yes"
    os.makedirs(yes_path, exist_ok=True)

    htmldata_yes = getdata(f"https://www.google.com/search?q={searchq_yes}&tbm=isch")
    if htmldata_yes is not None:
        soup_yes = BeautifulSoup(htmldata_yes, 'html.parser')
        for count, item in enumerate(soup_yes.find_all('img')):
            img_url = item['src']
            download_image(img_url, yes_path, searchq_yes, count)

    no_path = f"content/train/{searchq_no}/no"
    os.makedirs(no_path, exist_ok=True)
    for filename in os.listdir(yes_path):
        img_path = os.path.join(yes_path, filename)
        shutil.copy(img_path, no_path)

    no_path = f"content/train/{searchq_no}/yes"
    os.makedirs(no_path, exist_ok=True)

    htmldata_no = getdata(f"https://www.google.com/search?q={searchq_no}&tbm=isch")
    if htmldata_no is not None:
        soup_no = BeautifulSoup(htmldata_no, 'html.parser')
        for count, item in enumerate(soup_no.find_all('img')):
            img_url = item['src']
            download_image(img_url, no_path, searchq_no, count)

    yes_path = f"content/train/{searchq_yes}/no"
    os.makedirs(yes_path, exist_ok=True)
    for filename in os.listdir(no_path):
        img_path = os.path.join(no_path, filename)
        shutil.copy(img_path, yes_path)

    time.sleep(0)

if __name__ == "__main__":
    with open('images.json') as json_file:
        data = json.load(json_file)

    for searchq_yes, searchq_no in data.items():
        download_images(searchq_yes, searchq_no)

    print("Download complete.")
from requests.models import Response
import requests, base64, yaml, os
from bs4 import BeautifulSoup
from config import headers, base_url, database
from logger import *
from progress import *

# translate png to base64 code
def trans_png2base(pic_path):
    with open(pic_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read())
    return image_base64

# clear yaml file
def clear_yaml(yaml_path):
    with open(yaml_path, encoding='utf-8', mode='w') as f:
        f.truncate()

# write yaml file
def write_comic(keyword, page, comic_info, yaml_path):
    with open(yaml_path, encoding='utf-8', mode='a') as f:
        data = {
            "keyword": keyword,
            "page": page,
            "comic list": comic_info
        }
        yaml.dump(data=data, stream=f, allow_unicode=True)

# extract cover and url, input requests response return a tuple list, first png and second url
def extract_cover_url(response):
    soup = BeautifulSoup(response.text, "html.parser")
    cover_section_list = soup.find_all("article")
    comic_info = []
    for cover_section in cover_section_list:
        # each cover_section contains an article showing a comic cover and its addr
        comic_title = cover_section.find_all("div")[0].find_all("img")[0]['title']
        comic_id = cover_section['id']
        cover_addr = cover_section.find_all("img")[0]['src']
        comic_link = next(cover_section.find_all("h2", attrs={"class": "card_title"})[0].children)['href']
        comic_info.append({"id": comic_id, "title": comic_title, "cover": cover_addr, "link": comic_link})
    return comic_info

# generate img_list on https://nyahentai.biz
def gen_nyahentai(comic_link):
    title = "bad title"
    id = 0
    img_link_list = []
    response = requests.get(comic_link, headers=headers)
    if not response.ok:
        log_error(f"bad comic link, request fail: {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find_all("h1")[0].text
        id = soup.find_all("article")[0]['id']
        img_list = soup.find_all("img", {"data-lazy-src": True})
        # clear irrelevent link
        img_link_list = [img['data-lazy-src'] for img in img_list if "cdn" in img['data-lazy-src']]
    return {"title": title, "id": id, "img_link_list": img_link_list}

# jpg downloader, make a folder named f"{title}" and download pictures there
def pic_download(img_link_list, id):
    if not os.path.exists(f"./download/{id}"):
        os.mkdir(f"./download/{id}")
        log_info(f"make folder {id}")
    else:
        log_warning(f"floder {id} already exists, new comic may replace former ones")
    img_cnt = 0                 # how many images
    img_len = 0                 # number of digits total_len have
    total_num = len(img_link_list)   # number of image in the list
    while total_num > 0:
        img_len = img_len + 1
        total_num = total_num // 10
    progress_bar(0, len(img_link_list)) # begin progress bar
    for img_link in img_link_list:
        log_info(f"deal with {img_link}")
        img_cnt = img_cnt + 1
        new_pic_name = f"{img_cnt}.jpg"
        current_len = 0
        tmp = img_cnt
        while tmp > 0:          # number of digits img_cnt have
            current_len = current_len + 1
            tmp =  tmp // 10
        while current_len < img_len:
            new_pic_name = "0" + new_pic_name
            current_len = current_len + 1
        img = requests.get(img_link, headers=headers)
        if not img.ok:
            log_error(f"bad img link {img_link}")
        else:
            with open(f"./download/{id}/{new_pic_name}", 'wb') as f:
                f.write(img.content)
        progress_bar(img_cnt, len(img_link_list))
    print("\ndownload finish")                         # finish progress bar

# scratch pictures from a certain addr
def get_pictures(comic_link):
    response = requests.get(comic_link, headers=headers)
    if not response.ok:
        log_error(f"bad comic link, request fail: {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find_all("h1")[0].text
        if not os.path.exists(f"./download/{title}"):
            os.makedirs(f"./download/{title}")
            log_info(f"make folder {title}")
        else:
            log_warning(f"floder {title} already exists, new comic may replace former ones")
        img_list = soup.find_all("img", {"data-lazy-src": True})
        # clear irrelevent link
        img_link_list = [img['data-lazy-src'] for img in img_list if "cdn" in img['data-lazy-src']]
        img_cnt = 0                 # how many images
        img_len = 0                 # number of digits total_len have
        total_num = len(img_list)   # number of image in the list
        while total_num > 0:
            img_len = img_len + 1
            total_num = total_num // 10
        progress_bar(0, len(img_link_list)) # begin progress bar
        for img_link in img_link_list:
            log_info(f"deal with {img_link}")
            img_cnt = img_cnt + 1
            new_pic_name = f"{img_cnt}.jpg"
            current_len = 0
            tmp = img_cnt
            while tmp > 0:          # number of digits img_cnt have
                current_len = current_len + 1
                tmp =  tmp // 10
            while current_len < img_len:
                new_pic_name = "0" + new_pic_name
                current_len = current_len + 1
            img = requests.get(img_link, headers=headers)
            if not img.ok:
                log_error(f"bad img link {img_link}")
            else:
                with open(f"./download/{title}/{new_pic_name}", 'wb') as f:
                    f.write(img.content)
            progress_bar(img_cnt, len(img_link_list))
        print("\n")                         # finish progress bar


# input a string as keyword and it will return a list of pictures, each with corresponding urls
def get_comic_list(keyword, page):
    target = f"{base_url}/page/{page}?s={keyword}"
    response = requests.get(target, headers=headers)
    if not response.ok:
        log_error(f"request fail: {response.status_code}")
    else:
        log_info(f"request success: {response.status_code}")
        clear_yaml(database)
        write_comic(keyword, page, extract_cover_url(response), database)

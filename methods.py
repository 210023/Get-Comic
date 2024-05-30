from config import headers, base_url, database
import requests, base64, yaml
from bs4 import BeautifulSoup

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
        cover_addr = cover_section.find_all("img")[0]['src']
        comic_link = next(cover_section.find_all("h2", attrs={"class": "card_title"})[0].children)['href']
        comic_info.append({"cover": cover_addr, "link": comic_link})
    return comic_info

# input a string as keyword and it will return a list of pictures, each with corresponding urls
def get_comic_list(keyword, page):
    target = f"{base_url}/page/{page}?s={keyword}"
    response = requests.get(target, headers=headers)
    if not response.ok:
        print(f"request fail: {response.status_code}")
    else:
        print(f"request success: {response.status_code}")
        clear_yaml(database)
        write_comic(keyword, page, extract_cover_url(response), database)

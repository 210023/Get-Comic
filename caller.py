from requests.sessions import requote_uri
import yaml
from config import *
import requests

from methods import *

with open(database, "r", encoding='utf-8') as f:
    result = yaml.load(f.read(), Loader=yaml.FullLoader)

cover_link = result["comic list"][0]["cover"]
comic_link = result["comic list"][0]["link"]


target = gen_nyahentai(result["comic list"][1]["link"])
pic_download(target["img_link_list"], target["id"])
target = gen_nyahentai(result["comic list"][2]["link"])
pic_download(target["img_link_list"], target["id"])

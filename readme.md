### 2024.5.30

  last year, i wrote a python program to scratch ero pictures from [nyahentai.biz](https://nyahentai.biz) during my summer vacation. and it was not valiable cause i didn't copy it to my new device, so here i am going to rewrite it

  it requires requests, bs4, re and perhapes some other packages to run. requests can get page urls, then bs4 and re will get relevent content

  get_comic_list api gets keyword and page, if requests package goes well, it writes comic covers and its links to a yaml file which is named 'database' in config.py

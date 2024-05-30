### 2024.5.30

  last year, i wrote a python program to scratch ero pictures from [nyahentai.biz](https://nyahentai.biz) during my summer vacation. and it was not valiable cause i didn't copy it to my new device, so here i am going to rewrite it

  it requires requests, bs4, re and perhapes some other packages to run. requests can get page urls, then bs4 and re will get relevent content

  get_comic_list api gets keyword and page, if requests package goes well, it writes comic covers and its links to a yaml file which is named 'database' in config.py


  ### 2024.5.31

    **Implement program run in console mode**. The whole scratch progress is divided into two steps. In the first step, a keyword and a page number are provided to get a list of comics from nyahentai.biz. These information is stored in the comic_set.yaml, where a comic's cover, link, post id and title are composed as one dictionary component. During the second step, a ui based on gradio is avaliable. Method gen_nyahentai receives a specific comic page link, extracts relevent image link and return a list of links mentioned before. Call pic_download which receive the image list and its post id, a folder named with the post id will be created in "./download"(as a title might be too long and sometimes contains japanese characters that is not supported).

import gradio as gr
from config import *
import yaml
from methods import *

result = []
with open(database, "r", encoding='utf-8') as f:
    result = yaml.load(f.read(), Loader=yaml.FullLoader)
comic_list = result["comic list"]

with gr.Blocks() as preview:
    for comic in comic_list:
        id = comic["id"]
        title = comic["title"]
        with gr.Row():
            comic_title = gr.Textbox(show_copy_button=True, label=title, placeholder=id, interactive=False, autoscroll=False, min_width=1600)
    with gr.Row():
        chosen_id = gr.Textbox(label="id", interactive=True)
        download_btn = gr.Button("Download", interactive=True)
        def download(id):
            download_btn.interactive=False
            print(f"attempt download {id}")
            i = 0
            for comic in comic_list:
                if comic["id"] == id: break
                i = i + 1
            link = comic_list[i]["link"]
            pic_download(gen_nyahentai(link)["img_link_list"], id)
            download_btn.interactive=True
        download_btn.click(fn=download, inputs=chosen_id)





preview.launch()

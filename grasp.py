import gradio as gr
from methods import get_comic_list

with gr.Blocks() as grasp:
    with gr.Row():
        keyword = gr.Textbox(label="keyword")
        page = gr.Textbox(label="page")
    grasp_btn = gr.Button("Grasp")
    def on_click(keyword, page):
        get_comic_list(keyword, page)
    grasp_btn.click(fn=on_click, inputs=[keyword, page])

grasp.launch()

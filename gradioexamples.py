import gradio as gr
import numpy as np
import pandas as pd

# Authenticate with Google and get the sheet


def get_data():
    URL = "https://docs.google.com/spreadsheets/d/1UoKzzRzOCt-FXLLqDKLbryEKEgllGAQUEJ5qtmmQwpU/edit#gid=0"
    csv_url = URL.replace('/edit#gid=', '/export?format=csv&gid=')
    return pd.read_csv(csv_url)
# def get_data():
#     values = pd.read_csv(URL)
#     df = pd.DataFrame(values[1:], columns=values[0])
#     return df
with gr.Blocks() as demo:
    gr.Markdown("# 📈 Real-Time Line Plot")
    with gr.Row():
        with gr.Column():
            gr.DataFrame(get_data, every=5)
        with gr.Column():
            gr.LinePlot(get_data, every=5, x="Date", y="Sales", y_title="Sales ($ millions)", overlay_point=True, width=500, height=500)
demo.queue().launch()  #
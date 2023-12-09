import modules.scripts as scripts
from modules.paths_internal import models_path, data_path
from modules import script_callbacks, shared
from PIL import Image
import numpy as np
import gradio as gr
import requests
import os
import re
import subprocess
import threading


API_URL = "https://api.tzone03.xyz/"
ONLINE_DOCS_URL = API_URL + "docs/"
RESULT_PATH = "tmp/model-downloader-cn.log"
VERSION = "v1.1.4"


def check_aria2c():
    try:
        subprocess.run("aria2c", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def process_image(url):
    response = requests.get(url, stream=True)
    image = Image.open(response.raw)
    return image

def get_model_path(model_type):
    co = shared.cmd_opts
    pj = os.path.join
    MODEL_TYPE_DIR = {
        "Checkpoint": ["ckpt_dir", pj(models_path, 'Stable-diffusion', 'tmp_models')],
        "LORA": ["lora_dir", pj(models_path, 'Lora', 'tmp_Lora')],
        "TextualInversion": ["embeddings_dir", pj(data_path, 'embeddings')],
        "Hypernetwork": ["hypernetwork_dir", pj(models_path, 'hypernetworks')],
        # "AestheticGradient": "",
        # "Controlnet": "", #controlnet-dir
        "LoCon": ["lyco_dir", pj(models_path, 'LyCORIS')],
        "VAE": ["vae_dir", pj(models_path, 'VAE')],
    }

    dir_list = MODEL_TYPE_DIR.get(model_type)
    if dir_list == None:
        return None

    if hasattr(co, dir_list[0]) and getattr(co, dir_list[0]):
        return getattr(co, dir_list[0])
    else:
        return dir_list[1]


def request_civitai_detail(url):
    pattern = r'https://civitai\.com/models/(.+)'
    m = re.match(pattern, url)
    if not m:
        return False, "Jika Bukan tautan yang valid ke halaman model civitai, tidak didukung saat ini"

    req_url = API_URL + "civitai/models/" + m.group(1)
    res = requests.get(req_url)

    if res.status_code >= 500:
        return False, "Nah, layanan tampaknya sedang down, jadi secara teori saya seharusnya sedang mengusahakannya, jadi periksa dan lihat bagaimana perkembangannya.……"
    if res.status_code >= 400:
        return False, "Jika Bukan tautan yang valid ke halaman model civitai, tidak didukung untuk saat ini!"

    if res.ok:
        return True, res.json()
    else:
        return False, res.text

def resp_to_components(resp):
    if resp == None:
        return [None, None, None, None, None, None, None, None, None, None]

    img = resp["version"]["image"]["url"]
    if img:
        img = process_image(img)

    return [
        resp["name"],
        resp["type"],
        ", ".join(resp["version"]["trainedWords"]),
        resp["creator"]["username"],
        ", ".join(resp["tags"]),
        resp["version"]["updatedAt"],
        resp["description"],
        img,
        resp["version"]["file"]["name"],
        resp["version"]["file"]["downloadUrl"],
    ]


def preview(url):
    ok, resp = request_civitai_detail(url)
    if not ok:
        return [resp] + resp_to_components(None) + [gr.update(interactive=False)]

    has_download_file = False
    more_guides = ""
    if resp["version"]["file"]["downloadUrl"]:
        has_download_file = True
        more_guides = f'，Klik pada tombol unduh\n{resp["version"]["file"]["name"]}'


    return [f"Pratinjau Berhasil{more_guides}"] + resp_to_components(resp) + \
            [gr.update(interactive=has_download_file)]


def download(model_type, filename, url, image_arr):
    if not (model_type and url and filename):
        return "Informasi unduhan yang hilang"

    target_path = get_model_path(model_type)
    if not target_path:
        return f"Jenis ini tidak didukung saat ini：{model_type}"

    if isinstance(image_arr, np.ndarray) and image_arr.any() is not None:
        image_filename = filename.rsplit(".", 1)[0] + ".jpeg"
        target_file = os.path.join(target_path, image_filename)
        if not os.path.exists(target_file):
            image = Image.fromarray(image_arr)
            image.save(target_file)

    target_file = os.path.join(target_path, filename)
    if os.path.exists(target_file):
        return f"Sudah ada, tidak ada unduhan duplikat：\n{target_file}"


    cmd = f'curl -o "{target_file}" "{url}" 2>&1'
    if check_aria2c():
        cmd = f'aria2c -c -x 16 -s 16 -k 1M -d "{target_path}" -o "{filename}" "{url}" 2>&1'

    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="UTF-8"
    )
    status_output = ""
    if result.returncode == 0:
        status_output = f"Berhasil mengunduh, simpan ke：\n{target_file}\n{result.stdout}"
    else:
        status_output = f"Pengunduhan gagal. Pesan kesalahan.：\n{result.stdout}"

    return status_output

def on_ui_tabs():
    banner, footer = request_online_docs()

    with gr.Blocks() as ui_component:
        gr.Markdown(banner)
        with gr.Row() as input_component:
            with gr.Column():
                inp_url = gr.Textbox(
                    label="Alamat halaman model Civitai, bukan tautan unduhan.",
                    placeholder="sebanding https://civitai.com/models/28687/pen-sketch-style"
                )
                with gr.Row():
                    preview_btn = gr.Button("pratinjau")
                    download_btn = gr.Button("mengunduh", interactive=False)
                with gr.Row():
                    result = gr.Textbox(
                        # value=result_update,
                        label="Hasil implementasi",
                        interactive=False,
                        # every=1,
                    )
            with gr.Column() as preview_component:
                with gr.Row():
                    with gr.Column() as model_info_component:
                        name = gr.Textbox(label="nama", interactive=False)
                        model_type = gr.Textbox(label="tipologi", interactive=False)
                        trained_words = gr.Textbox(label="kata pemicu", interactive=False)
                        creator = gr.Textbox(label="penulis", interactive=False)
                        tags = gr.Textbox(label="tab (dari jendela) (komputasi)", interactive=False)
                        updated_at = gr.Textbox(label="Terakhir diperbarui", interactive=False)
                    with gr.Column() as model_image_component:
                        image = gr.Image(
                            show_label=False,
                            interactive=False,
                        )
                with gr.Accordion("Deskripsi", open=False):
                    description = gr.HTML()
        with gr.Row(visible=False):
            filename = gr.Textbox(
                visible=False,
                label="model_filename",
                interactive=False,
            )
            download_url = gr.Textbox(
                visible=False,
                label="model_download_url",
                interactive=False,
            )
        with gr.Row():
            gr.Markdown(f"rilis：{VERSION}\n\npenulis：@tzwm\n{footer}")
            gr.Markdown(f"Modifer：@vorstcavry\n{footer}")

        def preview_components():
            return [
                name,
                model_type,
                trained_words,
                creator,
                tags,
                updated_at,
                description,
                image,
            ]

        def file_info_components():
            return [
                filename,
                download_url,
            ]

        preview_btn.click(
            fn=preview,
            inputs=[inp_url],
            outputs=[result] + preview_components() + \
                file_info_components() + [download_btn]
        )
        download_btn.click(
            fn=download,
            inputs=[model_type] + file_info_components() + [image],
            outputs=[result]
        )

    return [(ui_component, "Unduh Model", "model_downloader_cn_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)

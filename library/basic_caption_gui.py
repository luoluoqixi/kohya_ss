import gradio as gr
from easygui import msgbox
import subprocess
from .common_gui import get_folder_path, add_pre_postfix, find_replace
import os


def caption_images(
    caption_text,
    images_dir,
    overwrite,
    caption_ext,
    prefix,
    postfix,
    find_text,
    replace_text,
):
    # Check for images_dir
    if not images_dir:
        msgbox('Image folder is missing...')
        return

    if not caption_ext:
        msgbox('Please provide an extension for the caption files.')
        return

    if caption_text:
        print(f'Captioning files in {images_dir} with {caption_text}...')
        run_cmd = f'python "tools/caption.py"'
        run_cmd += f' --caption_text="{caption_text}"'
        if overwrite:
            run_cmd += f' --overwrite'
        if caption_ext:
            run_cmd += f' --caption_file_ext="{caption_ext}"'
        run_cmd += f' "{images_dir}"'

        print(run_cmd)

        # Run the command
        if os.name == 'posix':
            os.system(run_cmd)
        else:
            subprocess.run(run_cmd)

    if overwrite:
        if prefix or postfix:
            # Add prefix and postfix
            add_pre_postfix(
                folder=images_dir,
                caption_file_ext=caption_ext,
                prefix=prefix,
                postfix=postfix,
            )
        if find_text:
            find_replace(
                folder_path=images_dir,
                caption_file_ext=caption_ext,
                search_text=find_text,
                replace_text=replace_text,
            )
    else:
        if prefix or postfix:
            msgbox(
                'Could not modify caption files with requested change because the "Overwrite existing captions in folder" option is not selected...'
            )

    print('...captioning done')


# Gradio UI
def gradio_basic_caption_gui_tab(headless=False):
    with gr.Tab('Basic Captioning (基本标注)'):
        gr.Markdown(
            'This utility will allow the creation of simple caption files for each image in a folder.'
        )
        with gr.Row():
            images_dir = gr.Textbox(
                label='Image folder to caption (标注图片的目录)',
                placeholder='Directory containing the images to caption',
                interactive=True,
            )
            folder_button = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not headless)
            )
            folder_button.click(
                get_folder_path,
                outputs=images_dir,
                show_progress=False,
            )
            caption_ext = gr.Textbox(
                label='Caption file extension (标注文件的后缀名)',
                placeholder='Extension for caption file. eg: .caption, .txt',
                value='.txt',
                interactive=True,
            )
            overwrite = gr.Checkbox(
                label='Overwrite existing captions in folder (覆盖已存在的标注)',
                interactive=True,
                value=False,
            )
        with gr.Row():
            prefix = gr.Textbox(
                label='Prefix to add to caption (添加前缀)',
                placeholder='(Optional)',
                interactive=True,
            )
            caption_text = gr.Textbox(
                label='Caption text (标注文本)',
                placeholder='Eg: , by some artist. Leave empty if you just want to add pre or postfix',
                interactive=True,
            )
            postfix = gr.Textbox(
                label='Postfix to add to caption (添加后缀)',
                placeholder='(Optional)',
                interactive=True,
            )
        with gr.Row():
            find_text = gr.Textbox(
                label='Find text （查找文本）',
                placeholder='Eg: , by some artist. Leave empty if you just want to add pre or postfix',
                interactive=True,
            )
            replace_text = gr.Textbox(
                label='Replacement text （替换文本）',
                placeholder='Eg: , by some artist. Leave empty if you just want to replace with nothing',
                interactive=True,
            )
            caption_button = gr.Button('Caption images')
            caption_button.click(
                caption_images,
                inputs=[
                    caption_text,
                    images_dir,
                    overwrite,
                    caption_ext,
                    prefix,
                    postfix,
                    find_text,
                    replace_text,
                ],
                show_progress=False,
            )

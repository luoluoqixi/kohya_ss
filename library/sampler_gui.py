import tempfile
import os
import gradio as gr
from easygui import msgbox

folder_symbol = '\U0001f4c2'  # 📂
refresh_symbol = '\U0001f504'  # 🔄
save_style_symbol = '\U0001f4be'  # 💾
document_symbol = '\U0001F4C4'   # 📄


###
### Gradio common sampler GUI section
###


def sample_gradio_config():
    with gr.Accordion('Sample images config （采样图片配置）', open=False):
        with gr.Row():
            sample_every_n_steps = gr.Number(
                label='Sample every n steps （每N步采样一次）',
                value=0,
                precision=0,
                interactive=True,
            )
            sample_every_n_epochs = gr.Number(
                label='Sample every n epochs（每N轮采样一次）',
                value=0,
                precision=0,
                interactive=True,
            )
            sample_sampler = gr.Dropdown(
                label='Sample sampler (采样方法)',
                choices=[
                    'ddim',
                    'pndm',
                    'lms',
                    'euler',
                    'euler_a',
                    'heun',
                    'dpm_2',
                    'dpm_2_a',
                    'dpmsolver',
                    'dpmsolver++',
                    'dpmsingle',
                    'k_lms',
                    'k_euler',
                    'k_euler_a',
                    'k_dpm_2',
                    'k_dpm_2_a',
                ],
                value='euler_a',
                interactive=True,
            )
        with gr.Row():
            sample_prompts = gr.Textbox(
                lines=5,
                label='Sample prompts (采样提示词)',
                interactive=True,
                placeholder='masterpiece, best quality, 1girl, in white shirts, upper body, looking at viewer, simple background --n low quality, worst quality, bad anatomy,bad composition, poor, low effort --w 768 --h 768 --d 1 --l 7.5 --s 28',
            )
    return (
        sample_every_n_steps,
        sample_every_n_epochs,
        sample_sampler,
        sample_prompts,
    )


def run_cmd_sample(
    sample_every_n_steps,
    sample_every_n_epochs,
    sample_sampler,
    sample_prompts,
    output_dir,
):
    output_dir = os.path.join(output_dir, 'sample')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    run_cmd = ''

    if sample_every_n_epochs == 0 and sample_every_n_steps == 0:
        return run_cmd

    # Create the prompt file and get its path
    sample_prompts_path = os.path.join(output_dir, 'prompt.txt')

    with open(sample_prompts_path, 'w') as f:
        f.write(sample_prompts)

    run_cmd += f' --sample_sampler={sample_sampler}'
    run_cmd += f' --sample_prompts="{sample_prompts_path}"'

    if not sample_every_n_epochs == 0:
        run_cmd += f' --sample_every_n_epochs="{sample_every_n_epochs}"'

    if not sample_every_n_steps == 0:
        run_cmd += f' --sample_every_n_steps="{sample_every_n_steps}"'

    return run_cmd

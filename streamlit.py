import streamlit as st
from PIL import Image
from streamlit.components.v1 import html
from pdf_utils import images_to_pdf
import base64
from io import BytesIO


def cropper(img: Image.Image, key: str):
    """Display simple drag-to-crop widget and return box coordinates."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    component = html(
        f"""
        <style>
        #container-{key} {{ position: relative; display: inline-block; }}
        #cropbox-{key} {{
            display: none;
            position: absolute;
            border: 2px dashed red;
            pointer-events: none;
        }}
        </style>
        <div id='container-{key}'>
            <img id='img-{key}' src='data:image/png;base64,{b64}' style='max-width:100%; display:block;'>
            <div id='cropbox-{key}'></div>
        </div>
        <script>
        (function() {{
            const img = document.getElementById('img-{key}');
            const box = document.getElementById('cropbox-{key}');
            let startX = 0, startY = 0, isDown = false;
            img.addEventListener('mousedown', e => {{
                const r = img.getBoundingClientRect();
                startX = e.clientX - r.left;
                startY = e.clientY - r.top;
                isDown = true;
                box.style.display = 'block';
                box.style.left = startX + 'px';
                box.style.top = startY + 'px';
                box.style.width = 0;
                box.style.height = 0;
            }});
            img.addEventListener('mousemove', e => {{
                if (!isDown) return;
                const r = img.getBoundingClientRect();
                const x = e.clientX - r.left;
                const y = e.clientY - r.top;
                const left = Math.min(startX, x);
                const top = Math.min(startY, y);
                const right = Math.max(startX, x);
                const bottom = Math.max(startY, y);
                box.style.left = left + 'px';
                box.style.top = top + 'px';
                box.style.width = (right - left) + 'px';
                box.style.height = (bottom - top) + 'px';
            }});
            window.addEventListener('mouseup', () => {{
                if (!isDown) return;
                isDown = false;
                const r = img.getBoundingClientRect();
                const left = parseFloat(box.style.left);
                const top = parseFloat(box.style.top);
                const width = parseFloat(box.style.width);
                const height = parseFloat(box.style.height);
                Streamlit.setComponentValue({{
                    left: Math.round(left * img.naturalWidth / r.width),
                    top: Math.round(top * img.naturalHeight / r.height),
                    right: Math.round((left + width) * img.naturalWidth / r.width),
                    bottom: Math.round((top + height) * img.naturalHeight / r.height)
                }});
            }});
            img.addEventListener('load', () => {{
                Streamlit.setComponentValue({{
                    left: 0,
                    top: 0,
                    right: img.naturalWidth,
                    bottom: img.naturalHeight
                }});
            }});
        }})();
        </script>
        """,
        height=400,
    )
    return component

st.title("PNG → PDF 変換ツール（Web）")

uploaded_files = st.file_uploader(
    "PNGファイルをアップロード（複数可）",
    type=["png", "PNG"],
    accept_multiple_files=True,
)

if uploaded_files:
    processed_images = []
    for file in uploaded_files:
        with Image.open(file) as img:
            st.image(img, caption=f"{file.name} (original)")
            with st.expander(f"編集: {file.name}"):
                coords = cropper(img, key=f"{file.name}_crop")
                rotation = st.slider(
                    "rotate (degrees)",
                    0,
                    270,
                    0,
                    step=90,
                    key=f"{file.name}_rot",
                )
                flip = st.checkbox("flip horizontally", key=f"{file.name}_flip")

            if isinstance(coords, dict):
                crop_box = (
                    coords.get("left", 0),
                    coords.get("top", 0),
                    coords.get("right", img.width),
                    coords.get("bottom", img.height),
                )
            else:
                crop_box = (0, 0, img.width, img.height)

            edited = img.crop(crop_box)
            if rotation:
                # PIL rotates counterclockwise by default
                edited = edited.rotate(-rotation, expand=True)
            if flip:
                edited = edited.transpose(Image.FLIP_LEFT_RIGHT)
            st.image(edited, caption=f"{file.name} (edited)")
            processed_images.append(edited.convert("RGB"))

    pdf_bytes = images_to_pdf(processed_images)

    st.download_button(
        "📄 PDFをダウンロード",
        pdf_bytes,
        file_name="converted.pdf",
    )

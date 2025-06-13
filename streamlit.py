import streamlit as st
from PIL import Image
from streamlit.components.v1 import html
from pdf_utils import images_to_pdf
import base64
from io import BytesIO


def cropper(img: Image.Image, key: str):
    """Display interactive cropper and return crop box coordinates."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    component = html(
        f"""
        <link rel='stylesheet' href='https://unpkg.com/cropperjs/dist/cropper.min.css'>
        <script src='https://unpkg.com/cropperjs/dist/cropper.min.js'></script>
        <img id='{key}' src='data:image/png;base64,{b64}' style='max-width:100%;'/>
        <script>
        const img = document.getElementById('{key}');
        const cropper = new Cropper(img, {{viewMode:1, autoCropArea:1}});
        function send() {{
          const d = cropper.getData(true);
          Streamlit.setComponentValue({{
            left: Math.round(d.x),
            top: Math.round(d.y),
            right: Math.round(d.x + d.width),
            bottom: Math.round(d.y + d.height)
          }});
        }}
        img.addEventListener('cropend', send);
        img.addEventListener('ready', send);
        </script>
        """,
        height=400,
        key=key,
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

            if coords:
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
            st.image(edited, caption=f"{file.name} (edited)")
            processed_images.append(edited.convert("RGB"))

    pdf_bytes = images_to_pdf(processed_images)

    st.download_button(
        "📄 PDFをダウンロード",
        pdf_bytes,
        file_name="converted.pdf",
    )

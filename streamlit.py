import streamlit as st
from PIL import Image
import io

st.title("PNG → PDF 変換ツール（Web）")

uploaded_files = st.file_uploader(
    "PNGファイルをアップロード（複数可）",
    type=["png", "PNG"],
    accept_multiple_files=True,
)

if uploaded_files:
    images = []
    for file in uploaded_files:
        with Image.open(file) as img:
            images.append(img.convert("RGB"))

    with io.BytesIO() as buf:
        images[0].save(buf, format="PDF", save_all=True, append_images=images[1:])
        pdf_bytes = buf.getvalue()

    st.download_button("📄 PDFをダウンロード", pdf_bytes, file_name="converted.pdf")

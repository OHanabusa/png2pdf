import streamlit as st
from PIL import Image
import io
from pdf_utils import images_to_pdf

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

    pdf_bytes = images_to_pdf(images)

    st.download_button("📄 PDFをダウンロード", pdf_bytes, file_name="converted.pdf")

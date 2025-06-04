import streamlit as st
from PIL import Image
import io

st.title("PNG → PDF 変換ツール（Web）")

uploaded_files = st.file_uploader("PNGファイルをアップロード（複数可）", type="png", accept_multiple_files=True)

if uploaded_files:
    images = [Image.open(file).convert("RGB") for file in uploaded_files]
    buf = io.BytesIO()
    images[0].save(buf, format="PDF", save_all=True, append_images=images[1:])
    st.download_button("📄 PDFをダウンロード", buf.getvalue(), file_name="converted.pdf")

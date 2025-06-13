import streamlit as st
from PIL import Image
from pdf_utils import images_to_pdf

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
            width, height = img.size
            with st.expander(f"編集: {file.name}"):
                left = st.slider(
                    "left",
                    0,
                    width - 1,
                    0,
                    key=f"{file.name}_left",
                )
                top = st.slider(
                    "top",
                    0,
                    height - 1,
                    0,
                    key=f"{file.name}_top",
                )
                right = st.slider(
                    "right",
                    left + 1,
                    width,
                    width,
                    key=f"{file.name}_right",
                )
                bottom = st.slider(
                    "bottom",
                    top + 1,
                    height,
                    height,
                    key=f"{file.name}_bottom",
                )
                rotation = st.slider(
                    "rotate (degrees)",
                    0,
                    270,
                    0,
                    step=90,
                    key=f"{file.name}_rot",
                )

            crop_box = (left, top, right, bottom)
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

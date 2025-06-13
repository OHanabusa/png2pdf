import streamlit as st
from PIL import Image
from pdf_utils import images_to_pdf
import numpy as np


def display_image_with_crop_sliders(img: Image.Image, key: str):
    """Display image with sliders for horizontal and vertical cropping."""
    # Get image dimensions
    width, height = img.size
    
    # Create columns for original and preview
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("元画像 (Original)")
        st.image(img, use_container_width=True)
    
    # Create sliders for horizontal cropping (left and right)
    st.write("水平方向のクロップ範囲 (Horizontal crop range)")
    h_crop = st.slider(
        "左右の範囲 (Left-Right)",
        0, width, (0, width),
        key=f"{key}_h_crop"
    )
    
    # Create sliders for vertical cropping (top and bottom)
    st.write("垂直方向のクロップ範囲 (Vertical crop range)")
    v_crop = st.slider(
        "上下の範囲 (Top-Bottom)",
        0, height, (0, height),
        key=f"{key}_v_crop"
    )
    
    # Create crop coordinates
    coords = {
        "left": h_crop[0],
        "right": h_crop[1],
        "top": v_crop[0],
        "bottom": v_crop[1]
    }
    
    # Show cropped preview
    with col2:
        st.write("クロッププレビュー (Crop Preview)")
        cropped_img = img.crop((coords["left"], coords["top"], coords["right"], coords["bottom"]))
        st.image(cropped_img, use_container_width=True)
    
    # Return crop coordinates
    return coords

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
            with st.expander(f"編集: {file.name}", expanded=True):
                coords = display_image_with_crop_sliders(img, key=f"{file.name}")
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

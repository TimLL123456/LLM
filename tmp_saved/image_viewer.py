import streamlit as st
import cv2

### repo: https://github.com/wjbmattingly/youtube-streamlit-image-grid

def sidebar_function():
    with st.sidebar:

        file_dir = st.text_input("Input file directory",
                                 "C:\\Users\\timom\\OneDrive\\圖片\\螢幕擷取畫面")
        

def display_image():
    st.image("C:\\Users\\timom\OneDrive\\\圖片\\螢幕擷取畫面\\test.jpg")
    pass

sidebar_function()
display_image()
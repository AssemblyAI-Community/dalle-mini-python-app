import streamlit as st
from dalle import create_and_show_images

st.title("DALL-E Mini")

text = st.text_input("What should I create?")

num_images = st.slider("How many images?", 1, 6)

ok = st.button("GO!")

if ok:
    create_and_show_images(text, num_images)

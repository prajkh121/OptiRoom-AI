import streamlit as st
from PIL import Image

st.set_page_config(page_title="OptiRoom: AI-Powered Interior Design", layout="wide")

st.title("🛋️ OptiRoom: Interior Design Generator")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

room_type = st.selectbox("Select Room Type", ["Bedroom", "Living Room", "Kitchen", "Bathroom"])
design_type = st.selectbox("Select Design Type", ["Modern", "Minimalistic", "Traditional", "Bohemian", "Industrial", "Rustic"])
additional_info = st.text_input("Additional Requirements (Optional)", "")

if uploaded_file:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="Uploaded Image", width=300)

if st.button("Submit Inputs"):
    if uploaded_file:
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["room_type"] = room_type
        st.session_state["design_type"] = design_type
        st.session_state["additional_info"] = additional_info
        st.success("Inputs saved! Go to the 'Send Input' page to view the data.")
    else:
        st.error("Please upload an image before submitting.")

import streamlit as st
from PIL import Image
import io

st.title("📤 Send Input Data")

if "uploaded_file" in st.session_state:
    st.subheader("Uploaded Image:")
    image_bytes = st.session_state["uploaded_file"].getvalue()
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Uploaded Image", width=300)

    st.subheader("Room Type:")
    st.write(st.session_state["room_type"])

    st.subheader("Design Type:")
    st.write(st.session_state["design_type"])

    st.subheader("Additional Requirements:")
    st.write(st.session_state["additional_info"])

    if st.button("Send Data"):
        st.success("✅ Data sent successfully!")
        input_data = {
            "room_type": st.session_state["room_type"],
            "design_type": st.session_state["design_type"],
            "additional_info": st.session_state["additional_info"],
        }
        st.json(input_data)
else:
    st.warning("No input data available. Go back and submit the form.")


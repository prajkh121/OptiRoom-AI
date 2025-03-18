import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from safetensors.torch import load_file
import io
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="OptiRoom: AI-Powered Interior Design", layout="wide")

# --- TITLE ---
st.title("🛋️ OptiRoom: AI-Powered Interior Design Generator")

# --- IMAGE UPLOAD ---
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# --- INPUT FORM ---
room_type = st.selectbox("Select Room Type", ["Bedroom", "Living Room", "Kitchen", "Bathroom"])
design_type = st.selectbox("Select Design Type", ["Modern", "Minimalistic", "Traditional", "Bohemian", "Industrial", "Rustic"])
additional_info = st.text_input("Additional Requirements (Optional)", "")

# --- PARAMETERS ---
strength = 0.75
steps = 50

# --- LOAD LoRA MODEL ---
@st.cache_resource
def load_pipeline():
    """Load the Stable Diffusion model and LoRA weights."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(device)

    # Load LoRA weights
    lora_path = "pages/model/interior-lora.safetensors"
    state_dict = load_file(lora_path)
    pipe.unet.load_state_dict(state_dict, strict=False)
    return pipe, device

# Load the model once and cache it
pipe, device = load_pipeline()

# --- GENERATE IMAGE ---
if st.button("Generate Interior Design") and uploaded_file:
    # Read uploaded image into PIL format
    image_bytes = uploaded_file.read()
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    input_image = input_image.resize((512, 512))  # Resize for consistency

    # Construct the prompt
    prompt = f"{room_type} with {design_type} and elegant interior design with {additional_info}"

    # Generate output image
    with st.spinner("Generating interior design..."):
        output_image = pipe(
            prompt=prompt,
            image=input_image,
            strength=strength,
            num_inference_steps=steps
        ).images[0]

    # --- DISPLAY INPUT AND OUTPUT IMAGES SIDE BY SIDE ---
    col1, col2 = st.columns(2)

    with col1:
        st.image(input_image, caption="Input Image", use_column_width=True)

    with col2:
        st.image(output_image, caption="Generated Image", use_column_width=True)

    # --- SAVE OUTPUT IMAGE ---
    output_path = "generated_interior.jpg"
    output_image.save(output_path)

    # --- DOWNLOAD BUTTON ---
    with open(output_path, "rb") as file:
        btn = st.download_button(
            label="Download Generated Image",
            data=file,
            file_name="interior_design.jpg",
            mime="image/jpeg"
        )

elif uploaded_file is None:
    st.warning("Please upload an image before generating.")

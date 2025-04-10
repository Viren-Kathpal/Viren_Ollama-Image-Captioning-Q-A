import streamlit as st
from PIL import Image
import ollama
import tempfile
import os

def save_image_temp(image):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "uploaded_image.png")
    image.save(temp_path, format="PNG")
    return temp_path

def generate_caption(image):
    image_path = save_image_temp(image)
    model = "llava"
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Please provide a detailed and accurate description of the image. If the image is blurry or unclear, mention that instead of giving false information.",
                "images": [image_path]
            }
        ]
    )
    return response.get("message", {}).get("content", "No description available.")

def answer_question(image, question):
    image_path = save_image_temp(image)
    model = "llava"
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Based on this image, answer the following question accurately: {question}",
                "images": [image_path]
            }
        ]
    )
    return response.get("message", {}).get("content", "No answer available.")

def main():
    st.title("Ollama Image Captioning and Q&A")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if "caption" not in st.session_state:
            st.session_state.caption = ""
        if "show_question_section" not in st.session_state:
            st.session_state.show_question_section = False
        if "questions" not in st.session_state:
            st.session_state.questions = []
        if "current_question" not in st.session_state:
            st.session_state.current_question = ""
        if "current_answer" not in st.session_state:
            st.session_state.current_answer = ""
        
        if st.button("Generate Caption"):
            st.session_state.caption = generate_caption(image)
            st.session_state.show_question_section = True
        
        st.write("**Caption:**", st.session_state.caption)
        
        if st.session_state.show_question_section:
            st.session_state.current_question = st.text_input("Ask a Question about the Image:", value="")
            if st.button("Get Answer") and st.session_state.current_question:
                st.session_state.current_answer = answer_question(image, st.session_state.current_question)
                st.write(f"**Q:** {st.session_state.current_question}")
                st.write(f"**A:** {st.session_state.current_answer}")

if __name__ == "__main__":
    main()
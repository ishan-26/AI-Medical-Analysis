from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(image, prompt):
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite", generation_config=generation_config)
    if image:
        response = model.generate_content([image[0], prompt])
    else:
       st.warning("Please upload the image")
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None

st.set_page_config(page_title="Diagnosis App")
st.header("Diagnosis App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

else:
    st.warning("Please upload the image")

submit = st.button("Tell me the diagnosis")

input_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.
Only respond if the image pertains to human health issues else respond with not appropriate image.

Analysis:

    Evaluation: Describe the anatomical structures visible in the image(s). Are there any unexpected findings, masses, or distortions?
    Pathological Evaluation: Based on the findings, is there evidence of any specific disease processes or abnormalities?
    If possible, narrow down the possibilities to a differential diagnosis (list of potential conditions).
    Urgency: Does the identified abnormality require immediate medical attention?
    Confidence Level: Express your confidence level in the analysis (high, medium, low).

Recommendations:

    Based on the analysis, recommend any additional tests or consultations that might be necessary for further evaluation.
    If a specific diagnosis is suspected, outline potential treatment options in general terms in a markdown manner.
    Here, avoid mentioning specific medications as they depend heavily on individual factors.
    Add disclaimer in bold letters.

Important Notes:
Scope of Response: Only respond if the image pertains to human health issues.
Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
Disclaimer: Accompany your analysis with the disclaimer:"Consult with a Doctor before making any decisions."
Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    if image_data:
        response = get_gemini_response(image_data, input_prompt)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload an image.")

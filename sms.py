import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
# import sys
import pandas as pd
from pathlib import Path
import os
from PIL import Image
import smtplib
from string import Template
from email.message import EmailMessage
from io import BytesIO
# from pathlib import path


# directory = sys.argv[1]
st.title("M_Ale Dashboard")
sub = st.text_input("Please enter the Subject.")
id = st.text_input("Please enter your email ID.")
password = st.text_input("Please enter your password")
bod = st.text_area("Please draft a body")
uploaded_file = st.file_uploader("Drag and Drop your mail recipient list here as csv.", type=["csv"], accept_multiple_files=False, label_visibility="visible")
but = st.button("Send")
html = Template(Path("index.html").read_text())


def upload_image_to_firebase_storage(image_object, destination_path):
    # Get a reference to the Firebase Storage bucket
    bucket = storage.bucket()
    try:
        # Upload the image object to Firebase Storage
        blob = bucket.blob(destination_path)
        blob.upload_from_file(BytesIO(image_object), content_type="png")  # Modify the content_type based on your image type

        print(f"Image uploaded to Firebase Storage at '{destination_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_shareable_link(image_path):
    # Get a reference to the Firebase Storage bucket
    bucket = storage.bucket()

    try:
        # Create a reference to the image file
        blob = bucket.blob(image_path)

        # Generate a signed URL with a validity of 1 hour
        url = blob.generate_signed_url(version='v4', expiration=3600)

        print(f"Shareable link for '{image_path}': {url}")
        return url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



if uploaded_file is not None and but == True and sub != "":
    cred = credentials.Certificate("male-8b6f5-firebase-adminsdk-qza06-e7d8fbd3e5.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'male-8b6f5.appspot.com'})
    
    directory = id.split("@")[0]

    if "." in directory:
        directory = directory.split(".")[0]
        
    if not os.path.exists(directory):
        os.makedirs(directory)

    no_img = len(os.listdir(directory)) + 1

    image = Image.new("RGBA", (100, 100), (200, 100, 50, 0))
    image.save(f'{directory}/{no_img}.png', 'png')

    if __name__ == "__main__":
        destination_path = f"Tracking_Pixel/{directory}/{no_img}.png"        # Replace with the desired destination path in the bucket
        upload_image_to_firebase_storage(image.tobytes(), destination_path)

        shareable_link = get_shareable_link(destination_path)

    df = pd.read_csv(uploaded_file, usecols=[0])
    st.dataframe(df)
    for index in df.to_numpy():
        mes = EmailMessage()
        mes["From"] = "kanwaldeep.puri@gmail.com"
        mes["Subject"] = sub
        mes["To"] = index
        mes.preamble = "This mail is Computer Generated please dont give a fuck!"
        mes.set_content(html.substitute({"img": directory, "img_chania" : str(no_img)}), "html")
        
        with smtplib.SMTP(host="smtp.gmail.com", port= 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("kanwaldeep.puri@gmail.com", "vtzzxtfobortpwhc")
            smtp.send_message(mes)
            print("message sent!!")

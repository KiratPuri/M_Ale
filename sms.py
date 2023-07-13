import streamlit as st
# import sys
import pandas as pd
from pathlib import Path
import os
from PIL import Image
import smtplib
from string import Template
from email.message import EmailMessage
# from pathlib import path
# directory = sys.argv[1]

directory = "dir"
if not os.path.exists(directory):
    os.makedirs(directory)

image = Image.new("RGBA", (100, 100), (200, 100, 50, 0))
image.save(f'{directory}.png', 'png')

st.title("M_Ale Dashboard")
sub = st.text_input("Please enter the Subject.")
bod = st.text_area("Please draft a body")
uploaded_file = st.file_uploader("Drag and Drop your mail recipient list here as csv.", type=["csv"], accept_multiple_files=False, label_visibility="visible")
but = st.button("Send")
html = Template(Path("index.html").read_text())
if uploaded_file is not None and but == True and sub != "":
    df = pd.read_csv(uploaded_file, usecols=[0])
    st.dataframe(df)
    for index in df.to_numpy():
        mes = EmailMessage()
        mes["From"] = "kanwaldeep.puri@gmail.com"
        mes["Subject"] = sub
        mes["To"] = index
        mes.preamble = "This mail is Computer Generated please dont give a fuck!"
        mes.set_content(html.substitute({"img_chania" : "charmander"}), "html")
        print(html.substitute({"img_chania" : "charmander"}))
        
        with smtplib.SMTP(host="smtp.gmail.com", port= 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("kanwaldeep.puri@gmail.com", "vtzzxtfobortpwhc")
            smtp.send_message(mes)
            print("message sent!!")




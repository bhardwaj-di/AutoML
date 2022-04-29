import streamlit as st
import os
import imageio
import io
import base64
import pandas as pd
from io import StringIO
import json
from google.cloud import storage
from google.oauth2 import service_account
import cv2



with open('./Credentials/fastapi-nowcast-349ba8715a42.json') as source:
    info = json.load(source)

credentials = service_account.Credentials.from_service_account_info(info)


def main():

    st.set_page_config(layout="wide")

    header = st.container()
    with header:
        st.title('Welcome to DSP weather forecasting')
        st.write("--------------------------------------------------------------------")
        uploaded_file = st.file_uploader("Choose a file")#,type = ['mp4','mov','wmv','avi'])
        if uploaded_file is not None:
            
            print(uploaded_file.name)
            cap = cv2.VideoCapture('/home/sudarshan/Downloads/' + uploaded_file.name)
            print(type(cap))
            """Uploads a file to the bucket."""
            # The ID of your GCS bucket
            bucket_name = "youtube_upload_bucket"
            # The path to your file to upload
            bytes_data = uploaded_file.getvalue()
            
            source_file_name = '/home/sudarshan/Downloads/'+ uploaded_file.name
            # The ID of your GCS object
            destination_blob_name = "Youtubevideo1"

            storage_client = storage.Client(credentials= credentials)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            #with open(source_file_name, 'rb') as f:
            blob.upload_from_filename(source_file_name)

            print(
                "File {} uploaded to {}.".format(
                    source_file_name, destination_blob_name
                )
            )
            st.write("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
            # To read file as bytes:
            #bytes_data = uploaded_file.getvalue()
            #st.write(bytes_data)

            # To convert to a string based IO:
            #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #st.write(stringio)

            # To read file as string:
            #string_data = stringio.read()
            #st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            #dataframe = pd.read_csv(uploaded_file)
            #st.write(dataframe)

main()
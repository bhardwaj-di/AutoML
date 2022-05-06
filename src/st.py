# streamlit_app.py
import streamlit as st
import pickle
import os
import re
import imageio
import io
import base64
import pandas as pd
import json
from google.cloud import storage
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import credentials, firestore
from os import listdir
from pytube import YouTube
from os.path import isfile, join
import toml

with open('../data/Credentials/fastapi-nowcast-349ba8715a42.json') as source:
    info = json.load(source)

credentialls = service_account.Credentials.from_service_account_info(info)

if not firebase_admin._apps:

    cred = credentials.Certificate("../data/Credentials/fastapi-nowcast-firebase-adminsdk-48a9r-85bb2191a6.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True



def ytlinks():
    videos = scrapetube.get_channel("UCupvZG-5ko_eiXAupbDfxWw")
    # print(type(videos))
    video_links = []
    for video in videos:
        #print(video['videoId'])
        video_links.append(video['videoId'])
        if len(video_links)==6:
            break
    
    return video_links

def show_ytlinks():

    loaded_dict = {}
    with open('../data/thumbnails.pickle', 'rb') as handle:
        loaded_dict = pickle.load(handle)


    ct = 0
    tab1, tab2 = st.columns(2)
    for k,v in loaded_dict.items():
        if(ct%2 == 0):
            tab1.write('https://www.youtube.com/watch?v='+k)
            image = v
            # image.show()
            tab1.image(image,caption = 'Video ' + str(ct + 1))
            
            ct = ct + 1
        else:
            tab2.write('https://www.youtube.com/watch?v='+k)
            image = v
            # image.show()
            tab2.image(image,caption = 'Video ' + str(ct + 1))
            ct = ct + 1

def download_ytvideo(link_to_download):
    yt = YouTube(link_to_download)
    mp4_files = yt.streams.filter(file_extension="mp4")
    mp4_360p_files = mp4_files.get_by_resolution("360p")
    mp4_360p_files.download("../data/YoutubeVideo/")
    


def upload_video_link(link_to_download):
    
    
    download_ytvideo(link_to_download)
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "youtube_upload_bucket"
    # The path to your file to upload
    onlyfiles = [f for f in listdir('../data/YoutubeVideo/') if isfile(join('../data/YoutubeVideo/', f))]
    source_file_name = onlyfiles[0]
    filename = source_file_name
    # The ID of your GCS object
    destination_blob_name = source_file_name

    storage_client = storage.Client(credentials= credentialls)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename('../data/YoutubeVideo/' +source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

    if os.path.exists('../data/YoutubeVideo/' + source_file_name):
        os.remove('../data/YoutubeVideo/' + source_file_name)
    else:
        print("The file does not exist")
    return filename

def upload_video_file(uploaded_file):

    print(uploaded_file)
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "youtube_upload_bucket"
    # The path to your file to upload
    bytes_data = uploaded_file.getvalue()
    
    source_file_name = uploaded_file.name
    filename = source_file_name
   
    with open('../data/UploadedVideo/' + source_file_name,'wb') as bf:
        bf.write(bytes_data)
    # The ID of your GCS object
    destination_blob_name = source_file_name

    storage_client = storage.Client(credentials= credentialls)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    #with open(source_file_name, 'rb') as f:
    blob.upload_from_filename('../data/UploadedVideo/' +source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    #st.write("File {} uploaded to {}.".format(os.getcwd() + '/UploadedVideo/' +source_file_name , destination_blob_name))
    if os.path.exists('../data/UploadedVideo/' + source_file_name):
        os.remove('../data/UploadedVideo/' + source_file_name)
    else:
        print("The file does not exist")
    return filename



def create_new_user(email,password,handle):
    data = {}
    input_file_name = ".streamlit/secrets.toml"
    with open(input_file_name) as toml_file:
        toml_dict = toml.load(toml_file)
        data = toml_dict

    user = email
    pwd = password
    handle_user = handle
    output_file_name = ".streamlit/secrets.toml"
    with open(output_file_name, "w") as toml_file:
        data_new = data['passwords']
        data_handle = data['handles']
        data['passwords'].update({user : pwd})
        data['handles'].update({user : handle_user})
        print(data)
        toml.dump(data, toml_file)

def get_youtube_link_id(link_to_download):

    if (('youtube.com' in link_to_download) or ('youtu.be'in link_to_download)):
        yt_id = re.split("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)",link_to_download)[1]
        if('&feature' in yt_id):
            yt_id = re.split("([\w\-\_]*)",yt_id)[1]
            return yt_id
        else:
            return yt_id
    else:
        yt_id = "nan"
        return yt_id


def concat_link(yt_id):
    if(yt_id == None):
        pass
    else:
        yt_link = 'https://www.youtube.com/watch?v=' + yt_id
        return yt_link


st.set_page_config(layout="wide")

header = st.container()
authenticate_userr = st.container()

with header:

        st.title('Welcome to DSP Business meeting Summarization!')
        st.write("--------------------------------------------------------------------")


with authenticate_userr:
    # Authentication
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up','Logout'])

    # Sign up Block
    if choice == 'Sign up':
        # Obtain User Input for email and password
        email = st.sidebar.text_input('Please enter your email address')
        password = st.sidebar.text_input('Please enter your password',type = 'password')
        handle = st.sidebar.text_input('Please input your app handle name', value='Default')
        submit = st.sidebar.button('Create my account')

        if submit:
           
            create_new_user(email,password,handle)
            st.success('Your account is created suceesfully!')
            st.balloons()
           
            st.title('Welcome' + handle)
            st.info('Login via login drop down selection')
        st.session_state["password_correct"] = False


    if choice == 'Login':
        if check_password():
            
            
            show_ytlinks()

            link_to_download = st.text_input('Enter a Youtube link to Summarize:')
            yt_id = get_youtube_link_id(link_to_download)
            if(yt_id == 'nan'):
                st.write("Link cannot be passed as we only support youtube as of now")
                link_to_download = 'nan'
            else:
                link_to_download = concat_link(yt_id)

            st.header('OR')
            st.write('Note : If you are uploading the file Please keep the LINK text box empty!!')
            
            uploaded_file = st.file_uploader("Choose a file",type = ['mp4','mov','wmv','avi','mkv'])


            summary = st.button("Summarize")
            
            if summary:
                
                if uploaded_file is None:
                    if not link_to_download:
                        st.write('Nothing to Show')
                    elif(link_to_download == 'nan'):
                        st.write("No results to show")
                        
                    else:
                        st.write(link_to_download)
                        filename = upload_video_link(link_to_download)
                        filename = filename.split('.')[0] 
                        print('Now for summarry: '+ filename )
                        doc_ref = db.collection('Summarizer').document(filename)
                        doc = doc_ref.get()
                        now = doc.exists
                        while not now:
                            doc = doc_ref.get()
                            if(doc.exists):
                                now = True
                
                        print('got file')
                        summarize_dtext = doc_ref.get().to_dict()
                        for key,val in zip (summarize_dtext.keys(),summarize_dtext.values()):
                            st.write("Speaker :" + key)
                            st.write(val)
                
                        

                if uploaded_file is not None:                    
                    filename = upload_video_file(uploaded_file)
                    filename = filename.split('.')[0]
                    print('Now for summarry: '+ filename )
                    doc_ref = db.collection('Summarizer').document(filename)
                    doc = doc_ref.get()
                    now = doc.exists
                    while not now:
                        doc = doc_ref.get()
                        if(doc.exists):
                            now = True
                        
                    print('got file')
                    summarize_dtext = doc_ref.get().to_dict()
                    for key,val in zip (summarize_dtext.keys(),summarize_dtext.values()):
                        st.write("Speaker :" + key)
                        st.write(val)
                    uploaded_file = None
            
    if choice == 'Logout':
                
                st.markdown('Log out successfully')
                st.session_state["password_correct"] = False
            
                
            

                
                


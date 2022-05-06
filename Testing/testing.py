import toml
import scrapetube
import yt as ytb
import re
import os
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import speech
import json
import firebase_admin
from firebase_admin import credentials, firestore

source = {
  "type": os.environ['GCP_TYPE'] ,
  "project_id": os.environ['GCP_PROJECT_ID'] ,
  "private_key_id":os.environ['GCP_PRIVATE_KEY_ID'] ,
  "private_key": os.environ['GCP_PRIVATE_KEY'] ,
  "client_email": os.environ['GCP_CLIENT_EMAIL'] ,
  "client_id": os.environ['GCP_CLIENT_ID'] ,
  "auth_uri": os.environ['GCP_AUTH_URI'] ,
  "token_uri": os.environ['GCP_TOKEN_URI'] ,
  "auth_provider_x509_cert_url": os.environ['GCP_AUTH_PROVIDER_X509_CERT_URL'] ,
  "client_x509_cert_url": os.environ['GCP_CLIENT_X509_CERT_URL'] 
}


source_new = {
  "type": os.environ['FIREBASE_TYPE'] ,
  "project_id": os.environ['FIREBASE_PROJECT_ID'] ,
  "private_key_id":os.environ['FIREBASE_PRIVATE_KEY_ID'] ,
  "private_key": os.environ['FIREBASE_PRIVATE_KEY'] ,
  "client_email": os.environ['FIREBASE_CLIENT_EMAIL'] ,
  "client_id": os.environ['FIREBASE_CLIENT_ID'] ,
  "auth_uri": os.environ['FIREBASE_AUTH_URI'] ,
  "token_uri": os.environ['FIREBASE_TOKEN_URI'] ,
  "auth_provider_x509_cert_url": os.environ['FIREBASE_AUTH_PROVIDER_X509_CERT_URL'] ,
  "client_x509_cert_url": os.environ['FIREBASE_CLIENT_X509_CERT_URL'] 
}


credentialls = service_account.Credentials.from_service_account_info(source)

if not firebase_admin._apps: 
    #cred = credentials.Certificate(source_new)
    firebase_admin.initialize_app(source_new)

#info = json.load(source)

db = firestore.client()
collection = db.collection('Audio_to_text')  # opens 'places' collection
doc = collection.document('link')  # specifies the 'rome' document

def check_password(user,pwd):
    """Returns `True` if the user had a correct password."""

    def check_user(dict, key):
        
        if key in dict:
            #print(key)
            return key
        else:
            print("Not present")
    
    def check_userpassword(dict, key):
        
        if key in dict:
            val = dict.get(key)
            #print(val)
            return val
        else:
            print("Not Value")

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        data = {}
        input_file_name = "/Testing/secrets.toml"
        with open(input_file_name) as toml_file:
            toml_dict = toml.load(toml_file)
            data = toml_dict
        data = data['passwords']
        if ( (user == check_user(data,user)) and (pwd == check_userpassword(data,user)) ):
            password_correct = 1
            print('correct username and password')
            return password_correct
        else:
            password_correct = 0
            print('incorrect username and password')
            return password_correct


    if password_entered() == 0:
        # Password incorrect.
        return 0
    else:
        # Password correct.
        return 1


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


def get_youtube_link_id(link_to_download):

    if (('youtube.com' in link_to_download) or ('youtu.be'in link_to_download)):
        yt_id = re.split("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)",link_to_download)[1]
        if('&feature' in yt_id):
            yt_id = re.split("([\w\-\_]*)",yt_id)[1]
            return yt_id
        else:
            return yt_id
    else:
        # Not a valid link!!
        yt_id = 'NNNNNNN'
        return yt_id

def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    

    client = speech.SpeechClient(credentials= credentialls)

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        audio_channel_count = 2,
        language_code="en-US",
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
    
    return response.results


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client(credentials= credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def retrive_text(filename):
    doc_ref = db.collection('Audio_to_text').document(filename)
    doc = doc_ref.get()
    now = doc.exists
    while not now:
        doc = doc_ref.get()
        if(doc.exists):
            now = True

    print('got file')
    summarize_dtext = doc_ref.get().to_dict()
    return summarize_dtext

def push_Data(link,data):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    db.collection(u'Audio_to_text').document(str(link)).set(data)
    res = retrive_text(link)
    if(len(res)>0):
        return 1
    else:
        return 0


def test_login_correct_credentials():
    user = 'dsp'
    pwd = 'bigdata'
    assert check_password(user,pwd) == 1 

def test_login_incorrect_credentials():
    user = 'random'
    pwd = 'random123'
    assert check_password(user,pwd) == 0 

def test_get_ytlinks():
    list_of_links = ytlinks()
    assert len(list_of_links) > 0

def test_get_youtube_link_id():
    link_to_download = 'https://www.youtube.com/watch?v=cUKXWQmkk3Y'
    id_yt = get_youtube_link_id(link_to_download)
    assert id_yt == 'cUKXWQmkk3Y'

def test_incorrect_link():
    link_to_download = 'https://towardsdatascience.com/'
    id_yt = get_youtube_link_id(link_to_download)
    assert id_yt == 'NNNNNNN'

def test_transcribe_file():
    speech_file = '/Testing/data/Test1minute_new.flac'
    result = transcribe_file(speech_file)
    assert len(result)> 0

def test_retrive_text():
    
    filename = 'Judge holds former President Trump in civil contempt-8QmCQN7k-80'
    result = retrive_text(filename)
    assert len(result)> 0

def test_push_text():
    filename = 'Judge holds former President Trump in civil contempt-8QmCQN7k-80'
    data = {'samp':'HEY!!'}
    result = push_Data(filename,data)
    assert result == 1

test_login_correct_credentials()
test_login_incorrect_credentials()
test_get_ytlinks()
test_get_youtube_link_id()
test_incorrect_link()
test_transcribe_file()
test_retrive_text()
test_push_text()
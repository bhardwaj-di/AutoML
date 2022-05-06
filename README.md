# Business Meeting Summarization


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


![image](https://user-images.githubusercontent.com/62667964/163837223-b5c76de9-7717-41a9-81e1-d6dbb30c653e.png)


## Objetive
The main aim of our project is to summarize business meetings, speaker diarization that will be processed into text synopsis, and build a fully functional data pipeline to provide a brief summary of meetings using GCP services and demonstrating insights in a reference web application.


> - Who - Business meetings, Student counsel, General Audience
> - What - Performing data wrangling and converting the input files to a specific audio format and store in a GCP bucket, creating a pipeline in which the audio first gets converted to 16000 Hz and then gets divided into chunks. Each chunk will be parallely sent to a Speech-to-text API and the result json will be then grouped into blobs based on the speaker. This data will be then summarized based on the speaker and as a total and will be passed to the user.
> - What - Over two weeks period timeline
> - Where - This project can be useful for any people or groups who missed the event and  want to get a short summary of the meeting held.
> - How - Implementing the project using Google cloud services like Bigquery, GCP bucket ,compute engine, GCP audio to text API and visualizations tools and applications like Streamlit & Locust or pytest.


## Team Information

| NAME              |     NUID        |
|-------------------|-----------------|
| Sudarshan Waydande|   001563532     |
| Divyanshu Bhardwaj|   002181815     |
| Prasanth Dwadasi  |   002115654     |


#### Quick Links

#### Web Application <br />
[Bizmeeting.website](http://bizmeeting.website/)


##### Project Proposal <br />
[Codelab](https://codelabs-preview.appspot.com/?file_id=19He61kjHAlpOpN0jEHL6G-H6mrsCFkyoYnUn37YTwlA#0)


##### Unit Testing <br />
[Document](https://docs.google.com/document/d/1N8h1MzA2c00Lgu0EDx5PJQGAeN9ENLDuuEGjDwZ3CeI/edit?usp=sharing)

##### Demonstrating our application <br />

[Demo](https://screenrec.com/share/3td1vE6P8S)

---

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
- [TestCases](#testcases)


## Introduction


#### Architecture 

![alt text](https://github.com/bhardwaj-di/Busines_meeting_summarization/blob/main/images/Architecture.png)

- A Scalable Data Pipeline for Summarizing video and audio, performing Speaker Diarization, with code executing on serverless google cloud functions and with all the components deployed oncompenents Google Cloud. Sending an e-mail to the customer at the end with a pdf containing the summary of all the speakers.

---

## Setup

The pipeline requires an Google cloud platform account to deploy and run. You must have an active accoung of GCP to use the services. The pipeline uses the folllowing GCP Services:

- Cloud function 
- Google VM instances
- GCP Bucket
- Firestore
- Speech-to-Text API
- Cloud Monitoring
- Pub/Sub

Other than GCP services we are using:

- Airflow
- Streamlit

Create a service account and enable the above mentioned API's
Follow this [Getting started](https://cloud.google.com/docs/get-started) documnetation for more information

1. Clone the repository using the command `git clone git@github.com:bhardwaj-di/Busines_meeting_summarization.git`

2. Create a virtual environment and Install the necessary packages and libraries from requirements.txt 

```
source activate <env>
pip3 install -r requirements.txt
```

3. By now you must already have an active GCP account , set up your gcp cli following instructions from [here](https://cloud.google.com/sdk/docs/install-sdk)

4. Create 3 buckets with names `youtube_upload_bucket` , `preprocessed_audio` and `model-storage` for storing files and model

5. You can create a bucket directly from website or through command line , for creation of bucket refer [gcp-bucket creation](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-cli)


6.

#### Deploying Cloud Functions 

The pipeline extensively uses Google Cloud Functions for Serverless Computing. All directories inside cloud functions directory are Lambda functions that have to be deployed on GCP. All functions follow a common deployment process. 

#### Deploy serverless Python code in GCP

  - Enable Cloud function API on your GCP `gcloud services enable cloudfunctions.googleapis.com` or through cloud console
  - We use seperate triggers for each cloud function which triggers the next event in the pipeline
  - To create a cloud function open the cloud functions console and fill the details as mentioned below
  ![creating cloud functiion](https://github.com/bhardwaj-di/Busines_meeting_summarization/blob/main/images/creating_cloud_function.png)
  - We have created a function `audio_preprocesing` which triggers when a new object has been uploaded to the `youtube_upload_bucket`
  - Similarly create another function `transcribe_audio` which triggers when a new object has been uploaded to the `preprocessed_audio`

  ![creating cloud functiion](https://github.com/bhardwaj-di/Busines_meeting_summarization/blob/main/images/transcribe_audio.png)
  
7. Enable the Firestore Database API in cloud console and create two new collections `Audio_to_text` and `Summarizer`
![Firestore](https://github.com/bhardwaj-di/Busines_meeting_summarization/blob/main/images/Firestore.png)

8. Setup another two cloud functions `summary` and `sendMail` which are responsible for summarizing the audio and sending a mail to user
after the pdf with summary was generated
![summary](https://github.com/bhardwaj-di/Busines_meeting_summarization/blob/main/images/summary.png)
![sendmail](https://github.com/bhardwaj-di/Busines_meeting_summarization/blob/main/images/sendmail.png)

9. Start the apache airflow by running scheduler and webserver

```
airflow webserver
airflow scheduler
python airflow/dags/generated_thumbnail.py
```

10. Now run the streamlit webapplication st.py inside the src folder

`streamlit run st.py`

11. Open the website [bizmeeting.website](http://bizmeeting.website/) and Signup

12. You are now ready to use the application

---

## TestCases

All Test Cases have been documented [here](https://docs.google.com/document/d/1N8h1MzA2c00Lgu0EDx5PJQGAeN9ENLDuuEGjDwZ3CeI/edit?usp=sharing)

Streamlit App can be accessed using this link: [Business Meeting Summarization | WebApp](http://bizmeeting.website/)

The pipeline can be tested with the video links displayed in the website. The video links are preiodically updated using an Airflow function.
Additonally any URL can be entered in the Streamlit app and results can be seen. 



![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)








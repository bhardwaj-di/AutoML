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
[Bizmeeting.website](bizmeeting.website)


##### Project Proposal <br />
[Codelab](https://codelabs-preview.appspot.com/?file_id=19He61kjHAlpOpN0jEHL6G-H6mrsCFkyoYnUn37YTwlA#0)


##### Unit Testing <br />
[Document](https://docs.google.com/document/d/1N8h1MzA2c00Lgu0EDx5PJQGAeN9ENLDuuEGjDwZ3CeI/edit?usp=sharing)

---

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
- [TestCases](#testcases)


## Introduction


#### Architecture 

![alt text](https://github.com/bhardwaj-di/Busines_meeting_summarization/images/Architecture.png)

- A Scalable Data Pipeline for Summarizing video and audio, performing Speaker Diarization, with code executing on serverless google cloud functions and with all the components deployed oncompenents Google Cloud. Sending an e-mail to the customer at the end with a pdf containing the summary of all the speakers.

---

## Setup

The pipeline requires an Google cloud platform account to deploy and run. You must have an active accoung of GCP to use the services. The pipeline uses the folllowing GCP Services:

- Cloud function 
- Google VM instances
- GCP Bucket
- Firestore
- Sppech-to-Text API
- Cloud Monitoring
- Pub/Sub

Create a service account and enable the above mentioned API's
Follow this [Getting started](https://cloud.google.com/docs/get-started) documnetation for more information




## TestCases

All Test Cases have been documented [here](https://docs.google.com/document/d/1N8h1MzA2c00Lgu0EDx5PJQGAeN9ENLDuuEGjDwZ3CeI/edit?usp=sharing)

Streamlit App can be accessed using this link: [Business Meeting Summarization | WebApp](http://bizmeeting.website/)

The pipeline can be tested with the video links displayed in the website. The video links are preiodically updated using an Airflow function.
Additonally any URL can be entered in the Streamlit app and results can be seen. 



![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)








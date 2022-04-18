# Business Meeting Summarization

![image](https://user-images.githubusercontent.com/62667964/163837223-b5c76de9-7717-41a9-81e1-d6dbb30c653e.png)


# Objetive
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

Project Proposal
https://codelabs-preview.appspot.com/?file_id=19tJ6F57N0Kxlcfh7sNTYj2OAWB0DcLX8hSqym6N2TdA



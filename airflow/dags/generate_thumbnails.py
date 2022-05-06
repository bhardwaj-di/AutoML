from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import urllib.request
from PIL import Image
import pickle
import scrapetube
import pendulum



def ytlinks():
    videos = scrapetube.get_channel("UCupvZG-5ko_eiXAupbDfxWw")
    # print(type(videos))
    video_links = []
    for video in videos:
        print(video['videoId'])
        video_links.append(video['videoId'])
        if len(video_links)==6:
            break
    video_thumbnails= {}
    for v in video_links:
        data= urllib.request.urlretrieve("http://img.youtube.com/vi/"+v+"/0.jpg")
        image= Image.open(data[0])
        video_thumbnails[v] = image
    with open('../data/thumbnails.pickle', 'wb') as handle:
        pickle.dump(video_thumbnails, handle, protocol=pickle.HIGHEST_PROTOCOL)


with DAG(dag_id="generate_thumbnails",
         start_date=pendulum.datetime(2022,5,5,tz='EST'),
         schedule_interval="@hourly",
         catchup=False) as dag:

        task1 = PythonOperator(
        task_id="ytlinks",
        python_callable=ytlinks)

task1

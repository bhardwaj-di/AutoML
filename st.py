import streamlit as st
import scrapetube
import ytscrape as yt
from PIL import Image
import urllib.request

header = st.container()
body = st.container()

with header:
    st.header('DSP Business go')


with body:
    videolist = yt.ytlinks()
    for v in videolist:
        st.write('https://www.youtube.com/watch?v='+v)
        data = urllib.request.urlretrieve("http://img.youtube.com/vi/"+v+"/0.jpg")
        image = Image.open(data[0])
        # image.show()
        (st.image(image))

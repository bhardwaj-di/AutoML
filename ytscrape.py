import scrapetube


def ytlinks():
    videos = scrapetube.get_channel("UCupvZG-5ko_eiXAupbDfxWw")
    # print(type(videos))
    video_links = []
    for video in videos:
        print(video['videoId'])
        video_links.append(video['videoId'])
        if len(video_links)==5:
            break
    
    return video_links


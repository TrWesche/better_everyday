import requests
from key import API_KEY

rootURL = "https://api.pexels.com/videos"


def get_video(video_id: int):
    headers={
        "Content-Type":"application/json",
        "Authorization":API_KEY
    }    

    resp = requests.get(f"{rootURL}/videos/{video_id}", headers=headers)
    
    return resp


def search_videos(query_str: str):
    headers={
        "Content-Type":"application/json",
        "Authorization":API_KEY
    } 

    resp = requests.get(f"{rootURL}/search?{query_str}", headers=headers)

    return resp


def get_popular_videos():
    headers={
        "Content-Type":"application/json",
        "Authorization":API_KEY
    } 

    resp = requests.get(f"{rootURL}/popular", headers=headers)

    return resp
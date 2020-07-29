import requests
from .key import API_KEY

rootURL = "https://api.pexels.com/v1"


def get_photo(photo_id: int):
    headers={
        "Content-Type":"application/json",
        "Authorization":API_KEY
    }    

    resp = requests.get(f"{rootURL}/photos/{photo_id}", headers=headers)
    
    return resp


def search_photos(query_str: str):
    headers={
        "Content-Type":"application/json",
        "Authorization":API_KEY
    } 

    resp = requests.get(f"{rootURL}/search?{query_str}", headers=headers)

    return resp


def get_curated_photos():
    headers={
        "Content-Type":"application/json",
        "Authorization":API_KEY
    } 

    resp = requests.get(f"{rootURL}/curated", headers=headers)

    return resp
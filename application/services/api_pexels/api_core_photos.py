import requests
from os import environ
# from .key import API_KEY

API_KEY = environ.get('PEXELS_API_KEY')

rootURL = "https://api.pexels.com/v1"

def create_headers():
    headers = {
        "Content-Type":"application/json",
        "Authorization":API_KEY
    }
    return headers

def get_photo(photo_id: int):
    headers = create_headers()

    resp = requests.get(f"{rootURL}/photos/{photo_id}", headers=headers)
    
    return resp


def search_photos(query_str: str):
    headers = create_headers()

    resp = requests.get(f"{rootURL}/search?{query_str}", headers=headers)

    return resp


def get_curated_photos():
    headers = create_headers()

    resp = requests.get(f"{rootURL}/curated", headers=headers)

    return resp
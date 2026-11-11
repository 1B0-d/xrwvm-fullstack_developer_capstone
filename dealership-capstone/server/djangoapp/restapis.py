# Uncomment the imports below before you add the function code
import requests
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    response = requests.get(backend_url.rstrip('/') + endpoint, params=kwargs, timeout=10)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    url = sentiment_analyzer_url.rstrip('/') + '/analyze/' + quote(text, safe='')
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def post_review(data_dict):
    response = requests.post(backend_url.rstrip('/') + '/insert_review', json=data_dict, timeout=10)
    response.raise_for_status()
    return response.json()

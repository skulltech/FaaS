import requests


def ip():
    return requests.get("https://api.ipify.org/").text

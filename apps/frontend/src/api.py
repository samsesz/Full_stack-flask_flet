import requests

BASE_URL = "http://127.0.0.1:5000/api"


def get_houses():
    response = requests.get(f"{BASE_URL}/houses/")

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    return response.json()


def get_dragons():
    response = requests.get(f"{BASE_URL}/dragons/")
    return response.json()


def get_characters():
    response = requests.get(f"{BASE_URL}/characters/")
    return response.json()


def get_swords():
    response = requests.get(f"{BASE_URL}/swords/")
    return response.json()
import requests
from urllib.parse import quote

def word_to_image(word, filename=None):
    url = f"https://image.pollinations.ai/prompt/{quote(word)}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(filename or f"{word}.jpg", "wb") as f:
        f.write(r.content)

word_to_image("hi")
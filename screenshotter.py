import requests
from PIL import ImageGrab, Image
from time import sleep
import io
import base64
import json
import os

wait = 5  # loop interval
url = "http://localhost/post"
headers = {
    "Content-Type": "application/json"
}

print(os.getcwd())

with open(f"{os.getcwd()}\\.auth.txt") as f:
    auth = f.readline()

print(auth)

while True:
    img = ImageGrab.grab()
    img = img.resize((1280, 720), Image.ANTIALIAS)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="png", optimize=True, quality=80)
    img_b64 = base64.b64encode(img_bytes.getvalue())
    img_b64_str = img_b64.decode("utf-8")

    print(img_b64_str[:10])

    try:
        resp = requests.post(
            url, data=json.dumps({"auth": auth, "img_b64_str": img_b64_str}), headers=headers)

        print(resp.json())
    except Exception as ex:
        print("REQUESTS EXCEPTION:", ex)

    sleep(wait)

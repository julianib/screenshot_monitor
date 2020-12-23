from flask import Flask, render_template, request
import base64
from PIL import Image
import random
import time
import socket
import os

app = Flask(__name__, static_url_path="/static", static_folder="static")

v = 0
last_update = 0

with open(f"{os.getcwd()}\\.auth.txt") as f:
    auth = f.readline()

print("IP:", socket.gethostbyname(socket.gethostname()))


@app.route("/")
def main():
    return render_template("index.html", random_version=v, last_update=last_update)


@app.route("/post", methods=["POST"])
def post():
    try:
        data = request.json
        print("got json data")
        if data["auth"] != auth:
            print("unauthorized")
            return {"response": "unauthorized"}

        time_now = time.time()
        img_b64_str = data["img_b64_str"]
        img_b64 = bytes(img_b64_str, "utf-8")
        img_bytes = base64.b64decode(img_b64)
        with open(f"{os.getcwd()}\\static\\image.png", "wb") as f:
            f.write(img_bytes)
        print("wrote to image.png")
        global v
        v = time_now
        global last_update
        last_update = time.strftime("%H:%M:%S", time.gmtime(time_now))

        # print(type(request.get_json()))
    except Exception as ex:
        print(ex)
        raise

    return {"response": "ok"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)

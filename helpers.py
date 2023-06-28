import requests

def upload_image(file):
    data = requests.post("https://freeimage.host/api/1/upload", {
        "key": "6d207e02198a847aa98d0a2a901485a5",
        "source": file
    })
    print(data.json())
    return data.json()["image"]["url"]
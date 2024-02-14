import json
import requests
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

import requests
import json

def test_txt2img():
    print("================================test2")

    ENDPOINT = "http://127.0.0.1:8000/image/txt2img"

    data = {
        "prompt": 'a photo of a dog sitting on a bench',
        "width": 128,
        "height": 128,
        "num_inference_steps": 10,
        "guidance_scale": 1,
        "num_outputs": 2,
        "seed": 0
    }

    print("================================test3")


    response = requests.post(url=ENDPOINT, json=data)
    print("==============================================")
    print(response['images']['base64'])
    print("==============================================")

    def b64_to_pil(input):
        output = Image.open( BytesIO( base64.b64decode( input ) ) )
        return output

    images = response[ 'images' ]


    return images

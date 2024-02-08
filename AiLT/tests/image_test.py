import json
import requests
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

import requests
import json

def test_txt2img():
    ENDPOINT = "http://127.0.0.1:8000/image/txt2img"

    data = {
        'prompt': 'a photo of a dog sitting on a bench',
        'width': 512,
        'height': 512,
        'num_inference_steps': 100,
        'guidance_scale': 7.5,
        'num_outputs': 2,
        'seed': 0,
    }

    response = requests.post(url=ENDPOINT, json=data)
    print("==============================================")
    print(response.json())
    print("==============================================")

    def b64_to_pil(input):
        output = Image.open( BytesIO( base64.b64decode( input ) ) )
        return output

    images = response[ 'images' ]


    return images

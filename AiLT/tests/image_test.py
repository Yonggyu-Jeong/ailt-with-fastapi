import json
import requests
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


def test_txt2img():
    ENDPOINT = "http://127.0.0.1:8000/image/txt2img"

    data = {
        'prompt': 'a photo of a dog sitting on a bench',
        'width': str(512),
        'height': str(512),
        'num_inference_steps': str(100),
        'guidance_scale': str(7.5),
        'num_outputs': str(2),
        'seed': str(0),
    }

    response = json.loads(requests.post(url=ENDPOINT, data=data).text)
    print("==============================================")
    print(response)
    print("==============================================")




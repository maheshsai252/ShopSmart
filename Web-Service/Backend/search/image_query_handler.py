from PIL import Image
from openai import OpenAI
import base64
import os
import json
from helpers.download_file import download_from_s3
def resize_image(image_path, output_size):
    try:
        img = Image.open(image_path)
        img_resized = img.resize(output_size)
        img_resized.save(image_path)
        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False
client = OpenAI(api_key=os.getenv('openai_key'))

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

instruction = """
Give the description of product that user is refering to in image in single sentence. 
You need to format the query to help user finding useful products.
Ignore the person you are seeing in image, describe only the product that user is talking about. 
The product could be clothing, watches and shoes. 
You can consider gender of person to identify category from:
['men_clothing', 'women_clothing', 'men_shoes','women_shoes', 'men_watches', 'women_watches']
Give your answer in below format:\n
{
    "category": "one of categories given",
    "query": "user query about product considering image"
}
"""

def handle_image(file_path,text):
    file = download_from_s3(file_path)
    resources = os.path.join(os.getcwd(), 'resources')
    file_path = os.path.join(resources, file)
    resize_image(file_path, (224, 224))
    base64_image = encode_image(file_path)
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages = [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": instruction+text
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ]
    )
    res = {}
    try:
       res = json.loads(response.choices[0].message.content)
    except Exception as e:
       print(str(e))
    return res
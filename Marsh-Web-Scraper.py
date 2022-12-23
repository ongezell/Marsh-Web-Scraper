import requests
import time
import os
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from PIL.Image import UnidentifiedImageError

url = input("Enter the URL of the website you want to download images from: ")
download_all = input("Do you want to download all images from the website (including those not using the img tag)? (y/n) ")
quality = int(input("Enter the quality of the converted images (in percentage, from 10 to 100): "))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
response = requests.get(url, headers=headers)
html = response.text

import re
if download_all == "y":
       image_urls = re.findall('(https://.*?)[\'"\)]', html)
else:
      image_urls = re.findall('img src="(https://.*?)"', html)

counter = 0
for image_url in tqdm(image_urls, "Saving images"):
    response = requests.get(image_url)
    image_data = response.content
    
    try:
        image = Image.open(BytesIO(image_data))
    except UnidentifiedImageError:
        continue
    
    filename = str(counter) + ".webp"
    
   image.save(filename, "webp", quality=quality)
   counter += 1

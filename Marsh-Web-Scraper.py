import requests
import time
import os
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from PIL.Image import UnidentifiedImageError

# Prompt the user for the URL of the website they want to download images from
url = input("Enter the URL of the website you want to download images from: ")

# Prompt the user to choose whether to download only images using the img tag or all images from the website
download_all = input("Do you want to download all images from the website (including those not using the img tag)? (y/n) ")

# Prompt the user for the quality of the converted images (in percentage)
quality = int(input("Enter the quality of the converted images (in percentage, from 10 to 100): "))

# Use requests to download the HTML of the website
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
response = requests.get(url, headers=headers)
html = response.text

# Use a regular expression to find all the image URLs in the HTML
import re
if download_all == "y":
    # Find all image URLs in the HTML
    image_urls = re.findall('(https://.*?)[\'"\)]', html)
else:
    # Find only image URLs in the img tag
    image_urls = re.findall('img src="(https://.*?)"', html)

# Iterate over the image URLs and download each image
counter = 0
for image_url in tqdm(image_urls, "Saving images"):
    # Use requests to download the image
    response = requests.get(image_url)
    image_data = response.content
    
    # Check if the image data is in a supported format
    try:
        image = Image.open(BytesIO(image_data))
    except UnidentifiedImageError:
        # Skip the image if it is not in a supported format
        continue
    
    # Generate a unique filename based on the counter variable
    filename = str(counter) + ".webp"
    
    # Use Pillow to open the image and convert it to the webp format
    image.save(filename, "webp", quality=quality)
    
    # Increment the counter variable
    counter += 1

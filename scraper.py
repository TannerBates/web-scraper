import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download an image
def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

# Function to resize an image while maintaining aspect ratio
def resize_image(image, size):
    image.thumbnail(size, Image.LANCZOS)
    return image

# Function to save an image to a specified folder
def save_image(image, url, folder):
    try:
        filename = os.path.join(folder, os.path.basename(url))
        image.save(filename)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Failed to save image {url}: {e}")

# Main function to scrape images
def scrape_images(url, folder='images', size=(900, 900)):
    create_directory(folder)
    
    # Fetch the web page
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Extract and process image URLs
    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            # Skip if the src attribute is missing
            continue
        # Handle relative URLs
        img_url = urljoin(url, img_url)
        
        # Download the image
        image = download_image(img_url)
        if image:
            # Resize the image
            resized_image = resize_image(image, size)
            # Save the resized image
            save_image(resized_image, img_url, folder)

# Example usage
website_url = "https://example.com/"
scrape_images(website_url)
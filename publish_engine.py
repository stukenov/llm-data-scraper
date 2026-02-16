# publish engine

import os
import uuid
import requests
import logging
from datetime import datetime
from db import ScraperDatabase
import time

def download_image(image_url):
    response = requests.get(image_url)
    file_extension = os.path.splitext(os.path.basename(image_url))[1].split('?')[0]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = os.path.join('img', unique_filename)
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path

def get_access_token():
    url = os.environ.get('PUBLISH_API_TOKEN_URL')
    data = {
        'username': os.environ.get('PUBLISH_USERNAME'),
        'password': os.environ.get('PUBLISH_PASSWORD')
    }
    if not all([url, data['username'], data['password']]):
        logging.error("Publishing credentials not configured in environment variables")
        return None
    response = requests.post(url, data=data)
    if response.status_code != 200:
        logging.error(f"Failed to get access token: {response.status_code} - {response.text}")
        return None
    return response.json().get('access', '').encode('utf-8').decode('utf-8')

def publish_to_myqaz(title, description, content, image_path, access_token):
    url = os.environ.get('PUBLISH_API_URL')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    files = {'image': open(image_path, 'rb')}
    data = {
        'title': title,
        'description': description,
        'body': content,
        'pub_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    response = requests.post(url, headers=headers, data=data, files=files)
    if response.status_code != 201:
        logging.error(f"Failed to publish to myqaz: {response.status_code} - {response.text}")
    return response.status_code

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    scraper_db = ScraperDatabase()
    logging.info("Starting publish engine")
    logging.info("Getting content for publish")
    try:
        content = scraper_db.get_content_for_publish()
    except Exception as e:
        logging.error(f"Failed to get content for publish: {e}")
        return
    if not content:
        logging.info("No content for publish")
        return
    logging.info("Content for publish: {content}")
    try:
        content_title = content['generated_title']
    except Exception as e:
        logging.error(f"Failed to get content title: {e}")
        return
    try:
        content_description = content['generated_description']
    except Exception as e:
        logging.error(f"Failed to get content description: {e}")
        return
    try:
        content_content = content['rewritten_content']
    except Exception as e:
        logging.error(f"Failed to get content content: {e}")
        return
    try:
        content_image_url = content['og_image_url']
    except Exception as e:
        logging.error(f"Failed to get content image url: {e}")
        return
    try:
        image_path = download_image(content_image_url)
        if not image_path:
            image_path = 'img/noimage.jpg'
    except Exception as e:
        logging.error(f"Failed to download image: {e}")
        image_path = 'img/noimage.jpg'
        
    try:
        access_token = get_access_token()
    except Exception as e:
        logging.error(f"Failed to get access token: {e}")
        return
    try:
        response = publish_to_myqaz(content_title, content_description, content_content, image_path, access_token)
    except Exception as e:
        logging.error(f"Failed to publish to myqaz: {e}")
        return
    logging.info(f"Published to myqaz: {response}")
    try:
        scraper_db.update_content_publish_status(content['id'], True)
    except Exception as e:
        logging.error(f"Failed to update content publish status: {e}")
        return

if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)

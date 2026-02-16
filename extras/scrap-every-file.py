import os
import requests

# Ensure the eurosports directory exists
os.makedirs('eurosports', exist_ok=True)

# Read the links from the CSV file
with open('links.csv', 'r') as file:
    next(file)  # Skip the header
    links = [line.strip() for line in file]

import time

from bs4 import BeautifulSoup

# Iterate over the links and save the text content inside <div id="content"> to a separate file
for link in links:
    try:
        response = requests.get(link)
        if response.status_code == 200:
            # Parse the page content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the <div> with id 'content'
            content_div = soup.find('div', id='content')
            if content_div:
                # Extract text from the content_div, removing HTML tags
                content_text = content_div.get_text(separator=' ', strip=True)
                # Generate a filename based on the current Unix timestamp
                timestamp = int(time.time())
                filename = f'{timestamp}'
                # Save the text content to a file in the eurosports directory
                with open(f'eurosports/{filename}.txt', 'w', encoding='utf-8') as f:
                    f.write(content_text)
                print(f'Saved {filename}.txt')
            else:
                print(f'Content not found in {link}')
        else:
            print(f'Failed to retrieve {link}. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'An error occurred while fetching {link}: {e}')

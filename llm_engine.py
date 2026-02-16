import json
import requests
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)

LLM_URL: str = os.environ.get('LLM_API_URL', 'http://localhost:11434/api/generate')

def request_to_llm(prompt: str, model: str) -> str:
    logging.info(f"Preparing to send request to LLM with model {model}")
    data: str = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    try:
        logging.info("Sending POST request to LLM")
        response: requests.Response = requests.post(LLM_URL, data=data, verify=False)
        response.raise_for_status()
        logging.info("POST request successful, processing response")
        response_text: str = response.json()['response']
        return response_text
    except requests.RequestException as e:
        logging.error(f"Error generating response: {e}")
        return "Failed to generate response"

def request_title(full_text: str) -> str:
    logging.info("Requesting title generation")
    model = os.environ.get('LLM_TITLE_MODEL', 'llama2')
    title_response: str = request_to_llm(full_text, model)
    return title_response

def request_content(full_text: str) -> str:
    logging.info("Requesting content rewriting")
    model = os.environ.get('LLM_REWRITER_MODEL', 'llama2')
    content_response: str = request_to_llm(full_text, model)
    return content_response

def request_description(full_text: str) -> str:
    logging.info("Requesting description creation")
    model = os.environ.get('LLM_DESCRIPTION_MODEL', 'llama2')
    description_response: str = request_to_llm(full_text, model)
    return description_response

while True:
    logging.info("Starting content processing loop")
    import time
    time.sleep(10)
    from db import ScraperDatabase
    scraper_db: ScraperDatabase = ScraperDatabase()
    content: dict = scraper_db.get_content_for_parse()
    if not content:
        logging.info("No content for parse")
        sys.exit()

    scraped_content: str = content['scraped_content']
    rewritten_content: str = request_content(scraped_content)
    if not rewritten_content:
        logging.error("Failed to rewrite content")
        sys.exit()

    # logging.info(f"Content (first 200 characters): {rewritten_content[:200]}")

    title: str = request_title(rewritten_content)
    if not title:
        logging.error("Failed to generate title")
        sys.exit()
    # title = title.strip().replace('"', '').replace('«', '').replace('»', '')
    # logging.info(f"Title: {title}")

    description: str = request_description(rewritten_content)
    if not description:
        logging.error("Failed to generate description")
        sys.exit()
    # description = description.strip().replace('"', '').replace('«', '').replace('»', '')
    # logging.info(f"Description: {description}")

    try:
        write_rewritten_content_response: bool = scraper_db.write_rewritten_content(
            original_content=scraped_content, 
            generated_title=title, 
            generated_description=description, 
            rewritten_content=rewritten_content, 
            url=content['url'], 
            og_image_url=content['og_image_url'], 
            publish_date=content['created_at']
        )
        logging.info("Rewritten content written to database")
    except Exception as e:
        logging.error(f"An error occurred while writing rewritten content to database: {e}")

    try:
        is_parsed: bool = scraper_db.mark_content_as_parsed(content['url'])
        logging.info(f"Content marked as parsed: {is_parsed}")
    except Exception as e:
        logging.error(f"An error occurred while marking content as parsed: {e}")


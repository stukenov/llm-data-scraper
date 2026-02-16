import subprocess
import logging
import json
import os

class Scraper:
    def __init__(self):
        shot_scraper_path = os.environ.get('SHOT_SCRAPER_PATH', 'shot-scraper')
        self.command_template = f"""
            {shot_scraper_path} javascript "{{url}}" "
            async () => {{{{
                const readability = await import('https://cdn.skypack.dev/@mozilla/readability');
                const readableContent = new readability.Readability(document).parse();
                {{additional_js}}
            }}}}"
            """
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_text_content(self, url):
        command = self.command_template.format(
            url=url,
            additional_js="return { textContent: readableContent.textContent };"
        )
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"Command failed with return code {result.returncode}")
            return None

        try:
            parsed_json = json.loads(result.stdout)
            return parsed_json.get('textContent')
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None

    def get_title(self, url):
        command = self.command_template.format(
            url=url,
            additional_js="""
                const title = document.querySelector('meta[property=\\"og:title\\"]') ? document.querySelector('meta[property=\\"og:title\\"]').content : '';
                return { title };
            """
        )
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"Command failed with return code {result.returncode}")
            return None

        try:
            parsed_json = json.loads(result.stdout)
            return parsed_json.get('title')
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None
    
    def get_og_image(self, url):
        command = self.command_template.format(
            url=url,
            additional_js="""
                const ogImage = document.querySelector('meta[property=\\"og:image\\"]') ? document.querySelector('meta[property=\\"og:image\\"]').content : '';
                return { ogImage };
            """
        )
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"Command failed with return code {result.returncode}")
            return None

        try:
            parsed_json = json.loads(result.stdout)
            return parsed_json.get('ogImage')
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None

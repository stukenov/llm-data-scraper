import subprocess
import os
import pdfplumber
import logging
import sys
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub


logging.basicConfig(level=logging.INFO)

def convert_to_txt(file_path):
    logging.info(f"Starting conversion of {file_path} to text")
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            pages = pdf.pages
            text_content = ''.join([page.extract_text() for page in pages])
        with open(f'{file_path[:-4]}.txt', 'w', encoding='utf-8') as f:
            f.write(remove_line_breaks(text_content))
        logging.info(f"PDF conversion completed for {file_path}")
    elif file_path.endswith('.epub'):

        book = epub.read_epub(file_path)
        content = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                content.append(soup.get_text())
        text_content = '\n'.join(content)
        with open(f'{file_path[:-5]}.txt', 'w', encoding='utf-8') as f:
            f.write(remove_line_breaks(text_content))
        logging.info(f"EPUB conversion completed for {file_path}")

def remove_line_breaks(text):
    logging.debug("Removing line breaks from text content")
    return text.replace('\n', ' ')


def clean_file_contents(input_filename, output_filename):
    """Clean the file contents by allowing only specified characters."""
    logging.info(f"Cleaning the contents of {input_filename} and saving to {output_filename}")

    allowed_chars = set('\n !(),-.0123456789?АаӘәБбВвГгҒғДдЕеЁёЖжЗзИиЙйКкҚқЛлМмНнҢңОоӨөПпРрСсТтУуҰұҮүФфХхҺһЦцЧчШшЩщЪъЫыІіЬьЭэЮюЯя')

    with open(input_filename, 'r', encoding='utf-8') as input_file, \
         open(output_filename, 'w', encoding='utf-8') as output_file:
        line_count = 0
        char_count = 0
        for line in input_file:
            cleaned_line = ''.join(filter(allowed_chars.__contains__, line))
            output_file.write(cleaned_line)
            line_count += 1
            char_count += len(cleaned_line)
            logging.debug(f"Processed {line_count} lines and {char_count} characters...")
    logging.info("Cleaning complete. The cleaned contents have been saved.")

def reduce_multiple_spaces_and_dots(input_filename, output_filename):
    """Replace multiple spaces with a single space and multiple dots with a single dot."""
    logging.info(f"Reducing spaces and dots in {input_filename} and saving to {output_filename}")

    with open(input_filename, 'r', encoding='utf-8') as input_file, \
         open(output_filename, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            line = line.replace('  ', ' ')
            line = line.replace('..', '.')
            output_file.write(line)
    logging.info("Reduction complete. The file has been saved.")

def insert_line_breaks(input_filename, output_filename):
    """Insert a line break after every '. ' in the text."""
    logging.info(f"Inserting line breaks in {input_filename} and saving to {output_filename}")

    with open(input_filename, 'r', encoding='utf-8') as input_file, \
         open(output_filename, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            line = line.replace('. ', '.\n')
            output_file.write(line)
    logging.info("Line break insertion complete. The file has been saved.")


def main():
    logging.info("Starting main process")
    if not os.path.exists('cleaned'):
        os.makedirs('cleaned')
    books = [book for book in os.listdir('books') if book != '.DS_Store' and not book.endswith('.docx')]

    for book in books:
        book_path = os.path.join('books', book)
        cleaned_book_path = os.path.join('cleaned', book)
        try:
            if book.endswith('.pdf') or book.endswith('.epub'):
                logging.info(f"Converting {book} to text")
                convert_to_txt(book_path)
                os.remove(book_path)
                logging.info(f"Removed original file {book_path}")
                book = os.path.splitext(book)[0] + '.txt'
                book_path = os.path.join('books', book)
                cleaned_book_path = os.path.join('cleaned', book)
            if not os.path.exists(os.path.dirname(cleaned_book_path)):
                os.makedirs(os.path.dirname(cleaned_book_path))
            clean_file_contents(book_path, cleaned_book_path)
            reduce_multiple_spaces_and_dots(cleaned_book_path, cleaned_book_path)
            insert_line_breaks(cleaned_book_path, cleaned_book_path)
            os.remove(cleaned_book_path)
            logging.info(f"Processed and removed cleaned file {cleaned_book_path}")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
    logging.info("Main process completed")

if __name__ == '__main__':
    main()

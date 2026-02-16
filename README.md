# LLM Data Scraper

A production-ready web scraping pipeline designed for collecting and processing content for Large Language Model (LLM) training datasets. This modular system automates the entire workflow from content discovery to data preparation, with built-in support for content rewriting and publishing.

## Features

- **Intelligent Content Extraction**: Uses Mozilla Readability for clean, semantic content extraction
- **Sitemap Processing**: Automatically discovers and processes XML sitemaps from multiple news sources
- **Database Management**: Efficient SQLite-based storage with duplicate detection
- **LLM Integration**: Built-in support for content rewriting and enhancement using LLM APIs
- **Publishing Pipeline**: Automated content publishing with image handling
- **Modular Architecture**: Clean separation of concerns for easy maintenance and extension

## Architecture

The scraper consists of several interconnected components:

1. **Scraper Engine** (`scraper.py`): Core web scraping functionality using shot-scraper and Readability
2. **Sitemap Parser** (`parse_sitemaps.py`, `sitemap_processor.py`): Automated discovery of new content from XML sitemaps
3. **Database Layer** (`db.py`): Data persistence and state management
4. **LLM Engine** (`llm_engine.py`): Content processing and rewriting using LLM APIs
5. **Publishing Engine** (`publish_engine.py`): Automated content publishing with media handling
6. **Orchestration** (`scrap_engine.py`): Main workflow coordinator

## Installation

### Prerequisites

- Python 3.7+
- [shot-scraper](https://github.com/simonw/shot-scraper) - Headless browser automation tool

### Setup

1. Clone the repository:
```bash
git clone https://github.com/stukenov/llm-data-scraper.git
cd llm-data-scraper
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install shot-scraper:
```bash
pip install shot-scraper
shot-scraper install
```

4. Configure environment variables (create `.env` file):
```bash
# Optional: Custom shot-scraper path
SHOT_SCRAPER_PATH=/path/to/shot-scraper

# LLM API Configuration (defaults to local Ollama)
LLM_API_URL=http://localhost:11434/api/generate
LLM_TITLE_MODEL=llama2
LLM_REWRITER_MODEL=llama2
LLM_DESCRIPTION_MODEL=llama2

# Publishing API Configuration (optional)
PUBLISH_API_URL=https://your-api.com/api/news/
PUBLISH_API_TOKEN_URL=https://your-api.com/api/token/
PUBLISH_USERNAME=your_username
PUBLISH_PASSWORD=your_password
```

## Usage

### Basic Scraping

Run the main scraping engine to continuously monitor and scrape content:

```bash
python scrap_engine.py
```

This will:
- Monitor configured news sources via their sitemaps
- Extract new articles using Readability
- Store content in the local SQLite database
- Mark processed articles to avoid duplicates

### Custom Sitemap Sources

To add new content sources, edit `parse_sitemaps.py`:

```python
@classmethod
def parse_your_source(cls):
    return cls.process_news(
        "https://example.com/sitemap.xml",
        condition=cls.your_condition,
        sitemap_sort_type='DESC',
        url_sort_type='DESC'
    )

@classmethod
def your_condition(cls, loc):
    return 'sitemap.news' in loc
```

Then add it to the sources list in `scrap_engine.py`:

```python
sources = [
    # ... existing sources
    ('your_source', parse_sitemaps.parse_your_source),
]
```

### LLM Processing

Process scraped content with LLM models:

```bash
python llm_engine.py
```

This will:
- Fetch unprocessed content from the database
- Generate optimized titles
- Rewrite content for quality and style
- Create SEO-friendly descriptions

### Publishing

Publish processed content:

```bash
python publish_engine.py
```

## Database Schema

The scraper uses SQLite with the following main tables:

### `links` table
- `id`: Primary key
- `url`: Article URL (unique)
- `source`: Content source identifier
- `scraped_content`: Raw extracted text
- `og_image_url`: Open Graph image URL
- `is_parsed`: Processing status flag
- `created_at`: Timestamp
- `action_type`: Processing action type

### `rewritten_content` table
- `id`: Primary key
- `original_content`: Original scraped text
- `generated_title`: LLM-generated title
- `generated_description`: LLM-generated description
- `rewritten_content`: LLM-rewritten content
- `url`: Source URL
- `og_image_url`: Associated image
- `publish_date`: Original publication date
- `is_published_to_site`: Publishing status

## Configuration

### Scraper Settings

Modify the scraper behavior by editing class parameters:

```python
# In scraper.py
class Scraper:
    def __init__(self):
        # Customize command template, timeouts, etc.
```

### Database Configuration

Database URLs can be customized in `db.py`:

```python
class ScraperDatabase:
    def __init__(self, db_url='sqlite:///scraper.db'):
        self.db_url = db_url
```

## Development

### Project Structure

```
llm-data-scraper/
├── scraper.py              # Core scraping functionality
├── scrap_engine.py         # Main orchestration loop
├── llm_engine.py           # LLM integration
├── publish_engine.py       # Publishing automation
├── db.py                   # Database layer
├── parse_sitemaps.py       # Sitemap parsers
├── sitemap_processor.py    # XML processing utilities
├── utils.py                # Helper functions
├── extras/                 # Additional utilities (see below)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md              # This file
```

### Extras Directory

The `extras/` directory contains additional standalone scraping and preprocessing tools:

- **scrap-every-file.py**: Batch scraper that reads URLs from a CSV file and extracts content from `<div id="content">` elements
- **small-scraper.py**: Simple scraper for extracting article links from Eurosport Football pages
- **parse.py**: Generic news parser with BeautifulSoup for extracting `<article>` tags
- **get-wiki-data.py**: Wikipedia data extractor using the Wikipedia API
- **convert-books.py**: Book format converter (PDF/EPUB to TXT) with text cleaning for Kazakh language
- **convert.py**: Video-to-audio converter using FFmpeg (requires external utils module)

These tools are provided as standalone utilities and may require additional dependencies not listed in the main requirements.txt.

### Adding New Features

The modular design makes it easy to extend functionality:

1. **New scrapers**: Add methods to `Scraper` class
2. **New sources**: Add parsers to `ParseSitemaps` class
3. **New LLM tasks**: Add functions to `llm_engine.py`
4. **New publishing targets**: Modify `publish_engine.py`

## Error Handling

The system includes comprehensive logging at all levels:

- **DEBUG**: Detailed execution traces
- **INFO**: Normal operation status
- **ERROR**: Exceptions and failures

Logs are output to console with timestamps and can be redirected to files.

## Performance Considerations

- **Rate Limiting**: Built-in delays between requests to respect server resources
- **Duplicate Detection**: Database-level URL uniqueness prevents redundant scraping
- **Incremental Processing**: Only new content is processed, skipping previously seen URLs
- **Resource Cleanup**: Proper database connection management

## Dependencies

- **shot-scraper**: Headless browser automation and JavaScript execution
- **requests**: HTTP client for API calls and downloads
- **dataset**: Simple database abstraction for SQLite

See `requirements.txt` for complete dependency list.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- [Mozilla Readability](https://github.com/mozilla/readability) for content extraction
- [shot-scraper](https://github.com/simonw/shot-scraper) by Simon Willison for browser automation
- The open-source community for various tools and libraries used in this project

## Disclaimer

This tool is for educational and research purposes. Always respect website terms of service, robots.txt files, and applicable laws when scraping content. The authors are not responsible for misuse of this software.

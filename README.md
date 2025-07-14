# Quotes Scraping Tutorial

This project demonstrates how to scrape quotes from [quotes.toscrape.com](http://quotes.toscrape.com) and store them in a SQLite database using Python, BeautifulSoup, and SQLAlchemy.

## Features
- Scrapes all quotes, authors, and tags from the website
- Stores data in a local SQLite database (`quotes.db`)
- Handles duplicate authors and tags
- Includes error handling and transaction rollback

## Project Structure
- `main.py`: Entry point (optional, may be used for custom scripts)
- `scraper.py`: Main scraping and database logic
- `models.py`: SQLAlchemy models and database setup
- `schemas.py`: (Optional) Pydantic schemas or data validation
- `quotes.db`: SQLite database file

## Requirements
- Python 3.12+
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

Install dependencies:
```bash
pip install requests beautifulsoup4 sqlalchemy
```

## Usage
Run the scraper:
```bash
python scraper.py
```
This will scrape all quotes and save them to `quotes.db`.

## Customization
- Modify `scraper.py` to change scraping logic or database handling.
- Use `models.py` to adjust database schema.

## API
This project includes a FastAPI-based web API to access the scraped quotes data.

### Endpoints
- `GET /` — Welcome message
- `GET /quotes/` — List quotes (supports `skip` and `limit` query parameters)
- `GET /quotes/{quote_id}` — Get a specific quote by ID

### Response Models
- Each quote includes its text, author, and associated tags.

### How to Run the API
1. Install dependencies (see above).
2. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```
3. Access the interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Example Usage
- List first 10 quotes:
  ```bash
  curl http://127.0.0.1:8000/quotes/
  ```
- Get quote with ID 1:
  ```bash
  curl http://127.0.0.1:8000/quotes/1
  ```

## License
MIT

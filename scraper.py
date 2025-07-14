import requests
from bs4 import BeautifulSoup
import time

from models import SessionLocal, engine, create_db_tables
from models import Quote, Author, Tag

BASE_URL = "http://quotes.toscrape.com"
next_page_url = "/"

def scrape_page(soup):
  quotes_divs = soup.find_all('div', class_='quote')
  scrapred_data = []
  for quote_div in quotes_divs:
    text = quote_div.find("span", class_="text").get_text(strip=True)
    author = quote_div.find("small", class_='author').get_text(strip=True)
    tags_elements = quote_div.find_all("a", class_='tag')
    tags = [tag.get_text(strip=True) for tag in tags_elements]

    scrapred_data.append({
      "text": text,
      "author_name": author,
      "tags_names": tags,
    })

  return scrapred_data

def scrape_all_pages():
  all_scraped_data = []
  next_page_url = "/"
  page_number = 1
  while next_page_url:
    full_url = BASE_URL + next_page_url
    response = requests.get(full_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    all_scraped_data.extend(scrape_page(soup))
    next_li = soup.find("li", class_="next")
    next_page_url = next_li.find("a")["href"] if next_li else None
    page_number += 1
    time.sleep(0.5)
  return all_scraped_data

def save_save_to_db(scraped_data):
  db = SessionLocal()
  try:
    for item in scraped_data:
      author = db.query(Author).filter(Author.name == item["author_name"]).first()
      if not author:
        author = Author(name=item["author_name"])
        db.add(author)
        db.flush()
      tag_objects = []
      for tag_name in item["tags_names"]:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
          tag = Tag(name=tag_name)
          db.add(tag)
          db.flush()
        tag_objects.append(tag)
      quote = Quote(
        text=item["text"],
        author=author,
        tags=tag_objects,
      )
      db.add(quote)
    db.commit()
  except Exception as e:
    print(f"--- ERRORS ON SAVING ---")
    print(e)
    print("--- CANCEL TRANSACTION (ROLLBACK) ---")
    db.rollback()
  finally:
    db.close()
    print("BDD session closed.")

if __name__ == "__main__":
  create_db_tables()
  all_quotes_data = scrape_all_pages()
  save_save_to_db(all_quotes_data)

from app.fetch import fetch_html
from app.parser import parse_html
from app.extractor import extract_books
from app.cleaner import clean_books
from app.saver import save_csv, save_json
from app.utils import setup_logger

from config.settings import RAW_FOLDER


def save_raw_html(html):

    with open(f"{RAW_FOLDER}/raw_page.html", "w", encoding="utf-8") as file:
        file.write(html)


def main():

    setup_logger()

    html = fetch_html()

    if html is None:
        print("Failed to fetch webpage.")
        return

    save_raw_html(html)

    soup = parse_html(html)

    books = extract_books(soup)

    cleaned_books = clean_books(books)

    save_csv(cleaned_books)

    save_json(cleaned_books)

    print(f"Successfully scraped {len(cleaned_books)} books.")


if __name__ == "__main__":
    main()

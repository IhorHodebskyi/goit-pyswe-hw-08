import json
from models import Author, Quote
import connect

def load_authors():
    with open("authors.json", "r", encoding="utf-8") as f:
        authors = json.load(f)
        for author_data in authors:
            # Перевірка на наявність автора в базі даних
            if not Author.objects(fullname=author_data["fullname"]).first():
                author = Author(**author_data)
                author.save()

def load_quotes():
    with open("qoutes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)
        for quote_data in quotes:
            author = Author.objects(fullname=quote_data["author"]).first()
            if author:
                quote = Quote(
                    tags=quote_data["tags"],
                    author=author,
                    quote=quote_data["quote"]
                )
                quote.save()

def run():

    print("Завантаження даних...")
    load_authors()
    load_quotes()
    print("Дані завантажені.")


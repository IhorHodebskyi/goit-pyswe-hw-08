from models import Author, Quote
import connect


def find_by_name(command):
    name = command.replace("name:", "").strip()
    author = Author.objects(fullname=name).first()
    if not author:
         return "Автор не знайдений."
    quotes = Quote.objects(author=author)
    return "\n".join(q.quote for q in quotes)


def find_by_tag(command):
    tag = command.replace("tag:", "").strip()
    quotes = Quote.objects(tags=tag)
    if not quotes:
        return "Цитати не знайдені."
    return "\n".join(q.quote for q in quotes)


def find_by_author(command):
    name = command.replace("author:", "").strip()
    author = Author.objects(fullname=name).first()
    if not author:
        return "Автор не знайдений."
    quotes = Quote.objects(author=author)
    return "\n".join(q.quote for q in quotes)


def main():
    while True:
        command = input("Введіть команду (наприклад, name: Steve Martin): ")
        if command == "exit":
            break
        if command.startswith("name:"):
            print(find_by_name(command))
        if command.startswith("tag:"):
            print(find_by_tag(command))
        if command.startswith("author:"):
            print(find_by_author(command))
        else:
            print("Невідома команда.")


if __name__ == '__main__':
    main()





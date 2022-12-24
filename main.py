"""
Зачетное задание.
Генерация случайных книг.
"""
import json
import random
import re
from typing import Generator

import faker

from conf import MODEL


BOOKS_FILE = "books.txt"
OUTPUT_FILE = "books.json"


def get_year() -> int:
    """
    Генерирует случайным образом год издания книги.
    :return: год издания, натуральное число
    """
    return random.randint(1900, 2022)


def get_pages() -> int:
    """
    Генерирует случайным образом количество страниц в книге.
    :return: количество страниц, натуральное число
    """
    return random.randint(5, 455)


def get_isbn13() -> str:
    """
    Генерирует случайным образом с помощью модуля Faker генерирует ISBN13,
    международный стандартный книжный номер.
    :return: ISBN13
    """
    f = faker.Faker()
    return f.isbn13()


def get_rating() -> float:
    """
    Генерирует случайным образом значение рейтинга книги.
    :return: рейтинг, число с плавающей запятой в диапазоне от 0 до 5,
            обе границы включительно
    """
    return round(random.uniform(0, 5), 2)


def get_price() -> float:
    """
    Генерирует случайным образом стоимость книги.
    :return: стоимость, число с плавающей запятой
    """
    return round(random.uniform(43, 4999), 2)


def get_author() -> list[str]:
    """
    Возвращает список авторов книги.
    Имя и фамилия автора выбираются случайным образом с помощью модуля Faker
    :return: список авторов. Содержит от 1 до 3 авторов
    """
    authors = list()
    authors_len = random.randint(1, 3)
    f = faker.Faker("ru")
    [authors.append(" ".join((f.last_name_female(), f.first_name_female())))
     for _ in range(0, authors_len)]
    return authors


def get_title() -> str:
    """
    Возвращает название книги из списка книг.
    Список книг хранится в файле books.txt.
    :return: название книги
    """
    BOOK_REGEX = r"(?P<title>.+?)\n"
    book_pattern = re.compile(BOOK_REGEX, re.DOTALL)
    books = list()
    with open(BOOKS_FILE, 'r', encoding="utf8") as f:
        for book in book_pattern.finditer(f.read()):
            books.append(book.groupdict())

    return random.choice(seq=books)["title"]


def book_gen(start_pk: int = 1) -> Generator:
    """
    Возвращает генератор книг.
    :param start_pk: счетчик книг, автоинкремент, по умолчанию 1.
    :return: генератор книг.
    """
    dict_ = dict()
    pk = start_pk
    for _ in range(100):
        dict_["model"] = MODEL
        dict_["pk"] = pk
        dict_["fields"] = dict()
        dict_["fields"]["title"] = get_title()
        dict_["fields"]["year"] = get_year()
        dict_["fields"]["pages"] = get_pages()
        dict_["fields"]["isbn13"] = get_isbn13()
        dict_["fields"]["rating"] = get_rating()
        dict_["fields"]["price"] = get_price()
        dict_["fields"]["author"] = get_author()
        yield dict_
        pk += 1


def main() -> list:
    """
    Генерирует словарь случайных книг и записывает полученный словарь в json файл.
    Пример структуры словаря:
    {
        "model": "shop_final.book",
        "pk": 1,
        "fields": {
            "title": "test_book",
            "year": 2020,
            "pages": 123,
            "isbn13": "978-1-60487-647-5",
            "rating": 5,
            "price": 123456.0,
            "author": [
                "test_author_1",
                "test_author_2"
            ]
        }
    }
    :return: список книг
    """
    book_gen_ = book_gen(start_pk=2)
    book_data = []

    for i in range(100):
        book = next(book_gen_)
        book_data.append(book)
        print(book)

    with open(OUTPUT_FILE, "w", encoding="utf8") as f:
        json.dump(book_data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()

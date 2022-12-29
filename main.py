"""
Зачетное задание.
Генерация случайных книг.
"""
import json
import random
import re
import sys
from typing import Generator, Callable

import faker

from conf import MODEL


BOOKS_FILE = "books.txt"
OUTPUT_FILE = "books.json"


def book_title_len_const(func: Callable):
    """
    Декоратор. Проверяет длину названия книги.
    :param func: декорируемая функция
    :return: None
    :raise: ValueError, если длина названия книги больше заданного значения
    """
    title_max_len = 255

    def wrapper():
        title = func()
        if len(title) > title_max_len:
            raise ValueError(f"Book title '{title}' length is {len(title)}. Expected: no more than {title_max_len}")
    return wrapper


def book_title_len(max_len: int):
    """
    Декоратор. Проверяет длину названия книги.
    :param max_len: максимальная длина названия книги, с которой сравнивается актуальная длина названия книги
    :return: None
    :raise: ValueError, если длина названия книги больше заданного значения
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            title = func(*args, **kwargs)
            if len(title) > max_len:
                raise ValueError(f"Book title '{title}' length is {len(title)}. Expected: no more than {max_len}")
        return wrapper
    return decorator


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


@book_title_len(255)
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


def get_book_title_offset() -> list:
    """
    Возращает в байтах смещение строк с книгами в файле.
    :return: список смещений в байтах
    """
    title_offset = [0]
    with open(BOOKS_FILE, 'rb') as f:
        for _ in f:
            title_offset.append(f.tell())
    return title_offset[:-1]


def get_title_effective() -> str:
    """
    Cчитывает только одну случайную строку с названием книги из файла.
    Список книг хранится в файле books.txt.
    :return: название книги
    """
    title_positions = get_book_title_offset()
    with open(BOOKS_FILE, 'r', encoding="utf8") as f:
        read_pos = random.choice(title_positions)
        f.seek(read_pos)
        book = f.readline().strip()
    return book


def book_gen(start_pk: int = 1) -> Generator:
    """
    Возвращает генератор книг.
    :param start_pk: счетчик книг, автоинкремент, по умолчанию 1.
    :return: генератор книг.
    """
    pk = start_pk
    for _ in range(100):
        dict_ = dict()
        dict_["model"] = MODEL
        dict_["pk"] = pk
        dict_["fields"] = dict()
        dict_["fields"]["title"] = get_title_effective()
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

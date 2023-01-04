import re
import faker

ISBN13_REGEX = r"(^978|979)-(\d{1,5})-(\d{1,7})-(\d{1,6})-([0-9]{1}|X$)"


def check_isbn13(isbn):
    result = re.fullmatch(ISBN13_REGEX, isbn)
    if result is None:
        raise ValueError(f"Данный ISBN {isbn} не соответствует формату ISBN13")


def test_isbn13(count):
    f = faker.Faker()
    gen_ = (f.isbn13() for _ in range(count))
    for _ in range(count):
        check_isbn13(next(gen_))


if __name__ == "__main__":
    test_isbn13(1000000)


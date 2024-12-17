import pytest

from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre имеет длину 2
        assert len(collector.books_genre.keys()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_add_too_long_and_too_short_names_no_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книгу с пустым именем
        collector.add_new_book('')

        # добавляем книгу с очень длинным именем
        collector.add_new_book('Книга' * 10)

        # проверяем, что книги не добавились в словарь
        assert len(collector.books_genre.keys()) == 0

    def test_add_new_book_add_same_name_twice_one_book(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()
        book = "Облачный Атлас"
        for _ in range(3):
            # добавляем книгу
            collector.add_new_book(book)
            # проверяем, что книга только одна
            assert len(collector.books_genre.keys()) == 1

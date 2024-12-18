import pytest

from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture(autouse=True)
    def new_collector(self):
        self.collector = BooksCollector()

    @pytest.fixture
    def collector(self):
        return self.collector

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books_two_books(self, collector):
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две книги
        # словарь books_genre имеет длину 2
        assert len(collector.get_books_genre().keys()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_add_too_long_and_too_short_names_no_books(self, collector):
        # добавляем две книгу с пустым именем
        collector.add_new_book('')

        # добавляем книгу с очень длинным именем
        collector.add_new_book('Книга' * 10)

        # проверяем, что книги не добавились в словарь
        assert len(collector.books_genre.keys()) == 0

    def test_add_new_book_add_same_name_twice_one_book(self, collector):
        book = "Облачный Атлас"
        for _ in range(3):
            # добавляем книгу
            collector.add_new_book(book)
            # проверяем, что книга только одна
            assert len(collector.books_genre.keys()) == 1

    def test_get_book_genre_add_two_books_no_genre(self, collector):
        # добавляем две книги
        book_1 = 'Book_1'
        book_2 = 'Book_2'
        collector.add_new_book(book_1)
        collector.add_new_book(book_2)

        # проверяем, что у книг нет жанра
        assert collector.get_book_genre(book_1) == collector.get_book_genre(book_2) == ""

    def test_set_book_genre_set_correct_genre_correct_genre(self, collector):
        # добавляем книгу
        book = 'Book'
        collector.add_new_book(book)
        for genre in collector.genre:
            collector.set_book_genre(book, genre)
            assert collector.get_book_genre(book) == genre

    def test_set_book_genre_set_incorrect_genre_no_genre(self, collector):
        # добавляем книгу
        book = 'Book'
        collector.add_new_book(book)
        for genre in ["", "Ужосы", 0, 1]:
            collector.set_book_genre(book, genre)
            assert collector.get_book_genre(book) == ""

    def test_get_books_with_specific_genre_assign_three_genres_return_two_books(self, collector):
        # выбираем 2 жанра
        genre_1, genre_2 = collector.genre[0], collector.genre[1]

        # создаем 3 названия
        book_1 = f'1_{genre_1}'
        book_2 = f'2_{genre_2}'
        book_3 = f'3_{genre_2}'

        # Добавляем все три книги, задаём жанры
        collector.add_new_book(book_1)
        collector.set_book_genre(book_1, genre_1)

        collector.add_new_book(book_2)
        collector.set_book_genre(book_2, genre_2)

        collector.add_new_book(book_3)
        collector.set_book_genre(book_3, genre_2)

        # проверяем, что метод вернёт только книги 2 и 3
        assert collector.get_books_with_specific_genre(genre_2) == [book_2, book_3]

        # def test_get_books_with_specific_genre_assign_invalid_genres_no_genres(self):
        #     # создаем экземпляр (объект) класса BooksCollector
        #     collector = BooksCollector()
        #     # создаем словарь с валидными именами книг и не валидными жанрами
        #     books_genres = {"1": "",
        #                     "2": "random_жанр_name",
        #                     "3": 0}
        #     for book, genre in books_genres.items():
        #         if genre not in collector.genre:
        #             collector.add_new_book(book)
        #             collector.set_book_genre(book, genre)
        #             print(collector.books_genre)
        #             assert collector.books_genre[book] == ""


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

    def add_correct_book(self, prefix: str = "Книга") -> str:
        if not 0 < len(prefix) < 41:
            prefix = "Книга"
        correct_book = f"{prefix}_{len(self.collector.books_genre) + 1}"
        self.collector.add_new_book(correct_book)
        return correct_book

    @pytest.mark.parametrize(
        "book_list, books_counter",
        [
            # Добавляем две книги с корректными названиями, должны добавиться обе
            (["Гордость и предубеждение и зомби", "Что делать, если ваш кот хочет вас убить"], 2),

            # Добавляем две книги с не корректными названиями, они не должны добавиться
            (["", "Книга" * 10], 0),

            # Дважды добавляем книгу с корректным названием, должна добавиться только одна
            (["Облачный Атлас", "Облачный Атлас"], 1),
        ]
    )
    def test_add_new_book_correct_count(self, collector, book_list, books_counter):
        # добавляем две книги
        for book in book_list:
            collector.add_new_book(book)

        # проверяем, что добавилось ожидаемое число книг
        assert len(collector.get_books_genre().keys()) == books_counter

        # проверяем, что у добавленных книг нет жанра
        assert all(genre == '' for genre in collector.get_books_genre().values())

    @pytest.mark.parametrize(
        "books_and_genre, is_genre_correct",

        [  # книги с корректным жанром должны корректно добавиться в словарь
            ({"Книга с корректным жанром 1": "Ужасы",
              "Книга с корректным жанром 2": "Детективы",
              "Книга с корректным жанром 3": "Мультфильмы"}, True),

            # книги с некорректным жанром должны добавиться в словарь,
            # но их жанр должен быть задан пустой строкой
            ({"Книга с некорректным жанром 1": "Ужосы",
              "Книга с некорректным жанром 2": 99,
              "Книга с некорректным жанром 3": False}, False)
        ])
    def test_set_book_genre(self, collector, books_and_genre, is_genre_correct):
        # добавляем новые книги, задаём жанры
        for book, genre in books_and_genre.items():
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

            # если по условию теста жанр не корректный (is_genre_correct == False),
            # то в словаре books_genre жанр должен быть пустой строкой
            if not is_genre_correct:
                genre = ""

            # проверяем значение жанра в словаре
            assert collector.books_genre[book] == genre

    def test_get_books_with_specific_genre(self, collector):
        # задаём жанр и число экземпляров жанра
        specific_genre, specific_counter = "Фантастика", 3

        # наполняем словарь указанным числом экземпляров книг выбранного жанра
        # и сохраняем имена добавленных книг для будущей проверки
        book_with_specific_genre = []
        for i in range(specific_counter):
            book = self.add_correct_book(specific_genre)
            book_with_specific_genre.append(book)
            collector.set_book_genre(book, specific_genre)

        # проверяем, что добавлено указанное число книг
        # так же эта строка проверяет работу функции self.add_correct_book()
        assert len(collector.books_genre) == len(book_with_specific_genre) == specific_counter

        # добавляем по одной книге всех оставшихся жанров
        for genre in collector.genre:
            if genre != specific_genre:
                book = self.add_correct_book(genre)
                collector.set_book_genre(book, genre)

        # проверяем, что метод get_books_with_specific_genre
        # вернёт только книги выбранного жанра
        assert collector.get_books_with_specific_genre(specific_genre) == book_with_specific_genre

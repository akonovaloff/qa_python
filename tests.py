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

    def add_correct_book(self, prefix: str = "Book") -> str:
        if not 0 < len(prefix) < 41:
            prefix = "Book"
        correct_book = f"{prefix}_{len(self.collector.books_genre) + 1}"
        self.collector.add_new_book(correct_book)
        return correct_book

    @pytest.mark.parametrize(
        "book_list, books_counter",
        [
            # Добавляем две книги с корректными названиями, должны добавиться обе
            (["Гордость и предубеждение и зомби",
              "Что делать, если ваш кот хочет вас убить",
              "Облачный Атлас"],
             3),

            # Добавляем две книги с не корректными названиями, они не должны добавиться
            (["",
              "Книга" * 10],
             0),

            # Дважды добавляем книгу с корректным названием, должна добавиться только одна
            (["Облачный Атлас",
              "Облачный Атлас"], 1),
        ]
    )
    def test_add_new_book_correct_counter(self, collector, book_list, books_counter):
        # добавляем две книги
        for book in book_list:
            collector.add_new_book(book)

        # проверяем, что добавилось ожидаемое число книг
        assert len(collector.get_books_genre().keys()) == books_counter

        # проверяем, что у добавленных книг нет жанра
        assert all(genre == '' for genre in collector.get_books_genre().values())

    @pytest.mark.parametrize(
        "genre, is_genre_correct",

        [  # книги с корректным жанром должны корректно добавиться в словарь
            ("Ужасы",       True),
            ("Детективы",   True),
            ("Мультфильмы", True),
            # книги с некорректным жанром должны добавиться в словарь,
            # но их жанр должен быть задан пустой строкой
            ("Ужосы",   False),
            (99,        False),
            (False,     False)
        ])
    def test_set_book_genre(self, collector, genre, is_genre_correct):
        # добавляем новые книги, задаём жанры
        book = self.add_correct_book()
        collector.set_book_genre(book, genre)

        # если по условию теста жанр не корректный (is_genre_correct == False),
        # то в словаре books_genre жанр должен быть пустой строкой
        if not is_genre_correct:
            genre = ""

        # проверяем значение жанра в словаре
        assert collector.books_genre[book] == genre

    def test_get_book_genre(self, collector):
        # добавляем новые книги, задаём жанры
        for genre in collector.genre:
            book = self.add_correct_book()
            collector.set_book_genre(book, genre)
            assert collector.get_book_genre(book) == genre

        for genre in ["Ужосы", "", 99, 0, False, True]:
            book = self.add_correct_book()
            collector.set_book_genre(book, genre)
            assert collector.get_book_genre(book) == ""

    @pytest.mark.parametrize("specific_genre",
                             ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_get_books_with_specific_genre(self, collector, specific_genre):
        # задаём число книг выбранного жанра
        specific_counter = 3
        # создаем пустой список книг для будущей проверки
        book_with_specific_genre = []
        # наполняем словарь книгами выбранного жанра
        for i in range(specific_counter):
            # добавляем книгу
            book = self.add_correct_book(specific_genre)
            # сохраняем имя книги для будущей проверки
            book_with_specific_genre.append(book)
            # задаём книге жанр
            collector.set_book_genre(book, specific_genre)

        # проверяем, что число книг в словаре и проверочном списке совпадает с указанным
        # так же эта строка проверяет работу функции self.add_correct_book()
        assert len(collector.books_genre) == len(book_with_specific_genre) == specific_counter

        # добавляем в словарь по одной книге всех оставшихся жанров
        for genre in collector.genre:
            if genre != specific_genre:
                book = self.add_correct_book(genre)
                collector.set_book_genre(book, genre)

        # проверяем, что метод get_books_with_specific_genre
        # вернёт только книги выбранного жанра
        assert collector.get_books_with_specific_genre(specific_genre) == book_with_specific_genre

    def test_get_books_with_specific_genre_empty_books_genre(self, collector):
        # для пустого словаря метод должен вернуть пустой список
        assert collector.get_books_with_specific_genre("Детективы") == []

    def test_get_books_with_specific_genre_empty_genre(self, collector):
        # добавляем книгу и указываем жанр
        book = self.add_correct_book()
        collector.set_book_genre(book, "Детективы")
        # проверяем, что при запросе книг некорректного жанра
        # из непустого словаря возвращается пустой список
        assert collector.get_books_with_specific_genre("") == []

    def test_get_books_for_children_two_books(self, collector):
        books_for_children = []
        for genre in collector.genre:
            book = self.add_correct_book()
            collector.set_book_genre(book, genre)
            if genre not in collector.genre_age_rating:
                books_for_children.append(book)

        assert collector.get_books_for_children() == books_for_children


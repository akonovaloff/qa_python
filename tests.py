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
    # test 1
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
            ("Ужасы", True),
            ("Детективы", True),
            ("Мультфильмы", True),
            # книги с некорректным жанром должны добавиться в словарь,
            # но их жанр должен быть задан пустой строкой
            ("Ужосы", False),
            (99, False),
            (False, False)
        ])
    # test 2
    def test_set_book_genre_correct_genre(self, collector, genre, is_genre_correct):
        # добавляем новые книги, задаём жанры
        book = self.add_correct_book()
        collector.set_book_genre(book, genre)

        # если по условию теста жанр не корректный (is_genre_correct == False),
        # то в словаре books_genre жанр должен быть пустой строкой
        if not is_genre_correct:
            genre = ""

        # проверяем значение жанра в словаре
        assert collector.books_genre[book] == genre

    # test 3
    def test_get_book_genre_correct_genre(self, collector):
        # добавляем новые книги, задаём жанры
        for genre in collector.genre + ["Ужосы", "", 99, 0, False, True]:
            book = self.add_correct_book()
            collector.set_book_genre(book, genre)
            if len(collector.books_genre.keys()) > len(collector.genre):
                genre = ""
            assert collector.get_book_genre(book) == genre

    @pytest.mark.parametrize("specific_genre",
                             ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    # test 4
    def test_get_books_with_specific_genre_correct_books(self, collector, specific_genre):
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

    # test 5
    def test_get_books_with_specific_genre_empty_books_genre(self, collector):
        # для пустого словаря метод должен вернуть пустой список
        assert collector.get_books_with_specific_genre("Детективы") == []

    # test 6
    def test_get_books_with_specific_genre_empty_genre(self, collector):
        # добавляем книгу и указываем жанр
        book = self.add_correct_book()
        collector.set_book_genre(book, "Детективы")
        # проверяем, что при запросе книг некорректного жанра
        # из непустого словаря возвращается пустой список
        assert collector.get_books_with_specific_genre("") == []

    # test 7
    def test_get_books_for_children_correct_book_for_each_children_genres(self, collector):
        # создаем пустой список для дальнейшей проверки
        books_for_children = []
        # добавляем по одной книге каждого жанра
        for genre in collector.genre:
            book = self.add_correct_book()
            collector.set_book_genre(book, genre)
            # сохраняем детские книги в список для проверки
            if genre not in collector.genre_age_rating:
                books_for_children.append(book)
        # проверяем, что итоговый и проверочный списки совпадают
        assert collector.get_books_for_children() == books_for_children

    # test 8
    def test_get_list_of_favorites_books_empty_favorite_list(self, collector):
        # проверяем что метод вернет пустой список для пустого словаря
        assert collector.get_list_of_favorites_books() == []

        # проверяем что метод вернет пустой список для не пустого словаря
        book = self.add_correct_book()
        assert collector.get_list_of_favorites_books() == []
        # проверяем, что метод вернёт пустой список, если добавить в избранное
        # не добавленную в словарь книгу
        collector.add_book_in_favorites(book + book)
        assert collector.get_list_of_favorites_books() == []

    # test 9
    def test_get_list_of_favorites_books_four_books(self, collector):
        favorites_books = []
        # добавляем в словарь 8 книг
        for i in (1, 2, 3, 4, 5, 6, 7, 8):
            book = self.add_correct_book()
            # четные книги добавляем в избранное
            if i in (2, 4, 6, 8):
                collector.add_book_in_favorites(book)
                favorites_books.append(book)

        assert collector.get_list_of_favorites_books() == favorites_books

        # проверяем, что список избранного не изменится, если добавить в него
        # одну книгу дважды
        collector.add_book_in_favorites(book)
        assert collector.get_list_of_favorites_books() == favorites_books

    # test 10
    def test_delete_book_from_favorites_three_books(self, collector):
        favorite_books = []
        for _ in (1, 2, 3, 4):
            book = self.add_correct_book()
            collector.add_book_in_favorites(book)
            favorite_books.append(book)
        assert favorite_books == collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites(book + book)
        assert favorite_books == collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites(book)
        assert book not in collector.get_list_of_favorites_books()

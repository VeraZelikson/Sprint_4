import pytest

from main import BooksCollector


class TestBooksCollector:

    @pytest.mark.parametrize(
        'book_name, should_be_added',
        [
            ['', False],
            ['1', True],
            ['Название книги на 20', True],
            ['Длинное название книги на сорок символов', True],
            ['Слишком длинное название книги 41 символ.', False]
        ]
    )
    def test_add_new_book_add_first_book(self, book_name, should_be_added):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        is_book_added = collector.get_books_genre().get(book_name) == ''
        assert is_book_added == should_be_added

    @pytest.mark.parametrize(
        "should_add_book, genre, expected_genre_set",
        [
            [True, 'Комедии', True],
            [True, 'Несуществующий_жанр', False],
            [False, 'Комедии', False]
        ]
    )
    def test_set_book_genre_if_book_added_set_genre(self, should_add_book, genre, expected_genre_set):
        book_name = 'Название'

        collector = BooksCollector()
        if should_add_book:
            collector.add_new_book(book_name)

        collector.set_book_genre(book_name, genre)
        genre_received = collector.get_book_genre(book_name)
        is_genre_saved = genre_received == genre
        assert expected_genre_set == is_genre_saved

    def test_get_book_genre_received_set_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Название')
        collector.set_book_genre('Название', 'Комедии')
        genre_received = collector.get_book_genre('Название')
        assert genre_received == 'Комедии'

    @pytest.mark.parametrize(
        'books, genre, expected_books',
        [
            [{}, 'Комедии', []],
            [{'Название': 'Комедии'}, 'Комедии', ['Название']],
            [{'Название1': 'Комедии', 'Название2': 'Ужасы', 'Название3': 'Комедии'}, 'Комедии',
             ['Название1', 'Название3']],
            [{'Название1': 'Комедии'}, 'Ужасы', []],
            [{'Название1': 'Трагикомедии'}, 'Трагикомедии', []]
        ]
    )
    def test_get_books_with_specific_genre_return_book_names(self, books, genre, expected_books):
        collector = BooksCollector()
        for book_name, book_genre in books.items():
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)
        received_books = collector.get_books_with_specific_genre(genre)
        assert received_books == expected_books

    def test_get_books_genre_return_saved_books(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}
        expected_books = {'Название': 'Комедии', 'Название2': 'Ужасы'}
        for book_name, book_genre in expected_books.items():
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)
        assert collector.get_books_genre() == expected_books

    @pytest.mark.parametrize(
        'books, expected_books',
        [
            [{'Название1': 'Комедии'}, ['Название1']],
            [{'Название1': 'Ужасы'}, []],
            [{'Название1': 'Ужасы', 'Название2': 'Мультфильмы', 'Название3': 'Мультфильмы'},
             ['Название2', 'Название3']],
            [{}, []],
            [{'Название1': 'Несуществующий_жанр'}, []]
        ]
    )
    def test_get_books_for_children_from_saved_books(self, books, expected_books):
        collector = BooksCollector()
        for book_name, book_genre in books.items():
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)
        children_books = collector.get_books_for_children()
        assert children_books == expected_books

    @pytest.mark.parametrize(
        'books, add_favorite_attempts_count, expected_favorites',
        [
            [['Название1'], 1, ['Название1']],
            [['Название1', 'Название2'], 1, ['Название1', 'Название2']],
            [['Название1'], 2, ['Название1']]
        ]
    )
    def test_add_book_in_favorites_save_books(self, books, add_favorite_attempts_count, expected_favorites):
        collector = BooksCollector()
        for book in books:
            collector.add_new_book(book)
            for i in range(add_favorite_attempts_count):
                collector.add_book_in_favorites(book)
        received_favorites = collector.get_list_of_favorites_books()
        assert received_favorites == expected_favorites

    @pytest.mark.parametrize(
        "books, books_to_remove, expected_favorites",
        [
            [['Название1'], ['Название1'], []],
            [['Название1', 'Название2'], ['Название1', 'Название2'], []],
            [['Название1', 'Название2'], ['Название1'], ['Название2']],
            [['Название1', 'Название2'], ['Название3'], ['Название1', 'Название2']]
        ]
    )
    def test_delete_book_from_favorites_remove_books(self, books, books_to_remove, expected_favorites):
        collector = BooksCollector()
        for book in books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        for book in books_to_remove:
            collector.delete_book_from_favorites(book)
        received_favorites = collector.get_list_of_favorites_books()
        assert received_favorites == expected_favorites

    def test_get_list_of_favorites_books_return_favorites(self):
        collector = BooksCollector()
        books = ['Название1', 'Название2']
        for book in books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        received_favorites = collector.get_list_of_favorites_books()
        assert received_favorites == books

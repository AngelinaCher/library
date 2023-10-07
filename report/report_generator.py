from collections import Counter
from datetime import datetime
from report.count_books import ListBook


class Report:

    def __init__(self, list_book: ListBook):
        """
        Инициализация объекта Report
        :param list_book: объект класса ListBook
        """
        self.list_book = list_book

    def _get_book_availability(self) -> tuple[list[tuple[str, int]], list[str], dict[str, str]]:
        """ Получает о книгах, получает имена тех, кто последний взял книгу """
        books_count = self.list_book.get_list_books_in_library()
        available_books, unavailable_books = self._process_book(books_count=books_count)
        last_book_borrower = self.list_book.last_borrowed_book

        return available_books, unavailable_books, last_book_borrower

    @staticmethod
    def _process_book(books_count: Counter) -> tuple[list[tuple[str, int]], list[str]]:
        """ Сортирует книги на "доступные" и "недоступные" """
        available_books = []
        unavailable_books = []
        for title, count in books_count.items():
            if count > 0:
                available_books.append((title, count))
            else:
                unavailable_books.append(title)
        return available_books, unavailable_books

    def create_library_report(self) -> None:
        """ Создает отчёт """
        now = datetime.now().strftime("%Y-%m-%dT%H:%M")
        report_filename = f"Library_report_{now}.txt"
        available_books, unavailable_books, last_book_borrower = self._get_book_availability()
        self._write_report(filename=report_filename, available_books=available_books,
                           unavailable_books=unavailable_books,
                           last_book_borrower=last_book_borrower)

    @staticmethod
    def _write_report(filename: str, available_books: list, unavailable_books: list, last_book_borrower: dict) -> None:
        """ Запись отчёта в файл """
        with open(filename, "w", encoding="utf-8") as file:
            file.write("# Доступно в библиотеке:\n")
            file.writelines(f"- {book[0]} ({book[1]})\n" for book in available_books)

            file.write("\n\n# Недоступные книги:\n")
            file.writelines(f"- {book} - читает {last_book_borrower[book]}\n" for book in unavailable_books)

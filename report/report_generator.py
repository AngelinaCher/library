from datetime import datetime

from report.count_books import ListBook
from library_api import library_api


def get_book_availability():
    users = library_api.LibraryAPI('users')
    events = library_api.LibraryAPI('events')
    books = library_api.LibraryAPI('books')

    list_book = ListBook(users=users, events=events, books=books)
    books = list_book.process_list_books()
    available_books = []
    unavailable_books = []
    for title, count in books.items():
        if count > 0:
            available_books.append((title, count))
        else:
            unavailable_books.append(title)
    return available_books, unavailable_books


def create_library_report():
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    report_filename = f"Library_report_{now}.txt"
    list_available_books, list_unavailable_books = get_book_availability()
    # with open(report_filename, "w", encoding="utf-8") as file:
    #     file.write("# Доступно в библиотеке:\n")
    #     for book in list_available_books:
    #         file.write(f"- {book[0]} ({book[1]})\n")


create_library_report()

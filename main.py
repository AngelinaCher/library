from library_api.library_api import LibraryAPI
from report.report_generator import Report
from report.count_books import ListBook


def main():
    users_api = LibraryAPI('users')
    events_api = LibraryAPI('events')
    books_api = LibraryAPI('books')

    list_book = ListBook(users=users_api, events=events_api, books=books_api)
    report = Report(list_book)
    report.create_library_report()


if __name__ == '__main__':
    main()

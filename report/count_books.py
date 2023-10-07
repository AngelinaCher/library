from collections import Counter
from datetime import datetime
from library_api.library_api import LibraryAPI


class ListBook:

    def __init__(self, users: LibraryAPI, events: LibraryAPI, books: LibraryAPI):
        """
        Инициализирует объект ListBook
        :param users: api users
        :param events: api events
        :param books: api books
        """
        self.users = users
        self.events = events
        self.books = books
        self.last_borrowed_book = {}

    @staticmethod
    def _bug_tracking(data: list) -> list:
        """ Проверка наличия ошибок к запросу, вывод ошибки в консоль и завершение работы программы """
        if 'error' in data:
            print(data)
            raise SystemExit(1)
        return data

    def _get_users_data(self) -> list:
        """ Получение данных из api users """
        users_data = self.users.get_data()
        if self._bug_tracking(users_data):
            return users_data

    def _get_count_books(self) -> Counter:
        """ Получение данных из api books """
        books_data = self.books.get_data()
        if self._bug_tracking(books_data):
            book_counts = Counter(books_data)
            return book_counts

    def _sorted_events(self) -> list:
        """ Получение данных из api о events сортировка events по дате """
        events_data = self.events.get_data()
        if self._bug_tracking(events_data):
            sorted_events_data = sorted(events_data, key=lambda event: datetime.fromisoformat(event['datetime']))
            return sorted_events_data

    def _get_list_books(self, events_data: list) -> Counter:
        """ Получение списка книг, учитывая последовательность событий. """
        books = self._get_count_books()
        users = self._get_users_data()
        for event in events_data:
            actor_id = str(event['actor_id'])
            datetime_action = datetime.fromisoformat(event['datetime'])

            user = next((user for user in users if user['id'] == actor_id), None)
            is_exists = self._check_user(user=user, datetime_action=datetime_action)
            if is_exists:
                self._process_library_event(event=event, user=user, books=books)
        return books

    @staticmethod
    def _check_user(user: dict, datetime_action: datetime) -> bool:
        """ Проверка наличия user и даты его создания """
        if user:
            user_created = datetime.fromisoformat(user['dt_created'])
            return datetime_action > user_created

    def _process_library_event(self, event: dict, user: dict, books: Counter) -> Counter:
        """ Обновляет счетчик книг на основе события (взятие или возврат книги) и обработка последнего взявшего книгу"""
        if event['action'] == 'take':
            book_title = event['target']
            if books[book_title] > 0:
                books[book_title] -= 1
                self.last_borrowed_book[book_title] = user['username']
        elif event['action'] == 'return':
            book_title = event['target']
            books[book_title] += 1
            if book_title in self.last_borrowed_book:
                del self.last_borrowed_book[book_title]

        return books

    def get_list_books_in_library(self) -> Counter:
        """ Обрабатывает список книг на основе событий и возвращает счетчик книг. """
        sorted_events = self._sorted_events()
        list_books = self._get_list_books(sorted_events)
        return list_books

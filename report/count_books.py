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

    def _get_users_data(self) -> list:
        """ Получение данных из api users """
        users_data = self.users.get_data()
        if 'error' in users_data:
            return users_data
        return users_data

    def _get_count_books(self) -> Counter:
        """ Получение данных из api books """
        books_data = self.books.get_data()
        if 'error' in books_data:
            return books_data
        book_counts = Counter(books_data)
        return book_counts

    def _sorted_events(self) -> list:
        """ Получение данных из api о events сортировка events по дате """
        events_data = self.events.get_data()
        if 'error' in events_data:
            return events_data
        sorted_events_data = sorted(events_data, key=lambda event: datetime.fromisoformat(event['datetime']))
        return sorted_events_data

    def _get_list_books(self, events_data: list) -> Counter:
        """ Получает список книг, учитывая последовательность событий. """
        books = self._get_count_books()
        users = self._get_users_data()
        for event in events_data:
            actor_id = str(event['actor_id'])
            datetime_action = datetime.fromisoformat(event['datetime'])

            user = next((user for user in users if user['id'] == actor_id), None)
            books = self._get_borrowed_books(event=event, user=user, datetime_action=datetime_action, books=books)
        return books

    @staticmethod
    def _get_borrowed_books(event: dict, user: dict, datetime_action: datetime, books: Counter):
        """ Обновляет счетчик книг на основе события (взятие или возврат книги) и проверка пользователя """
        if user:
            user_created = datetime.fromisoformat(user['dt_created'])
            if datetime_action > user_created:
                if event['action'] == 'take':
                    book_title = event['target']
                    if books[book_title] > 0:
                        books[book_title] -= 1
                elif event['action'] == 'return':
                    books[event['target']] += 1
        return books

    def process_list_books(self) -> Counter:
        """ Обрабатывает список книг на основе событий и возвращает счетчик книг. """
        sorted_events = self._sorted_events()
        list_books = self._get_list_books(sorted_events)
        return list_books

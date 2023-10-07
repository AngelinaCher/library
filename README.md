# library
Тестовое задание от MeдРокет

## Описание

Данный проект - это выполнение тестового задания от компании МедРокет. 
После запуска программы, скрипт создаст отчёт о доступных и недоступных книгах

## Установка

1. Склонируйте репозиторий: `https://github.com/AngelinaCher/library.git`
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте виртуальное окружение:
    * Для Windows: `venv\Scripts\activate`
    * Для Linux: `source venv/bin/activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Запуск
```
python main.py
```
## Технологии
* Python 3.10.12
* requests 2.31.0

## Структура проекта

* [library_api](library_api)
   + [library_api.py](library_api%2Flibrary_api.py) - получение данных из API
* [report](report)
   + [count_books.py](report%2Fcount_books.py) - формирование списка наличия книг
   + [report_generator.py](report%2Freport_generator.py) - формирование отчёта
* [Library_report_2023-10-07T22:42.txt](Library_report_2023-10-07T22%3A42.txt) - пример отчёта
* [main.py](main.py) - точка входа в программу
* [requirements.txt](requirements.txt) - файл с необходимыми зависимостями

# REST API для мотосервиса

Приложение реализует работу с данными о мотоциклах, поступающих на ремонт, по CRUD сценарию.\
Предусмотрена авторизация пользователей и несколько ролей для них с разными уровнями доступа.\
Для взаимодействия с БД используется ORM Django. Реализована работа со связанными таблицами.\
Выдача списков сущностей с возможностью сортировки, фильтрации и разбиением на страницы.\
Использована библиотека Django REST Framework.\
Архитектура построена с использованием паттернов проектирования с расчётом на большое приложение.

### - Аутентификация
JWT (Djoser, SimpleJWT)

### - Разрешения
Список мото - могут получить все\
Один мот - superuser, мастер\
Создание/обновление мото - superuser, мастер\
Удаление мота - superuser\
Список владельцев/один владелец - superuser, мастер\
Удаление владельца - superuser

### - Ограничение запросов
Запрещает любые запросы с 0:00 до 5:00\
Установлены ограничения для аутентифицированных и анонимных пользователей\
Опционально: низкая нагрузка - 2 запроса в минуту

### - Пагинация
Объектов на странице по умолчанию - 3,\
Возможность ручной установки количества объектов\
Максимально для ручной установки - 4

### - Фильтрация и поиск
Бибилиотека **django-filter**\
Фильтрация по марке мото\
Поиск по модели мото\
Фильтрация выдачи по году выпуска

## Дополнительно:

### - Вычисленяемое поле возраста мото

### - Конвертация цвета мото (hex-code <--> name) 
Библиотека **webcolors**\
в режиме записи конвертирует *код* цвета в его название\
в режиме чтения вернёт *название* цвета из БД


## Запросы

###/api/v1/bikes/

GET - список мото с пагинацией

POST - создание мото (+ создание владельца), 'previous_owners': необязательное\
(поля: {'nickname', 'brand', 'model', 'color', 'made_year', 'age', 'current_owner': {'name', 'surname'}, 'previous_owners': [{'name', 'surname'},]})

```commandline
{
  "nickname": "Виражка",
  "brand": "YAMAHA",
  "model": "XV750",
  "color": "wine",
  "made_year": 1995,
  "current_owner": {
    "name": "Наталья",
    "surname": "Lis"
  },
  "previous_owners": [
    {
      "name": "Наталья",
      "surname": "Lis"
    }
  ]
}
```
###/api/v1/bikes/id

GET - один мот

PUT - обновление мото (+ создание владельца), 'previous_owners': необязательное\
(поля: {'nickname', 'brand', 'model', 'color', 'made_year', 'current_owner': {'name', 'surname'}, 'previous_owners': [{'name', 'surname'},]})

```commandline
{
  "nickname": "Виражка",
  "brand": "YAMAHA",
  "model": "XV750",
  "color": "wine",
  "made_year": 1995,
  "current_owner": {
    "name": "Наталья",
    "surname": "Lis"
  },
  "previous_owners": [
    {
      "name": "Наталья",
      "surname": "Lis"
    }
  ]
}
```
PATCH - метод запрещен

DELETE - удаление мото

###/api/v1/owners/

GET - список владельцев

###/api/v1/owners/id

GET - один владелец

DELETE - удаление владельца

### Подробная документация - motoAPI/openapi.yaml

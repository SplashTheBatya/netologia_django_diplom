# Дипломный проект по курсу «Django: создание функциональных веб-приложений»
Разработан API для интернет-магазина. Реализован API сервиса и интерфейс администрирования. В качестве фреймворка используется Django и Django REST Framework.

Предоставлены код и тесты.

## Описание API

Сущности:

### Товар

url: `/api/v1/products/`

Поля:

- название
- описание
- цена
- дата создания
- дата обновления

Доступные действия: retrieve, list, create, update, destroy.

Создавать товары могут только админы. Смотреть могут все пользователи.

Есть возможность фильтровать товары по цене и содержимому из названия / описания.

### Отзыв к товару

url: `/api/v1/product-reviews/`

- ID автора отзыва
- ID товара
- текст
- оценка от 1 до 5
- дата создания
- дата обновления

Доступные действия: retrieve, list, create, update, destroy.

Оставлять отзыв к товару могут только авторизованные пользователи. 1 пользователь не может оставлять более 1го отзыва.

Отзыв можно фильтровать по ID пользователя, дате создания и ID товара.

Пользователь может обновлять и удалять только свой собственный отзыв.

### Заказы

url: `/api/v1/orders/`

- ID пользователя
- позиции: каждая позиция состоит из товара и количества единиц
- статус заказа: NEW / IN_PROGRESS / DONE
- общая сумма заказа
- дата создания
- дата обновления

Доступные действия: retrieve, list, create, update, destroy.

Создавать заказы могут только авторизованные пользователи. Админы могут получать все заказы, остальные пользователи только свои.

Заказы можно фильтровать по статусу / общей сумме / дате создания / дате обновления и продуктам из позиций.

Менять статус заказа могут только админы.

### Подборки

url: `/api/v1/product-collections/`

- заголовок
- текст
- товары в подборке
- дата создания
- дата обновления

Доступные действия: retrieve, list, create, update, destroy

Создавать подборки могут только админы, остальные пользователи могут только их смотреть.

## Интерфейс администратора

* Редактирование и просмотр подборок.
* Редактирование и просмотр товаров.
* Просмотр списка заказов пользователей, отсортированных по дате создания, с указанием пользователя и количества товаров.
* Страница детализации заказа с просмотром списка заказанных товаров.
* Редактирование и просмотр отзывов

## Данные для проверки
Файлы `fixture.json` с дамп-датой и список запросов `requests.http` расположены в папке `check_utils`

## Запуск проекта
1.Необходимо создать базу данных с названием netologia_diplom или изменить в `netologia_django_diplom\settings` в разделе `DATABASE` параметр `NAME` на название своей базы а так же `PASSWORD` и `USER` на соответсвующие вашей базе.   
2.Установить необходимые модули с помощью команды `pip install -r requirements-dev.txt`   
3.Совершить необходимые миграции используя команду `manage.py makemigrations`.  
4.Запустить проект командой `manage.py runserver`.  


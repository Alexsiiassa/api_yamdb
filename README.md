# REST API для проекта YaMDb

## Содержимое файла requirements:

requests==2.26.0
django==2.2.16
djangorestframework==3.12.4
djangorestframework-simplejwt==4.7.2
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
django_filter==21.1

## Установка:
Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

https://github.com/Alexsiiassa/api_yamdb
cd api_yamdb
Cоздать и активировать виртуальное окружение:

python3 -m venv env
source env/bin/activate
Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip
pip install -r requirements.txt
Выполнить миграции:

python3 manage.py migrate
Запустить проект:

python3 manage.py runserver

При желании можно загрузить тестовые данные в базу данных командой:
python3 manage.py load_csv_data

./manage.py loaddata data/fixtures.json

## Описание проекта

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: Книги, Фильмы, Музыка. Список категорий (Category) может быть расширен администратором (например, можно добавить категорию изобразительное искусство или Ювелирка).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории Книги могут быть произведения Винни-Пух и все-все-все и Марсианские хроники, а в категории Музыка — песня Давеча группы Насекомые и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, Сказка, Рок или Артхаус). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Когда вы запустите проект, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API YaMDb. В документации описано, как как работает API. Документация представлена в формате Redoc.

Аутентифицированный пользователь авторизован на изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения. При попытке изменить чужие данные должен возвращаться код ответа 403 Forbidden.

## Пользовательские роли

Аноним — может просматривать описания произведений, читать отзывы и комментарии.

Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.

Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.

Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

Суперюзер Django — обладет правами администратора (admin)

## Authentication

jwt-token

используется аутентификация с использованием JWT-токенов

## Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.

YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).

При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

## Ресурсы API YaMDb:

api/v1/auth/token (POST): передаём логин и пароль, получаем токен.

api/v1/users/me/ (GET, PATCH): пользователь переходит в свой профайл.

api/v1/users/ (GET, POST, PATCH, DELETE): пользователи.

api/v1/titles/ (GET, POST, PATCH): произведения, к которым пишут отзывы.

api/v1/categories/ (GET, POST, DELETE): категории (типы) произведений (Фильмы, Книги, Музыка).

api/v1/genres/ (GET, POST, DELETE): жанры произведений. 

api/v1/reviews/ (GET, POST, PATCH, DELETE): отзывы на произведения.

api/v1/comments/ (GET, POST, PATCH, DELETE): комментарии к отзывам. 

При запросе на изменение или удаление данных осуществляется проверка прав доступа.

### База данных:

Для загрузки данных, получаемых вместе с проектом, используем management-команду, добавляющую данные в БД через Django ORM.

Файлы CSV, расположенны в папке static. Выполнив все миграции, можно добавить данные из CSV в БД выполнив команду в терминале:

python manage.py load_csv_data


### Над проектом работали:

**[Игорь Солохин](https://github.com/igor-solokhin)**. Управление пользователями: система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля.

**[Роман Елизов](https://github.com/ElisovRoman)**. Категории, жанры и произведения: модели, view и эндпойнты для них.

**[Алексий Бобылев](https://github.com/Alexsiiassa)**. Отзывы и комментарии: модели и view, эндпойнты, права доступа для запросов.

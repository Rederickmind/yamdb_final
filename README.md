# Проект по созданию CI и CD для группового проекта Api_Yamdb

Проект подразумевает:
* автоматический запуск тестов,
* обновление образов на Docker Hub,
* автоматический деплой на боевой сервер при пуше в главную ветку main.

![example workflow](https://github.com/Rederickmind/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект развернут по адресу http://158.160.19.189/
  
# Описание Группового проекта YaMDb

  Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). 
  
  Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
  
  Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

# Над проектом работали:

* <img src="https://media.tenor.com/PS9Tcg6mIY4AAAAd/cat-ayasan.gif" width="40" height="40" /><a href='https://github.com/shinket7'> - shinket7 (Тимлид - разработчик 1)</a>
* <img src="https://media.tenor.com/ABqRkYb1P-wAAAAS/cat-cattitude.gif" width="40" height="40" /><a href='https://github.com/YaroslavButorin'> - YaroslavButorin (разработчик 2)</a>
* <img src="https://media.tenor.com/c3ORHs0_cuAAAAAM/cat-cute.gif" width="40" height="40" /><a href='https://github.com/Rederickmind'> - Rederickmind (разработчик 3)</a>



Стек технологий использованный в проекте:
* requests==2.26.0
* Django==3.2
* djangorestframework==3.12.4
* PyJWT==2.1.0
* pytest==6.2.4
* pytest-django==4.4.0
* pytest-pythonpath==0.7.3
* django-filter=23.1


## Запуск проекта:
* Клонировать репозиторий и перейти в него в командной строке.
* Перейти в консоли в папку infra
* Там находится нужный нам файл docker-compose

```
Необходимо установить Docker на ваше устройство

Из папки ../api_yamdb/infra выполнить команду:
docker-compose up -d --build 
```
Далее миграции, создание суперюзера и сбор статики

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

* Если есть необходимость, заполняем базу тестовыми данными:

Запустить командной:

```
docker-compose exec web python manage.py import_csv
```

## Пользовательские роли
* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
* Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
*  Суперюзер Django — обладает правами администратора (admin) 

### Подробная документация доступна по эндпоинту /redoc/

### Регистрация: POST запрос на адрес http://localhost/api/v1/auth/signup/

{
"email": "user@example.com",
"username": "string"
}

### Получение JWT токена происходит через confirmation code и POST запрос на адрес http://localhost/api/v1/auth/token/

{
  "username": "string",
  "confirmation_code": "string"
}

confirmation code можно найти в папке app/sent_emails/ в файлах контейнера infra-web-1
# yamdb_final

![After "push" status:](https://github.com/RabcriN/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

## YaMDb API

### Описание
Проект **YaMDb** собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

### Пользовательские роли
* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь** (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор** (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
* **Администратор** (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Суперюзер Django** — обладет правами администратора (admin)


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/RabcriN/yamdb_final
```

Добавить в https://github.com/<your_name>/yamdb_final/settings/secrets/actions
следующие ключи:
```

SECRET_KEY - Секретный ключ Вашего проекта для settings.py.

DEBUG - Выбрать режим разработки или отладки (по умолчанию False).
Варианты значений для "DEBUG": True values are "y", "yes", "t", "true", "on" and "1". False values are "n", "no", "f", "false", "off" and "0".
 
DB_ENGINE- Параметр указывает на используемый движок для доступа к БД.
По умолчанию используется Postgres.

DB_NAME - Имя базы данных.

POSTGRES_USER - Имя учётной записи для суперпользователя в Postgres.

POSTGRES_PASSWORD - Пароль для суперпользователя в Postgres.

DB_HOST - IP-адрес удаленной БД.
По умолчанию БД берётся из docker-контейнера под названием "db".

DB_PORT - Порт для подключения к БД.
По умолчанию для Postgres - 5432
```

### Если хотите получать уведомления в Telegram о том, что процесс деплоя успешно завершился,
### добавьте следующие ключи:
```
TELEGRAM_TO - ID своего телеграм-аккаунта. Узнать свой ID можно у бота @userinfobot.
TELEGRAM_TOKEN - Токен вашего бота. Получить этот токен можно у бота @BotFather.
```

### Проект автоматически разворачивается по адресу 84.201.160.143
### при внесении изменений и команде git push 

Выполняем миграции:
```
sudo docker-compose exec web python manage.py migrate
```
Создаём суперюзера:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Собираем статику:

```
sudo docker-compose exec web python manage.py collectstatic --no-input 
```

Админка доступна по адресу:

```
http://84.201.160.143/admin/
```
### Если используете Google Chrome:
Если админка отображается не корректно, очистите cache сочетанием клавиш
```
Ctrl+Shift+F5
```

Полная документация доступна по адресу:

```
http://84.201.160.143/redoc/
```

Стек технологий:
- Python 3.7 (https://docs.python.org/3/whatsnew/3.7.html)
- Django 3.2 (https://docs.djangoproject.com/en/3.2/)
- DRF (https://www.django-rest-framework.org/)
- Docker / Docker-compose (https://www.docker.com/)
- Nginx (http://nginx.org/en/docs/)
- Postgresql (https://www.postgresql.org/docs/)
- GitHub Actions workflows (https://docs.github.com/en/actions/using-workflows)

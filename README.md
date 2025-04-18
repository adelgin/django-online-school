# Онлайн школа на Django

Данный проект выполнен по дисциплине "Мультимедиа и технологии в образовании".

## Описание проекта

Этот проект представляет собой онлайн школу, разработанную на Django. Он включает в себя функционал для управления курсами, лекциями, тестами и пользователями (студентами и преподавателями).

## Установка и запуск проекта

Следуйте этим шагам, чтобы установить и запустить проект на вашем локальном компьютере:

### 1. Клонирование репозитория

Сначала клонируйте репозиторий на свой компьютер:

```bash
git clone https://github.com/adelgin/django-online-school.git
cd django-online-school/onlineschool
```

### 2. Установка зависимостей

Убедитесь, что у вас установлен Python 3.6 или выше. Рекомендуется использовать виртуальное окружение:

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Для Windows
venv\Scripts\activate
# Для macOS/Linux
source venv/bin/activate
```

Теперь установите все зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных

Перед запуском проекта вам нужно настроить базу данных. По умолчанию используется SQLite, но вы можете изменить настройки в файле settings.py.

Создайте миграции и примените их:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Создание суперпользователя

Создайте суперпользователя для доступа к админке:

```bash
python manage.py createsuperuser
```

Следуйте инструкциям на экране, чтобы задать имя пользователя, адрес электронной почты и пароль.

### 5. Запуск сервера
Теперь вы готовы запустить сервер разработки:

```bash
python manage.py runserver
```
Перейдите в браузере по адресу http://127.0.0.1:8000/, чтобы увидеть приложение в действии.

### 6. Админка

Для доступа к административной панели перейдите по адресу http://127.0.0.1:8000/admin/ и войдите, используя учетные данные суперпользователя, созданного ранее.

Используемые технологии

- Python 10
- Django
SQLite
- HTML/CSS/JavaScript
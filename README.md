ПРОЕКТ Магазин продуктов

Описание
Магазин продуктов — сайт на котором пользователи могут просматривать перечень продуктов питания, разбитых на категории и подкатегории. Для авторизованных пользователей реализована возможность добавлять продукты в корзину покупок.

Стек технологий:
- Backend: Python, Django Rest Framework
- База данных: SQLite

ЗАПУСК ПРОЕКТА

Клонировать репозиторий.

Cоздать и активировать виртуальное окружение:

python -m venv venv
source venv/Scripts/activate

Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:

python manage.py migrate

Установить фикстуры:

python manage.py loaddata categories.json subcategories.json products.json users.json shopping_carts.json

Запустить проект:

python manage.py runserver

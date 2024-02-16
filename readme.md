1. python -m venv .venv (python3 -m venv venv)
2. .venv/Scripts/activate (source .venv/bin/activate) 
3. python -m pip install -r requirements/prod.txt
4. cd lyceum
5. python manage.py runserver

Некоторые переменные сохранены в .env

Если хотите протестировать нужно:
1. Убедиться, что в файле .env значение DJANGO_DEBUG установлено True 
2. python -m venv .venv 
3. source .venv/bin/activate 
4. python -m pip install -r requirements/dev.txt -r requirements/prod.txt 
5. cd lyceum 
6. python manage.py test 
7. deactivate

Статус проверки:
[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/145442-timiniljuha-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/145442-timiniljuha-course-1112/-/commits/main) 
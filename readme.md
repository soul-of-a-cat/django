Для Windows используем **python (pip)**, для Linux - **python3 (pip3)**

# Запуск сервера
1. Создать виртуальное окружение\
python -m venv .venv
2. Активировать виртуальное окружение\
.venv/Scripts/activate (*source .venv/bin/activate* для Linux) 
3. Установить нужные библиотеки\
python -m pip install -r requirements/dev.txt
4. Переходим в нужную директорию\
cd lyceum
5. Запускаем сервер\
python manage.py runserver *(если нужно указываем нужный порт)*

***
<u>Некоторые переменные сохранены в .env</u>
***

# Запуск тестирования
1. Создать виртуальное окружение\
python -m venv .venv
2. Активировать виртуальное окружение\
.venv/Scripts/activate (*source .venv/bin/activate* для Linux) 
3. Установить нужные библиотеки\
python -m pip install -r requirements/dev.txt -r requirements/prod.txt
4. Переходим в нужную директорию\
cd lyceum
5. Запустить тесты\
python manage.py test 
6. Деактивировать виртуальное окружение (при необходимости)\
deactivate

***
<u>Структура базы данных описана в файле ER.jpg</u>

### Статус проверки в GitLab: [![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/145442-timiniljuha-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/145442-timiniljuha-course-1112/-/commits/main) 

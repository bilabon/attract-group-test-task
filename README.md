Test task for the Attract Group
======

Это тестовое задание на позицию Python developer.

####Задание 1:

- Есть таблица людей people (id, name) и таблица документов document (id, education, people_id).
Написать модели и выполнить инициализирующие миграции. Написать консольный скрипт (https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/), который принимает на вход условие отбора по типу документа (например python должно вернуть всех людей, у которых есть данное образование).

Решение:

Команда `(.env)$ ./manage.py find_people 'primary school, college, Университет'` запускает данный скрипт. В результате мы получаем список людей у которых есть все перечисленные образования. Есть возможность добавить аргумент `-exclude`, тогда результатом выполнения скрипта будет список людей у которых нету ни одного из перечисленных образований.
Фикстуры лоадятся при запуске команды `make migrate`, так что БД не пустая. Команда `make test` запускает тесты для данного решения.
Скрин консоли:

![Скрин выполнения задания 1](https://raw.githubusercontent.com/bilabon/attract-group-test-task/master/static/task1.png)

####Задание 2:

- Написать консольный скрипт по работе с одним из внешних сервисов (на Ваш выбор): получение курсов валют (с двух сайтов, на Ваш выбор).

Решение:

Скрипт запускается командой: `(.env)$ python parse_currency.py`. Парсер написан для privatbank.ua и kurs.com.ua сайтов.
Скрин консоли:

![Скрин выполнения задания 1](https://raw.githubusercontent.com/bilabon/attract-group-test-task/master/static/task2.png)


**Test admin panel:** http://127.0.0.1:8895/admin/

- Login: admin
- Password: admin

-------


Agreement
=========

- The `(.env)$` identifier of command line is indicates that there must be active virtual environment.

- In this manual path to the project, for example: `/full/path/to/the/attract-group-test-task/` - it will be designated as `$BASE_DIR`.


Attention
=========

- Python support: `2.7`

-------


Quick start guide
================

Clone
-----

    $ git clone git@github.com:bilabon/attract-group-test-task.git
    $ cd attract-group-test-task/


Install virtualenv
------------------

    $ virtualenv --no-site-packages -p/usr/bin/python2.7 .env
    $ source .env/bin/activate
    (.env)$


Install packages
----------------

    (.env)$ pip install -r requirements.txt


Synchronize
----------------

    (.env)$ make install
    (.env)$ make migrate
    (.env)$ make test
    (.env)$ make run

=======================================
Тестовое задание от проекта Rate&Goods
=======================================

  Задача
-------------
Создать систему рекомендаций для пользователя на базе действий других пользователей.
К примеру, у каждого пользователя есть список фильмов, которые он просмотрел, и если пользователь смотрел фильмы А и B,
но не смотрел фильм С, но у большинства пользователей, смотревших фильм А и В, фильм С попадается чаще всего,
он должен рекомендоваться для просмотра.

Основные требования:
- сгенерировать базу данных пользователей не менее 10 000 человек (можно использовать faker для генерации профилей);
- сгенерировать базу фильмов (или любых других сущностей) в количестве не меньше 50;
- случайным образом привязать одну или несколько сущностей к каждому пользователю;
- в выдаче рекомендации должны выдаваться несколько результатов, отсортированных по частоте попадания в порядке убывания
- получение рекомендаций должно работать разумное время для получения их в реальном времени;
- база данных для хранения профилей и сущностей - postgresql;
- язык python;
- остальные инструменты на выбор.


 Установка
-------------
Поднимаем окружение ``docker-compose build && docker-compose up``
Генерация фэйковых данных ``docker-compose run web python manage.py load_test_data``
Генерация матрицы item-based коллаборативной фильтрации  ``docker-compose run web python manage.py compile_collaborative_matrix``

 Использование
----------------
Для выполнения задачи было реализованно 2 метода:

1. Через обычный SQL запрос
http://127.0.0.1:8000/api/v1/recommendations/simple_sql/?user_id=14

+ Плюсы +:
* простое исполнение
* реалтайм данные
* точная сортировка результата, учитывает разницу в 1 просмотр

- Минусы -:
* тяжелый запрос
* одновременные запросы к таблице на select и insert
* при увеличении данных увеличивается время ответа на запрос, сложность O(n^2)

2. Использование Item-based коллаборативной фильтраци
http://127.0.0.1:8000/api/v1/recommendations/collaborative/?user_id=14

+ Плюсы +:
* высокая скорость получения результата
* с появлением новых просмотров значения внутри ячеек матрицы будут почти неизменны. Стабильность позволяет не перестраивать матрицу каждый раз при появлении новых просмотров.
* при увеличении данных время ответа на запрос не изменяется, сложность O(1)

- Минусы -:
* усложненное исполнениие
* погрешность в сортировке результата
* обновление данных через генерацию матрицы данных


 Тесты
-------------
``docker-compose run web python manage.py test``

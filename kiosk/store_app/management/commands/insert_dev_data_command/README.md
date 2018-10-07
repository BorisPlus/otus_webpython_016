# Заполнение каталога товаров (вариант реализации импорта данных с ресурсов сети Интернет)

Дополнительно, с целью заполнения базы данных Веб-приложения "КИОСК" сведениями о товарах, атрибутах и их значениях, были разработаны:
 * модули получения сведений о товарах (офлайн - из подготовленного вручную списка и онлайн - с сайта Интернет-магазина "Мвидео" (не реклама));
 * модуль импорта в базу данных Веб-приложения "КИОСК" полученных сведений.
 
Модуль импорта задействует те же модели, что и само Веб-приложение, что избавило от написания SQL-инструкций SELECT\INSERT, и реализован в виде MANAGEMENT-комманды приложения Django.

Вы можете разработать дополнительные модули получения сведений о товарах из других источников, главное чтобы разработанный модуль получения сведений, если вы хотите использовать уже реализованный мной модуль импорта, возвращал сведения о товарах, атрибутах и их значениях в формате данных, установленном мною для импорта.

Это списочно-словарная структура специального вида, и ее вид можно представить так:
 ```python
[
    {
        'main_image_url': STRING,
        'name': STRING,
        'description': STRING,
        'url_at_shop': STRING,
        'attrs': [
            {
                'name': STRING,
                'value': STRING,
            },
            {
                'name': STRING,
                'value': STRING,
            },
            ...
        ]
    },
    ...
]
```
Эта структура и является форматом входных данных для модуя импорта сведений о товарах, атрибутах и их значениях в **КИОСК**

### Модули получения сведений о товарах

[Пример](https://github.com/BorisPlus/otus_webpython_016/tree/master/kiosk/store_app/management/commands/insert_dev_data_command/data_fetchers/mvideo_ru_data.py) 
интерактивного сбора сведений о товарах, атрибутах и их значениях со страниц сайта Интернет-магазина "Мвидео" (не реклама) лежит в **_kiosk/store_app/management/commands/insert_dev_data_command/data_fetchers/mvideo_ru_data.py_**.

Данный пример осуществляет разбор html-структуры страниц сайта Интернет-магазина "Мвидео" и выбирает значения, соответствущие полям товаров и атрибутов, приводя собираемые даные к вышеописанному формату данных для импорта.

Пример использует библиотеки:
* beautifulsoup4=4.3.2
* urllib3=1.22

Установите их

```python
pip3 install beautifulsoup4==4.3.2
pip3 install urllib3==1.22
```
или
```
pip3 install -r additional/import_to_db_from/requirements.txt
```

### Запуск сбора и последующего импорта свведений
Вызов заполнения тестовыми данными

```bash
python3 kiosk/manage.py insert_dev_data '<НАЗВАНИЕ МАГАЗИНА>' '<URL страницы товаров МВИДЕО>'
```

Например,
```bash
python3 kiosk/manage.py insert_dev_data 'Мвидео' 'https://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118/f/page=2'
```

```bash
python3 kiosk/manage.py insert_dev_data 'М-Audio' 'https://www.mvideo.ru/videotehnika/saundbary-2547/f/page=2'
python3 kiosk/manage.py insert_dev_data 'М-Audio' 'https://www.mvideo.ru/videotehnika/saundbary-2547/f/page=5'
```

```bash
python3 kiosk/manage.py insert_dev_data '"Василий" Incorporated' 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/category=iphone-914/page=1'
python3 kiosk/manage.py insert_dev_data '"Василий" Incorporated' 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/category=iphone-914/page=2'
python3 kiosk/manage.py insert_dev_data '"Василий" Incorporated' 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/category=iphone-914/page=3'

```

В случае реализации Вами собственного модуля сбора сведений о товарах, атрибутах и их значениях просто замените ссылку на модуль получения сведений на свою (возможно добавив при импорте as get_products_info).

## Авторы

* **BorisPlus** - [https://github.com/BorisPlus/otus_webpython_016](https://github.com/BorisPlus/otus_webpython_016)

## Лицензия

Распространяется свободно.

## Дополнительные сведения

Проект в рамках домашнего задания курса "Web-разработчик на Python" на https://otus.ru/learning

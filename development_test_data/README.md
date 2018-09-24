# Заполнение каталога товаров (вариант реализации импорта данных с ресурсов сети Интернет)

Дополнительно, с целью заполнения базы данных Веб-приложения "КИОСК" сведениями о товарах, атрибутах и их значениях, были разработаны:
 * модули получения сведений о товарах (офлайн - из подготовленного вручную списка и онлайн - с сайта Интернет-магазина "Мвидео" (не реклама));
 * модуль импорта в базу данных Веб-приложения "КИОСК" полученных сведений.
 
Модуль импорта задействует те же модели, что и само Веб-приложение, что избавило от написания SQL-инструкций SELECT\INSERT.

Вы можете разработать дополнительные модули получения сведений о товарах из других источников, главное чтобы разработанный модуль получения сведений, если вы хотите использовать уже реализованный мной модуль импорта, возвращал сведения о товарах, атрибутах и их значениях в формате данных, установленном мною для импорта.


## Руководство разработчика

### Модуль импорта (формат входных данных)

Папка **_import_data_to_kiosk_db_from_different_sources/data_importer_** содержит модуль, реализующий импорт данных в БД о товарах, атрибутах и их значениях. На вход функции _importer.do_import_products_info_to_database()_ подается списочно-словарная структура специального вида.
 
 Ее вид можно описать так:
 ```python
[
    {
        'main_image_path': STRING,
        'name': STRING,
        'description': STRING,
        'shop_url': STRING,
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

#### Пример заранее подготовленных сведений (офлайн)

[Пример](https://github.com/BorisPlus/otus_webpython_006/tree/master/development_test_data/data_fetchers/test_data.py) заранее подготовленных сведений о товарах, атрибутах и их значениях лежит в **_example_import_to_db_from_different_sources/data_fetchers/test_data.py_**. Это данные с "Яндекс.Маркет" (не реклама), внесенные вручную в указанную структуру специального вида для последующего их импорта.

#### Пример онлайн сбора сведений с сайта Интернет-магазина "Мвидео" (не реклама) 

[Пример](https://github.com/BorisPlus/otus_webpython_006/tree/master/development_test_data/data_fetchers/mvideo_ru_data.py) 
интерактивного сбора сведений о товарах, атрибутах и их значениях со страниц сайта Интернет-магазина "Мвидео" (не реклама) лежит в **_example_import_to_db_from_different_sources/data_fetchers/mvideo_ru_data.py_**.

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

[Демонстрационный пример](https://github.com/BorisPlus/otus_webpython_006/tree/master/development_test_data/import_data_to_kiosk_db.py) сбора данных и их импорта в БД приведен в скрипте **_example_import_to_db_from_different_sources/example_import.py_**

```python
from additional_files_for_demonstration_of_app_working.import_data_to_kiosk_db_from_different_sources.data_fetchers.mvideo_ru_data import get_products_info
from additional_files_for_demonstration_of_app_working.import_data_to_kiosk_db_from_different_sources.data_importer.importer import do_import_products_info_to_database

if __name__ == '__main__':
    # сбор с первых 9 страниц о ноутбуках
    for i in range(2, 10):
        url = 'https://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118/f/page=%s' % i
        do_import_products_info_to_database(get_products_info(url))
```
В случае реализации Вами собственного модуля сбора сведений о товарах, атрибутах и их значениях просто замените ссылку на модуль получения сведений на свою (возможно добавив при импорте as get_products_info).

## Авторы

* **BorisPlus** - [https://github.com/BorisPlus/otus_webpython_006](https://github.com/BorisPlus/otus_webpython_006)

## Лицензия

Распространяется свободно.

## Дополнительные сведения

Проект в рамках домашнего задания курса "Web-разработчик на Python" на https://otus.ru/learning

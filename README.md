# Kiosk Django App

Проект простого Интернет-магазина "КИОСК"

## Описание

Проект отображает список товаров и их атрибутов и состоит из трех сущностей:
* Товары
* Атрибуты (характеристики)
* Значение атрибутов (характеристик) у товаров

, что схематично можно представить ER-моделью (3NF) базы данных как
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_004/master/README.files/images/simple_ER_model.png "Title")
[скачать проект схемы БД в формате DbWrench](https://raw.githubusercontent.com/BorisPlus/otus_webpython_004/master/README.files/docs/db_wrench_project.xml "Title")

Если углубляться в реальные требования к подобному приложению, даже без реализации функционала осуществления заказов пользователем, то не хватает многого (в т.ч. по БД), например:
* Отнесение товаров к категории
* Иерархия категорий
* Дополнительные изображения товара
* Учет типов атрибутов (целое, строка, период, множественный выбор, состоящий из других атрибутов атрибут) и их форматированный вывод пользователю
* Назначение товару группы атрибутов и их значений
* Упорядочивание атрибутов и их групп у товаров
* Фильтрация товаров по значениям атрибутов
* Архив товаров
* Скрытие товаров
* Цены на товары с их динамикой
* Еще много и много чего...

... но это выходит, как я понял, за рамки данного домашнего задания.

### Требования

Данный проект использует:
* Django 2

Установите:

```bash
$ pip3 install 'django>=2.0'
```

или

```bash
$ pip3 install -r requirements.txt
```

### Установка

```bash
$ cd <your_dir>
$ git clone git://github.com/BorisPlus/otus_webpython_006.git
```

### Использование

В качетве базы данных в данном проекте выбрана SQLite, поскольку она лучше всего подходит для быстрого разворачивания приложения с целью демонстратиции его работоспособности. 

Чтобы запустить проект выполните:
```bash
python3 /<absolute_path>/kiosk/manage.py migrate
python3 /<absolute_path>/kiosk/manage.py createsuperuser --username=admin --email=admin@example.com
python3 /<absolute_path>/kiosk/manage.py runserver
```
Перейдите по адресу http://127.0.0.1:8000

Административная панель http://127.0.0.1:8000/admin/

### Демонстрационный вариант базы данных

С целью демонстрации функционирования Веб-приложения "КИОСК" Вы можете воспользоваться файлом БД SQLite c уже подготовленными сведениями о товарах, атрибутах и их значениях. Скопируйте файл  подготовленной демонстрационной БД **_db.sqlite3_** из директории **_additional_files_for_demonstration_of_app_working/demo_db_** в директорию приложения **_kiosk_**.
 
При демонстрационном запуске с существующей заполненной проектной базой данных необходим доступ к сети Интернет, поскольку пути на изображения товаров указывают на их реальные ссылки (в демонстрационном варианте изображения не сохранены локально).

### Заполнение каталога товаров тестовыми данными

Дополнительно, с целью заполнения базы данных Веб-приложения "КИОСК" сведениями о товарах, атрибутах и их значениях, были разработаны:
 * модули получения сведений о товарах (офлайн - из подготовленного вручную списка и онлайн - с сайта Интернет-магазина "Мвидео" (не реклама));
 * модуль импорта в базу данных Веб-приложения "КИОСК" полученных сведений. 
 
Модуль импорта задействует те же модели, что и само Веб-приложение, что избавило от написания SQL-инструкций SELECT\INSERT.

Вы можете разработать дополнительные модули получения сведений о товарах из других источников, главное чтобы разработанный модуль получения сведений, если вы конечно хотите использовать уже реализованный мной модуль импорта, возвращал сведения о товарах, атрибутах и их значениях в формате данных, установленном мною для импорта.

Если Вам интересно, то ознакомтесь с [дополнительной документацией](https://github.com/BorisPlus/otus_webpython_006/tree/master/additional_files_for_demonstration_of_app_working/import_data_to_kiosk_db_from_different_sources/README.md)
данного проекта (**_внимание!_**: у модуля получения сведений о товарах с сайта Интернет-магазина "Мвидео" (не реклама) имеются свои зависимости).

### Cкриншоты

Открытая часть Веб-приложения:
* Список товаров
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/product_list.png "Title")

* Описание товара
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/product_detail.png "Title")

Административная панель Веб-приложения:
* Вход в административную панель Django
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_login.png "Title")
* Административная панель Django
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin.png "Title")
* Список товаров
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_product_list.png "Title")
* Создание \ редактирование товара
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_product.png "Title")
* После перехода в магазин
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/go_to_store.png "Title")
* Виджет для изображения в форме
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_img_widget.png "Title")

### Фичеризм реализации

#### Подход к реализации представлений (Django Class Based Views)

Использование _Django Class Based Views_, таких как _ListView_  и _DetailView_ позволяет существенно сократить объем кода. Вся логика отображения списка объектов и его деталеного представления инкапсулирована внутри данных классов. Необходимо лишь указать название модели для получения базового результата.

```python
from .models import Product
from django.views.generic import (
    ListView,
    DetailView,
)


class ProductDetail(DetailView):
    model = Product


class ProductList(ListView):
    model = Product
```
#### Подход к реализации маршрутов

Для маршрута по умолчанию применяется _RedirectView_ того же набора _Django Class Based Views_. 

```python
    ...
    url(r'^admin$', RedirectView.as_view(url='/admin/store_app/product/')),
    url(r'^admin/', admin.site.urls),
    url(r'^product_list/$', store_app_views.ProductList.as_view()),
    url(r'^product_detail/(?P<pk>\d+)/$', store_app_views.ProductDetail.as_view()),
    url(r'', RedirectView.as_view(url='/product_list/')),
    

```

В качетсве пути по умолчанию, когда ни один маршрут для осуществленного HTTP-запроса не подошел, применено перенаправление на представление по умолчанию. В данном случае это _'/product_list/'_:

```python
    ...
    url(r'', RedirectView.as_view(url='/product_list/')),
    ...
```

Аналогично и организации для "быстрой" ссылки на основную страницу административной панели. В данном случае это _'/admin/store_app/product/'_:

```python
    ...
    url(r'^admin$', RedirectView.as_view(url='/admin/store_app/product/')),
    ...
```

#### Подход к реализации расширенных представлений полей моделей

В модели Product имеется два поля, чье отображение в административной панели в виде текста является не эффективным. Это _shop_url_ - 'Ссылка на товар в магазине' и , )
    main_image_path - 'Изображение' (ссылка на него).
    
Типовым подходом к реализации корректного отображения подобных полей в виде HTML ссылки (<a ...>...</a>) и изображения (<img ...>) в списке объектов принято считать следующую реализацию (Custom Model Field at Admin site):

```python
from django.utils.html import mark_safe, escape
from django.contrib import admin
from .models import (
    Product,
)

class ProductAdmin(admin.ModelAdmin):
    ...
    list_display = (
        ...
        'shop_url_tag',
        ...
    )
    ...
    def shop_url_tag(self, obj):
        return mark_safe(
            '<a href="{href}">{text}</a>'.format(
                href=escape(obj.shop_url),
                text=escape(obj.shop_url),
            )
        )
        return obj.shop_url


admin.site.register(Product, ProductAdmin)
```

Данный подход при наличии большого числа таких полей, например, если у вас много подобных моделей, будет вынуждать реализовавать "пухлые" методы для каждого такого поля. А при необходимости внесения изменений в генерируемый HTML, например, внесение _CSS_ атрибута _class_, понадобится внести эти изменения везде. Предлагаю усовершенствовать подход, провести декомпозизию и вынести генерацию HTML кода в отдельную функцию, что упростит возможный последующий рефакторинг, так как правка будет в одном месте. 

Взгляните не предлагаемую реализацию с использованием декораторов:
```python
from django.utils.html import mark_safe, format_html_join, escape


def a(text=None, href=None):
    def decorator(decorate_me):
        def wrapper(self, obj):
            return mark_safe(
                '<a href="{href}">{text}</a>'.format(
                    href=href or decorate_me(self, obj),
                    text=text or decorate_me(self, obj),
                )
            )
        return wrapper
    return decorator
    
...
    @a(text='Перейти в магазин')
    def shop_url_tag(self, obj):
        return obj.shop_url
...

```

Ее можно развить, заставив тег HTML ссылки (<a ...>...</a>) иметь только те атрибуты, которые были переданы. Кроме того при передаче в качестве значений строк специального формата, например, имеющих два лидирующих подчеркивания, можно реализовать обращение к полю данной модели по шаблону, не имеющего данных два лидирующих подчеркивания. Так, например, ссылка на товар в стороннем магазинет сможет иметь в качестве текста название этого товара. Можно пойти еще дальше, реализовав подгрузку шаблона данного поля, или даже подгрузку результата шаблона другого поля объекта, например, для вставки в качестве текста изображения.

В настоящем приложении реализованы базовые варианты такого подхода с использованием декораторов для расширенного представления в административной панели в виде HTML  ссылок (<a ...>...</a>), изображений (<img ...>) и списков значений.
 
```python
class ProductAdmin(admin.ModelAdmin):
    ...
    @img()
    def main_image_path_tag(self, obj):
        return obj.main_image_path
    ...
    @a(text='Перейти в магазин')
    def shop_url_tag(self, obj):
        return obj.shop_url
    ...
    @html_list(row_format='<b>{}:</b> {}')
    def attributes_tag(self, obj):
        return obj.productattributes_set.all().values_list('attribute__name', 'value')
    ...
```
#### Форма создания \ редактирования товара

##### Заполнение M2M-связи

Сужность "Товар" связана с сущностью "Атрибут" связью _many-to-many_ через сущность "Значение атрибутов у товаров". Идея реализации отдельной формы для сущности "Значение атрибутов у товаров" приведет к неудобному интефейсу, так как назначение значений будет просиходть отдельно для каждой пары "Товар" - "Атрибут". Гораздо удобнее в Django использовать так называемые _inline_-формы. 

```python

class ProductAttributesInline(admin.TabularInline):
    model = ProductAttributes
    extra = 1


class ProductAdmin(ImageAdmin):
    inlines = (
        ProductAttributesInline,
    )
    ...
```
В данной реализации это позволило именно **назначать** товару его атрибуты, указывая их значения, в одной форме создания \ редактирования товара.

![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_product.png "Title")


##### Виджет изображения

В форме создания и редактировани товара присутствует область для редактирования поля _main_image_path_ объекта _Product_. На нем представлено текщее значение ссылки на изображение и HTML-поле для его правки. За представление поля _main_image_path_ объекта _Product_ в форме отвечает т.н. виджет. Для поля типа _models.URLField_ этот виджет именно таков и есть. 

![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_url_widget.png "Title")

Но гораздо эффективнее было бы дополнительное демонстрирование фотографии. Тип поля _models.ImageField_ так же не подходит, его виджет позволяет загружать фотографию, но опять же не демонстируя текщее изображение. 

Таким образом был разработан виждет для поля _models.URLField_, отображающий на форме HTML-изображение с указанием ссылки на него и HTML-поле для ее правки.

![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_006/master/README.files/images/screenshots/admin_img_widget.png "Title")

Но чтобы этот виджет применялся к полям именно ссылок на изображения был реализован класс административного представления объектов, от которого и был унаследован итоговый _class ProductAdmin_.

С целью возможного повтороного использования виджета и декораторов в других частях приложения их реализация была вынесена в отдельный модуль _additional_.

## Авторы

* **BorisPlus** - [https://github.com/BorisPlus/otus_webpython_006](https://github.com/BorisPlus/otus_webpython_006)

## Лицензия

В рамках лицензии Django - https://github.com/django/django/blob/master/LICENSE

## Дополнительные сведения

Проект в рамках домашнего задания курса "Web-разработчик на Python" на https://otus.ru/learning

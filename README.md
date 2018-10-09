# Оптимизация работы ORM Django 

С целью снижения числа запросов к базе данных при формировании списка объектов на следующем примере я хочу продемонстрировать существующие в Django возможности доопределения поведения ORM при конструировании запроса к базе данных, используя штатное [Django QueryAPI](htSELECtps://docs.djangoproject.com/en/2.1/ref/models/querysets/). 

Вот они, те методы, за чье грамотное использование администратор баз данных вам пожмет руку:
* select_related;
* prefetch_related;
* annotation, agregation, Subquery (заняло один пункт в списке, так как в этом примере они объеденены в одну подзадачу, но это вовсе не значит, что использование их обособленно друг от друга является нецелесообразным).

## На примере

Итак, пусть у нас будет проект простого Интернет-магазина "КИОСК" с таким списком сущностей:
* Магазин
* Город магазина
* Товары
* Атрибуты товаров
* Значение атрибутов у товаров

С точки зрения БД схема такова:
![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_016/master/README.files/images/simple_ER_model.png "Title")

[скачать проект схемы БД в формате DbWrench](https://raw.githubusercontent.com/BorisPlus/otus_webpython_016/master/README.files/docs/db_wrench_project.xml "Title")

Спискок сущностей немного надуманный, он подобран для демонстрации возможности оптимизации запросов ORM Django к базе данных.

### Список товаров

Первое, что можно оптимизировать, это снижение числа запросов при формировании списка объектов. У нас это список товаров, состоящих из:
* уникальны идентификатор товара;
* название магазина, продающего товар;
* название города магазина, продающего товар (<a name="attention_001">запомните этот пункт</a>);
* название товара;
* описание товара;
* основное изображение товара (про работу с картинками я описал ранее в ДЗ 006, но планирую реализовать отдельный пакет);
* список атрибутов товара.

Пусть у нас на страницу выводятся 25 товаров. Я сделал так, чтоб и малого импорта данных мне было достаточно для возникновения пагинации. Хотя в настоящее время, проблем с массовым импортом реальных "магазинных" данных проект не испытывает (см. [пункт](https://github.com/BorisPlus/otus_webpython_016#Загрузка-БД-тестовыми-свдениями)).
 
 Так как я использую авторизацию в админке, то на всё про всё приходится 80 запросов (запросы к _django_session_ и _auth_user_ включены).
 
 Итак. Товаров **25**, а запросов **80**. Понятно, идет отбор соответствующих внешних ключей (магазин, город магазина) и свяей многие-ко-многим (список атрибутов и их значений). **Но 80 - это ж более чем в 3 раза больше, чем 25!!!**
 
 Начнем с простого.
  
 Используем для автоподгрузки внешних ключей метод [_select_related_](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#select-related)
 
```python
def get_queryset(self, request):
     qs = super(ProductAdmin, self).get_queryset(request)
     qs = qs.select_related('shop')
     return qs
```
Хорошо, теперь стало **55** запросов.

Теперь вспомните пункт ["запомните этот пункт"](https://github.com/BorisPlus/otus_webpython_016#attention_001), в товарах есть обращение к городу магазина, где продается этот товар, а это внешний ключ (город) внешнего ключа (магазина) сущности (товара).

```python
def get_queryset(self, request):
     ...
     qs = qs.select_related('shop__city')
     return qs
```
 
Еще лучше, теперь стало **30** запросов.

И в итоге запрос свзанных внешних ключей таков

```postgres-sql
SELECT 
    "store_app_product"."id", 
    "store_app_product"."shop_id", 
    "store_app_product"."name", 
    "store_app_product"."description", 
    "store_app_product"."url_at_shop", 
    "store_app_product"."main_image_url", 
    "store_app_shop"."id", 
    "store_app_shop"."city_id", 
    "store_app_shop"."name", 
    "store_app_shop"."description", 
    "store_app_shop"."site", 
    "store_app_city"."id", 
    "store_app_city"."name" 
FROM 
    "store_app_product" 
INNER JOIN 
    "store_app_shop" 
ON 
    ("store_app_product"."shop_id" = "store_app_shop"."id") 
INNER JOIN 
    "store_app_city" 
ON 
    ("store_app_shop"."city_id" = "store_app_city"."id") 
ORDER BY
    "store_app_product"."id" ASC 
LIMIT 25
```

**Замечание**:

если использовать только `qs = qs.select_related('shop__city')`, то этого вполне будет достаточно для оптимизации выборки сущностей внешних ключей со всеми промежуточными, так как чтобы добраться по краних таких сущностей (внешний ключ внешнего ключа), то все равно запросу приходится выбирать промежуточные внешние ключи, чьи внешние ключи потом он и выберет. Просто так устроен реляционный язык запросов (будь то SQL или еще какой *QL). Чтоб добраться до объекта-связи текущего объекта-родителя, нужны все промежуточные связи. Как то так...

  Я к чему, уберите связь:
```python
     ...
     # qs = qs.select_related('shop')
     ...
```
и число запросов останется преждним - 30 запросов. Запрос к SQL то же тот же.

Продолжим.

Стоит изменить число выбираемых товаров на странице, мы увидем что число запросов растет абсолютно соразмерно-пропорционально. Увеличим число товаров на странице на 5, число запросов тоже подскочит на 5, а если на 25 - то и запросов на 25.

Вспомин, что есть атрибуты товаров, которые мы так же выводим в списке товаров. У атрибутов мы задействуем их имена и их значения у конкретных товаров.

На данном этапе метод выборки атрибутов товара и их значений таков
```python
    @separated_list(row_format='<b>{}:</b> {}', separator=',<br>')
    def get_attributes(self, obj):
        return obj.productattributes_set.all().values_list('attribute__name', 'value')
```

Для автоподгрузки сущностей, связанных отношением многие-ко-многим, будем использовать метод [_prefetch_related_](https://docs.djangoproject.com/en/2.1/**ref/models/querysets/#prefetch-related)

```python
    def get_queryset(self, request):
        ...
        qs = qs.prefetch_related(
            Prefetch(
                'productattributes_set',
                models.ProductAttributes.objects.select_related('attribute'),
            ),
        )
        return qs
        
```

Как не странно - число запросов возрасло до 31, и стало на 1 запрос больше.
А все потому, что при такой оптимизации ORM не добирается до оптимизированных моделей при обращении через метод _.values_list_. Для оптимизированного ORM необходимо использование list-comprehension подхода к выборке полей связанных M2M-сущностей.

```python
    @separated_list(row_format='<b>{}:</b> {}', separator=',<br>')
    def get_attributes(self, obj):
        return [(i.attribute.name, i.value) for i in obj.productattributes_set.all()]
```
ORM в этом случае "помнит", что объекты коллекции _productattributes_set_ задействуют _prefetch_related_.

Запросов стало... **6**!!! шесть, жесть, шесть...

Увеличим число товаров на странице до 100. Запросов по прежднему всего **6**!!!.

На моих данных (из-за числа попавших в выборку атрибутов и городов), если просто закоменнетировать `get_queryset`, выборка 100 товаров на страницу приведет к **499** запросам! Что **в 83 раза больше 6**! Пока отложим дальнейшие манипуляции с этой моделью в админке. Если говорить о времени, то это 93 миллисекунды против 3.

### Список магазинов

В списке магазинов отображаестя:
* наименование магазина,
* город магазина,
* описание магазина,
* сайт.
	
Очень бы хотелось иметь столбец с числом товаров в магазине. Вмешаемся опять в _queryset_.

```python
    def get_queryset(self, request):
        qs = super(ShopAdmin, self).get_queryset(request)

        products_count_qs = models.Product.objects.filter(shop=OuterRef(name='pk')). \
            values('id'). \
            annotate(v=Count('id')). \
            values('v')

        products_count_qs.query.group_by = None

        qs = qs.annotate(
            products_count_annotation=Subquery(
                queryset=products_count_qs,
                output_field=IntegerField()
            )
        )

        return qs
```

![shop_prod_count](https://raw.githubusercontent.com/BorisPlus/otus_webpython_016/master/README.files/images/screenshots/shop_prod_count.png "Title")

Очень бы хотелось правильно и доступно донести суть проделанного. Это выражение сложно воспринимается, но это абсолютно то, что вы сделали бы "ручками", если б писали чистый SQL запрос. Итак.

 Мы, _во-первых_, агрегировали число (см. "Count('id')") товаров, имеющихся с магазинах (shop), применив _OuterRef_, для отсылки выбираемых товаров на магазин.
  
  Поскольку это число, то обернем значение этого типа в _IntegerField()_.
  
 Это делается не для конкретного объекта, а для всех в выборке, что  через Subquery и аннотированеие дает результирующий целочисленный столбец с числом товаров в магазине. Обращение к этому столбцу реализовано в отдельном custom-методе администратора модели:
  
```python
    def get_products_count(self, obj):
        return obj.products_count_annotation

    get_products_count.short_description = 'Число товаров в магазине'
    get_products_count.admin_order_field = 'products_count_annotation'
```

Аха. А что у нас тут с числом запросов? Оно неизменно. Тут **5** SQL-запрососов.

Едем дальше.

### Бонус

Захотелось мне установить возможность отфильтровать сведения о товарах по их магазинам.
 
Если штатно, то в админке:
```python
    ...
    list_filter = (
        'shop',  # add some additional count of queries
    )

```
Число запросов увеличилось до **14**! Мне показалось это странным, я думал, раз мы добавляем фильтр по одной модели, то должен быть и один запрос. А тут 8 добавилось...

А сделаем сами custom-фильтр данных...

```python

class ShopFilter(SimpleListFilter):
    title = models.Shop._meta.verbose_name_plural.title()
    parameter_name = 'shop__id__exact'

    def lookups(self, request, model_admin):
        return [(s.id, str(s)) for s in models.Shop.objects.all().select_related('city')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(shop__id__exact=self.value())

```
Так, число запросов осталось неизменным.

Но мы забили. У магазина есть внешний ключ на город, который мы используем в отображении полного наименования магазина в формате "Магазин (г.Город)". Вам не напомнило это задачу выборки внешнего ключа, связанного по внешнему ключу с объеком. Да! тут нужен уже известный метод _select_related_.

```python
    ...
    def lookups(self, request, model_admin):
        return [(s.id, str(s)) for s in models.Shop.objects.all().select_related('city')]
    ...
```
Вуаля. Как я и хотел, тут **7** запросоа = **6** было и **+1** на получение магазинов для фильтра товаров по городам магазинов, где эти товары продаются.

E-e-e...


## Теперь о фишках

### Подход к реализации расширенных представлений полей моделей

В модели Product имеется три поля, чье отображение в административной панели в виде текста является не эффективным:
* _url_at_shop_ - cсылка на товар в магазине
* _main_image_url_ - главное изображение
* _attributes_ - список атрибутов
    
Типовым подходом к реализации корректного отображения подобных полей в админке в виде HTML ссылки (<a ...>...</a>), изображения (<img ...>) или списка с разделителем (', ') принято считать создание нового метода у модели в админке с оборачиванием вывода значения в HTML. Например:

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

Данный подход при наличии большого числа таких полей, которые нужно обернуть в HTML, например, если у вас много моделей c полями картинка или ссылками, будет вынуждать реализовавать "пухлые" методы для каждого такого поля. А при возникновении необходимости внесения изменений в генерируемый HTML, например, при необходимости внесения _CSS_-атрибута _class_, понадобится внести эти изменения **везде** во все эти и без того "пухлые" методы. Я предлагаю усовершенствованый подход. 

Генерация HTML кода должна быть в отдельных функциях, что упростит возможный последующий рефакторинг, так как правка будет в **одном** месте. 

Взгляните не предлагаемую реализацию с использованием декораторов:
```python
from plugins.django_model_admin_custom_field_decorators.html import (
        a,
        img,
        separated_list
    )
...
    # ShopAdmin 
    @a()
    def get_site(self, obj):
        return obj.site
    ...
    @a(title='Перейти к товарам', text='use_orm__get_full_name')
    def view_products(self, obj):
        return '/admin/store_app/product/?shop__id__exact=%s' % obj.pk
...
    # Product 
    # it is double_decorate
    @a(href='use_orm__url_at_shop', target='blank')
    @img()
    def get_main_image_url(self, obj):
        return obj.main_image_url
    ...
    @separated_list(row_format='<b>{}:</b> {}', separator=',<br>')
    def get_attributes(self, obj):
        return [(i.attribute.name, i.value) for i in obj.productattributes_set.all()]
...
```

Обратите внимание на последовательное использование декораторов

```python
    @a(href='use_orm__url_at_shop', target='blank')
    @img()
    def get_main_image_url(self, obj):
        return obj.main_image_url
```

Это декорирование приведет к тому, что будет открывающася при нажатии в новой вкладке ссылка на товар в магазине, при это ссылка будет не текстом и главной картинкой товара. Сам текст ссылки берется из поля объекта.

Кроме того, обратите внимание на префикс 'use_orm__*' в ключах. Этот префикс введен для указания необходимости вызова метода или получения значения поля соответствующего объекта admin-модели. Метод или поле должны иметь имя, последующее после указанного префикс 'use_orm__'.

При передаче в декоратор в качестве значений строк специального формата, например, имеющих лидирующие 'use_orm__', можно реализовать обращение к полю данной модели. Так, например, ссылка на товар в стороннем магазине сможет иметь в качестве title-текста название этого товара. Можно пойти еще дальше, реализовав подгрузку шаблона данного поля, или даже подгрузку результата шаблона другого поля объекта, например.

Я поместил эти декораторы в отдельный пакет _django_model_admin_custom_field_decorators_. Опишу его позже.

В настоящем приложении реализованы базовые варианты такого подхода с использованием декораторов для расширенного представления в административной панели в виде HTML ссылок (<a ...>...</a>), изображений (<img ...>) и списков значений (разделитель <br>).

### Форма создания \ редактирования товара

#### Заполнение M2M-связи

Сужность "Товар" связана с сущностью "Атрибут" связью _many-to-many_ через сущность "Значение атрибутов у товаров". Идея реализации отдельной формы для сущности "Значение атрибутов у товаров" приведет к неудобному интефейсу, так как установка этих значений будет просиходть отдельно для каждой пары "Товар" - "Атрибут". Гораздо удобнее в Django использовать так называемые _inline_-формы. 

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
В данной реализации это позволило именно **назначать** товару его атрибуты, устанавливая и их значения, в той же форме создания \ редактирования товара.

![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_016/master/README.files/images/screenshots/admin_product.png "Title")


#### Виджет изображения

В форме создания и редактировани товара присутствует область для редактирования поля _main_image_url_. В этой области представлено текщее значение ссылки на изображение и input-поле для его правки. За представление поля _main_image_url_ в форме отвечает т.н. виджет. Для поля типа _models.URLField_ этот виджет таков. 

![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_016/master/README.files/images/screenshots/admin_url_widget.png "Title")

Но гораздо эффективнее было бы дополнительное демонстрирование фотографии. Тип поля _models.ImageField_ так же не подходит, его виджет позволяет загружать фотографию, но опять же не демонстируя текщее изображение. 

Таким образом был разработан виждет для поля _models.URLField_, отображающий на форме изображение с указанием ссылки на него и имеющий input-поле для ее правки.

![KIOSK_ER_model](https://raw.githubusercontent.com/BorisPlus/otus_webpython_016/master/README.files/images/screenshots/admin_img_widget.png "Title")

Но чтобы этот виджет применялся к полям именно ссылок на изображения, был реализован класс административного представления объектов, от которого и был унаследован итоговый _class ProductAdmin_.

С целью возможного повтороного использования виджета и декораторов в других частях приложения их реализация была вынесена в отдельный модуль _plugin/django_imaged_model_admin_.

## Загрузка БД тестовыми свдениями

Загрузка БД тестовыми свдениями осуществляется с использованием management-комманды:

`python3 kiosk/manage.py insert_test_data 'Наименование магазина в нашей БД' 'город' 'ссылка на товары Мвидео'`

, например:

```
python3 kiosk/manage.py insert_test_data 'Мвидео' 'г.Москва' 'https://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118/f/page=2'

python3 kiosk/manage.py insert_test_data 'М-Audio' 'г.Новосибирск' 'https://www.mvideo.ru/videotehnika/saundbary-2547/f/page=2'

python3 kiosk/manage.py insert_test_data 'М-Audio' 'филиал в г.Москва' 'https://www.mvideo.ru/videotehnika/saundbary-2547/f/page=2'

python3 kiosk/manage.py insert_test_data 'М-Audio' 'филиал в г.Москва' 'https://www.mvideo.ru/videotehnika/saundbary-2547/f/page=5'

python3 kiosk/manage.py insert_test_data '"Василий" Incorporated' 'с.Яфонино' 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/category=iphone-914/page=1'

python3 kiosk/manage.py insert_test_data '"Василий" Incorporated' 'с.Яфонино' 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/category=iphone-914/page=2'

python3 kiosk/manage.py insert_test_data '"Василий" Incorporated' 'с.Яфонино' 'https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/category=iphone-914/page=3'

python3 kiosk/manage.py insert_test_data '"Истина где-то рядом"' 'г.Нью-Йорк' 'https://www.mvideo.ru/hobbi/binokli-i-teleskopy-2268'


python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=1'

python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=2'

python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=3'

python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=4'

python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=5'

python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=6'

python3 kiosk/manage.py insert_test_data '"Сам себе режиссер"' 'г.С-Пб' 'https://www.mvideo.ru/videokamery-i-ekshn-kamery/ekshn-kamery-2288/f/page=7'

python3 kiosk/manage.py insert_test_data 'Пусто' 'г.Вообще' 'https://www.mvideo.ru/empty'
```

## Авторы

* **BorisPlus** - [https://github.com/BorisPlus/otus_webpython_016](https://github.com/BorisPlus/otus_webpython_016)

## Лицензия

В рамках лицензии Django - https://github.com/django/django/blob/master/LICENSE

## Дополнительные сведения

Проект в рамках факультативного домашнего задания курса "Web-разработчик на Python" на https://otus.ru/learning

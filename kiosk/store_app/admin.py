from django.contrib import admin
from django.utils.html import mark_safe, format_html_join, escape
from .models import (
    Product,
    Attribute,
    ProductAttributes
)
from .widgets import (
    ImageWidget
)

admin.site.site_header = 'КИОСК'


def a(title=None, text=None, href=None, css_class=None):
    def decorator(decorate_me):
        def wrapper(self, *args, **kwargs):
            return mark_safe(
                '<a href="{href}" title="{title}" class="{css_class}">{text}</a>'.format(
                    href=href or decorate_me(self, *args, **kwargs),
                    title=title or decorate_me(self, *args, **kwargs),
                    text=text or decorate_me(self, *args, **kwargs),
                    css_class=css_class or "undef_css_class",
                )
            )

        return wrapper

    return decorator


def img(src=None, alt=None, width=None, css_class=None):
    def decorator(decorate_me):
        def wrapper(self, *args, **kwargs):
            return mark_safe(
                '<img alt="{alt}" src="{src}" width="{width}" class="{css_class}">'.format(
                    src=src or decorate_me(self, *args, **kwargs),
                    alt=alt or decorate_me(self, *args, **kwargs),
                    width=width or "150",
                    css_class=css_class or "undef_css_class",
                )
            )

        return wrapper

    return decorator


def html_list(row_format, seporator='<br>'):
    def decorator(decorate_me):
        def wrapper(self, *args, **kwargs):
            rows = []
            for item in decorate_me(self, *args, **kwargs):
                row = []
                for cell in item:
                    row.append(escape(cell))
                rows.append(tuple(row))
            return format_html_join(
                mark_safe(seporator),
                row_format,
                tuple(rows),
            )

        return wrapper

    return decorator


class ProductAttributesInline(admin.TabularInline):
    model = ProductAttributes
    extra = 1


class AttributeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attribute, AttributeAdmin)


class ImageAdmin(admin.ModelAdmin):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = ImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class ProductAdmin(ImageAdmin):
    image_fields = [
        'main_image_path',
    ]
    inlines = (
        ProductAttributesInline,
    )
    fields = [
        'name',
        'description',
        'shop_url',
        'main_image_path',
        'attributes_tag',
    ]
    list_display = (
        'id',
        'name',
        'description',
        'shop_url_tag',
        'main_image_path_tag',
        'attributes_tag',
    )
    list_display_links = (
        'name',
        'main_image_path_tag',
    )
    search_fields = [
        'attributes__name',
        'productattributes__value',
    ]
    readonly_fields = [
        'attributes_tag',
        'main_image_path_tag',
        'shop_url_tag'
    ]

    @img()
    def main_image_path_tag(self, obj):
        return obj.main_image_path

    main_image_path_tag.short_description = Product._meta.get_field('main_image_path').verbose_name.title()
    main_image_path_tag.admin_order_field = None

    @a(text='Перейти в магазин')
    def shop_url_tag(self, obj):
        return obj.shop_url

    shop_url_tag.short_description = Product._meta.get_field('shop_url').verbose_name.title()
    shop_url_tag.admin_order_field = None

    @html_list(row_format='<b>{}:</b> {}')
    def attributes_tag(self, obj):
        return obj.productattributes_set.all().values_list('attribute__name', 'value')

    attributes_tag.short_description = ProductAttributes._meta.verbose_name_plural.title()


admin.site.register(Product, ProductAdmin)

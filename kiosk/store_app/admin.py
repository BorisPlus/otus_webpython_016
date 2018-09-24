from django.contrib import admin
from .models import (
    Product,
    Attribute,
    ProductAttributes
)
from additional.admin_extra_classes import (
    ImageAdmin
)
from additional.admin_custom_fields_decorators import (
    a,
    img,
    html_list
)

admin.site.site_header = 'КИОСК'


class AttributeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attribute, AttributeAdmin)


class ProductAttributesInline(admin.TabularInline):
    model = ProductAttributes
    extra = 1


class ProductAdmin(ImageAdmin):
    inlines = (
        ProductAttributesInline,
    )
    image_fields = [
        'main_image_path',
    ]
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

    @a(text='Перейти в магазин')
    def shop_url_tag(self, obj):
        return obj.shop_url

    shop_url_tag.short_description = Product._meta.get_field('shop_url').verbose_name.title()

    @html_list(row_format='<b>{}:</b> {}')
    def attributes_tag(self, obj):
        return obj.productattributes_set.all().values_list('attribute__name', 'value')

    attributes_tag.short_description = ProductAttributes._meta.verbose_name_plural.title()


admin.site.register(Product, ProductAdmin)

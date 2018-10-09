from django.contrib import admin
from django.db.models import (
    Count,
    Prefetch,
    IntegerField
)
from django.db.models import OuterRef, Subquery

from . import models

try:
    # For Django running
    from plugins.django_imaged_model_admin.dima import (
        ImagedModelAdmin
    )
    from plugins.django_model_admin_custom_field_decorators.html import (
        a,
        img,
        separated_list
    )
except:
    # For PyCharm autocomplite only
    from kiosk.plugins.django_imaged_model_admin.dima import (
        ImagedModelAdmin
    )
    from kiosk.plugins.django_model_admin_custom_field_decorators.html import (
        a,
        img,
        separated_list
    )

admin.site.site_header = 'КИОСК'

from django.contrib.admin import SimpleListFilter


class ShopFilter(SimpleListFilter):
    title = models.Shop._meta.verbose_name_plural.title()
    parameter_name = 'shop__id__exact'

    def lookups(self, request, model_admin):
        return [(s.id, str(s)) for s in models.Shop.objects.all().select_related('city')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(shop__id__exact=self.value())


class ShopAdmin(admin.ModelAdmin):
    list_per_page = 10
    fields = [
        'name',
        'city',
        'site',
        'description',
    ]
    list_display = (
        'id',
        'view_products',
        'name',
        'city',
        'description',
        'get_site',
        'get_site_decorated_by_full_name_and_name',
        'get_products_count',
    )
    list_display_links = (
        'id',
    )
    search_fields = [
        'name',
        'city',
        'site',
    ]
    readonly_fields = (
        'get_site',
    )

    def get_queryset(self, request):
        qs = super(ShopAdmin, self).get_queryset(request)

        products_count_qs = models.Product.objects.filter(shop=OuterRef(name='pk')). \
            values('id'). \
            annotate(v=Count('id')). \
            values('v')

        products_count_qs.query.group_by = None
        # products_count_qs.query.clear_ordering(force_empty=True)

        qs = qs.annotate(
            products_count_annotation=Subquery(
                queryset=products_count_qs,
                output_field=IntegerField()
            )
        )

        return qs

    def get_products_count(self, obj):
        return obj.products_count_annotation

    get_products_count.short_description = 'Число товаров в магазине'
    get_products_count.admin_order_field = 'products_count_annotation'

    @a()
    def get_site(self, obj):
        return obj.site

    get_site.short_description = models.Shop._meta.get_field('site').verbose_name.title()

    @a(title='Перейти к товарам', text='use_orm__get_full_name')
    def view_products(self, obj):
        return '/admin/store_app/product/?shop__id__exact=%s' % obj.pk

    view_products.short_description = 'Перейти к товарам'

    @a(title='use_orm__get_full_name', text='use_orm__name')
    def get_site_decorated_by_full_name_and_name(self, obj):
        return obj.site

    get_site_decorated_by_full_name_and_name.short_description = 'декорирование URL атрибутом класса'


admin.site.register(models.Shop, ShopAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


admin.site.register(models.Attribute, AttributeAdmin)


class ProductAttributesInline(admin.TabularInline):
    model = models.ProductAttributes
    extra = 1


class ProductAdmin(ImagedModelAdmin):
    list_per_page = 100
    inlines = (
        ProductAttributesInline,
    )
    image_fields = [
        'main_image_url',
    ]
    fields = [
        'name',
        'description',
        'url_at_shop',
        'main_image_url',
        'get_attributes'
    ]
    list_display = (
        'id',
        'get_shop_name',
        'get_city',
        'name',
        'description',
        'get_main_image_url',
        'get_attributes',
    )
    list_display_links = (
        'id',
        'name',
    )
    search_fields = [
        'attributes__name',
        'productattributes__value',
    ]
    readonly_fields = [
        'get_attributes',
        'get_main_image_url',
    ]

    # There are no any optimization approach, when you want to use list_filter
    # but your can redeclare widget and behavior of list_filter item
    # for query count lowering
    list_filter = (
        # 'shop',  # add some additional count of queries
        ShopFilter,
        # 'attributes',  # add some additional count of queries
    )

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        # qs = qs.select_related('shop')  # No need if using qs.select_related('shop__city')
        qs = qs.select_related('shop__city')  # for: def get_city()...
        qs = qs.prefetch_related(
            Prefetch(
                'productattributes_set',
                models.ProductAttributes.objects.select_related('attribute'),
            ),
        )
        return qs

    # it is double_decorate
    @a(href='use_orm__url_at_shop', target='blank')
    @img()
    def get_main_image_url(self, obj):
        return obj.main_image_url

    # get_main_image_url.short_description = models.Product._meta.get_field('main_image_url').verbose_name.title()
    get_main_image_url.short_description = 'ссылка на %s в магазине' % models.Product._meta.verbose_name.title()

    # @html_list(separator=', ')
    @separated_list(row_format='<b>{}:</b> {}', separator=',<br>')
    def get_attributes(self, obj):
        """
        Prefetch research

        WITH PREFETCH
        qs = qs.prefetch_related(
            ...
            Prefetch(
                'attributes',
                Attribute.objects.all().only('name'),
            ),
            ...
        )

        return obj.attributes.all().values_list('name', flat=True) - 26 queries
        return [(i.name, i.name) for i in obj.attributes.all()] - 6 queries - but I need value!!


        WITH PREFETCH
        qs = qs.prefetch_related(
            ...
            Prefetch(
                'productattributes_set',
                ProductAttributes.objects.all().only('attribute__name', 'value'),
            ),
            ...
        )

        return [(i.attribute.name, i.value) for i in obj.productattributes_set.all()] - 166 queries
        return obj.productattributes_set.all().values_list('attribute__name', 'value') - 106 queries


        WITHOUT ANY PREFETCH!!!!!!

        return [(i.attribute.name, i.value) for i in obj.productattributes_set.all()] - 105 queries
        return obj.productattributes_set.all().values_list('attribute__name', 'value') - 25 queries!!!!!!

        It because you use THROUGH-model!!!!!!

        Not work:
        https://stackoverflow.com/questions/35093204/django-prefetch-related-with-m2m-through-relationship

        FINAL PREFETCH
        qs = qs.prefetch_related(
            ...
            Prefetch(
                'attributes',
                models.ProductAttributes.objects.select_related('attribute'),
            )
            ...
        )

        return [(a.attribute, a.value) for a in obj.attributes.all()] - 6 queries!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        # return [(p2a.attribute.name, p2a.value) for p2a in obj.attributes.all()]
        return [(i.attribute.name, i.value) for i in obj.productattributes_set.all()]

        # return obj.productattributes_set.all().values_list('attribute__name', 'value')

    get_attributes.short_description = models.ProductAttributes._meta.verbose_name_plural.title()

    def get_city(self, obj):
        """
        31 queries instead 65 queries
        because City queried with Product:

        def get_queryset(self, request):
            ...
            qs = qs.select_related('shop__city')
            ...
        """
        return obj.shop.city

    get_city.short_description = '%s (через select_related)' % models.City._meta.verbose_name.title()

    def get_shop_name(self, obj):
        return obj.shop.get_name()

    get_shop_name.short_description = models.Shop._meta.verbose_name.title()


admin.site.register(models.Product, ProductAdmin)

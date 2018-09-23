from django.db import models


class Attribute(models.Model):
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ('name',)
        unique_together = (('name',),)

    id = models.AutoField(primary_key=True, verbose_name='#')
    name = models.CharField(blank=False, null=False, max_length=100, verbose_name='Наименование', )

    def __str__(self):
        return '{x}'.format(x=self.name)


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('id',)
        unique_together = (('shop_url',),)

    id = models.AutoField(primary_key=True, verbose_name='#')
    name = models.CharField(blank=False, null=False, max_length=100, verbose_name='Наименование', )
    description = models.TextField(blank=False, null=False, max_length=200, verbose_name='Описание', )
    shop_url = models.URLField(blank=False, null=False, verbose_name='Ссылка на товар в магазине', )
    main_image_path = models.URLField(blank=False, null=False, verbose_name='Изображение', )
    attributes = models.ManyToManyField(
        Attribute, through='ProductAttributes',
        verbose_name=Attribute._meta.verbose_name_plural.title())

    def __str__(self):
        return 'ID:{x}, {y}'.format(x=self.id, y=self.name)


class ProductAttributes(models.Model):
    class Meta:
        verbose_name = 'Характеристики товара'
        verbose_name_plural = 'Характеристики товаров'
        ordering = ('-product__id', 'attribute__id',)
        unique_together = (('product', 'attribute'),)

    id = models.AutoField(primary_key=True, verbose_name='#')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=Product._meta.verbose_name.title())
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name=Attribute._meta.verbose_name.title())
    value = models.TextField(blank=True, null=False, max_length=100, verbose_name='Значение', )

    def __str__(self):
        return '{x} / {y}: {z}'.format(
            x=self.product,
            y=self.attribute,
            z=self.value
        )

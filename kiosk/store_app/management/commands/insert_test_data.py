from django.core.management.base import BaseCommand

try:
    from store_app import models
except:
    # For PyCharm autocomplite only
    from kiosk.store_app import models

from .insert_test_data_command.data_fetchers import mvideo_ru_data as dev_data


class Command(BaseCommand):
    help = 'Import test data'
    DEFAULT_VALUE = ''

    def add_arguments(self, parser):
        parser.add_argument('shop_name', type=str)
        parser.add_argument('shop_city_name', type=str)
        parser.add_argument('mvideo_ru_url_of_products', type=str)

    def handle(self, *args, **options):
        shop_name = options['shop_name']
        shop_city_name = options['shop_city_name']
        mvideo_ru_url_of_products = options['mvideo_ru_url_of_products']
        products_info = list()
        try:
            city, city_created = models.City.objects.get_or_create(name=shop_city_name)

            shop, shop_created = models.Shop.objects.get_or_create(
                name=shop_name,
                city=city
            )
            # shop.save()

            products_info = dev_data.get_products_info(url=mvideo_ru_url_of_products)
            for product_info in products_info:

                product, product_created = models.Product.objects.get_or_create(
                    shop=shop,
                    name=product_info.get('name', Command.DEFAULT_VALUE),
                    description=product_info.get('description', Command.DEFAULT_VALUE),
                    main_image_url=product_info.get('main_image_url', Command.DEFAULT_VALUE),
                    url_at_shop=product_info.get('url_at_shop', Command.DEFAULT_VALUE),
                )
                product.save()

                for attribute_info in product_info.get('attrs', []):
                    attribute, attribute_created = models.Attribute.objects.get_or_create(
                        name=attribute_info.get('name', Command.DEFAULT_VALUE),
                    )
                    attribute.save()

                    p2a_obj, p2a_obj_created = models.ProductAttributes.objects.get_or_create(
                        attribute_id=attribute.id,
                        product_id=product.id
                    )
                    p2a_obj.value = attribute_info.get('value', Command.DEFAULT_VALUE)
                    p2a_obj.save()

        except:
            #  DoesNotExist
            raise
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully %s products were loaded to shop \'%s\' (%s)' % (
                    len(products_info), shop_name, shop_city_name
                )
            )
        )

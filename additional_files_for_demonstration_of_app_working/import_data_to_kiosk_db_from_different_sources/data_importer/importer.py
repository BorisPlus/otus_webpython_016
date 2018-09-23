import os
import sys

kiosk_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if kiosk_path not in sys.path:
    sys.path.append(kiosk_path)

from store_app import models


def do_import_products_info_to_database(products_info):
    for product_info in products_info:
        obj_product = models.Product.objects.filter(
            name=product_info.get('name', 'UNDEF'),
            shop_url=product_info.get('shop_url', 'UNDEF')).first()
        if not obj_product:
            obj_product = models.Product(
                name=product_info.get('name', 'UNDEF'),
                description=product_info.get('description', 'UNDEF'),
                main_image_path=product_info.get('main_image_path', 'UNDEF'),
                shop_url=product_info.get('shop_url', 'UNDEF'),
            )
            obj_product.save()
        for attribute_info in product_info.get('attrs', []):
            obj_attribute = models.Attribute.objects.filter(name=attribute_info.get('name', 'UNDEF')).first()
            if not obj_attribute:
                obj_attribute = models.Attribute(
                    name=attribute_info.get('name', 'UNDEF'),
                )
            obj_attribute.save()

            obj_p2a = models.ProductAttributes.objects.filter(
                attribute__id=obj_attribute.id,
                product__id=obj_product.id,
            ).first()

            if not obj_p2a:
                obj_p2a = models.ProductAttributes()
                obj_p2a.attribute = obj_attribute
                obj_p2a.product = obj_product
                obj_p2a.value = attribute_info.get('value', 'UNDEF')

                obj_p2a.save()


if __name__ == '__main__':
    pass

import os
import sys

kiosk_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if kiosk_path not in sys.path:
    sys.path.append(kiosk_path)


def get_products_info(link=None):
    if link:
        pass
    return [
        {
            'main_image_path': 'https://avatars.mds.yandex.net/get-mpic/364668/img_id4117518369631908336.jpeg/6hq',
            'name': 'Ноутбук Lenovo IdeaPad 320 15 Intel',
            'description': 'Покупателям нравится небольшой вес, мощный процессор',
            'shop_url': 'https://market.yandex.ru/product/1730364335',
            'attrs': [
                {
                    'name': 'Процессор',
                    'value': 'Core i5 / Core i7',
                },
                {
                    'name': 'Частота процессора',
                    'value': '1600...1800 МГц',
                },
                {
                    'name': 'Объем оперативной памяти',
                    'value': '8...16 ГБ',
                },
                {
                    'name': 'Объем жесткого диска',
                    'value': '256 ГБ',
                },
                {
                    'name': 'Диагональ экрана',
                    'value': '15.6 "',
                },
            ]
        },
        {
            'main_image_path': 'https://avatars.mds.yandex.net/get-mpic/200316/img_id1017256079183483194/6hq',
            'name': 'Ноутбук Xiaomi Mi Notebook Air 12.5"',
            'description': 'Покупателям нравится долгое время работы, небольшой вес',
            'shop_url': 'https://market.yandex.ru/product/1727118961',
            'attrs': [
                {
                    'name': 'Процессор',
                    'value': 'Core M3 / Core i3 / Core i5',
                },
                {
                    'name': 'Частота процессора',
                    'value': '900...1200 МГц',
                },
                {
                    'name': 'Объем оперативной памяти',
                    'value': '4...8 ГБ',
                },
                {
                    'name': 'Объем жесткого диска',
                    'value': '128...256 ГБ',
                },
                {
                    'name': 'Диагональ экрана',
                    'value': '12.5 "',
                },
            ]
        },
    ]


if __name__ == '__main__':
    pass

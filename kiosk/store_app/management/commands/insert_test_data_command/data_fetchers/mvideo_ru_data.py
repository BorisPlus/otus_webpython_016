import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_products_info(url='https://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118'):
    products_info = []
    try:

        http = urllib3.PoolManager()
        request = http.request('GET', url)
        soup = BeautifulSoup(request.data)

        product_dict_template = {
            'main_image_url': '',
            'name': '',
            'description': '',
            'url_at_shop': '',
            'attrs': ''
        }
        attrs = []
        attr_dict_template = {
            'name': '',
            'value': '',
        }

        for product_row in soup.findAll('div', {'class': 'c-product-tile sel-product-tile-main '}):
            product_dict = product_dict_template.copy()

            # Берем главную картинку продукта
            is_break = False
            image_place = product_row.findAll('div', {'class': 'c-product-tile-picture'})
            for image in image_place:
                if is_break:
                    break
                img_tags = image.findAll('img', {'class': 'lazy product-tile-picture__image'})
                for img_tag in img_tags:
                    if img_tag.get('data-original', None):
                        product_dict['main_image_url'] = 'http:%s' % img_tag['data-original']
                        is_break = True
                        break

            # Берем описание продукта
            is_break = False
            description_place = product_row.findAll('div', {'class': 'c-product-tile__description-wrapper'})
            for description in description_place:
                if is_break:
                    break
                h4_tags = description.findAll('h4', )
                for h4_tag in h4_tags:
                    if h4_tag.get('title', None):
                        product_dict['name'] = h4_tag.get('title').strip()
                        a_tags = h4_tag.findAll('a', )
                        for a_tag in a_tags:
                            if a_tag.get('href', None):
                                product_dict['url_at_shop'] = 'https://www.mvideo.ru%s' % a_tag.get('href')
                                break
                        is_break = True
                        break

            is_break = False
            main_description_place = product_row.findAll('div', {'class': 'c-product-tile-badge'})
            for description in main_description_place:
                if is_break:
                    break
                span_tags = description.findAll('span')
                for span_tag in span_tags:
                    product_dict['description'] = span_tag.string.strip('\t\n\r ')
                    is_break = True
                    break

            # Берем атрибуты продукта
            attrs_of_object = attrs.copy()
            features_place = product_row.findAll('div', {'class': 'c-product-tile__feature-list'})
            for feature_place in features_place:
                features = feature_place.findAll('div', {'class': 'c-product-tile__feature'})
                for feature in features:
                    feature_name = feature.findAll('span', {'class': 'c-product-tile__feature-name'})
                    feature_value = feature.findAll('span', {'class': 'c-product-tile__feature-value'})
                    for n in feature_name:
                        for v in feature_value:
                            attr_dict = attr_dict_template.copy()
                            attr_dict['name'] = n.text.strip()
                            attr_dict['value'] = v.text.strip()
                            attrs_of_object.append(attr_dict)
            product_dict['attrs'] = attrs_of_object

            products_info.append(product_dict)

    except:
        raise Exception('ТОВАРИЩ, ЧТО-ТО ПОШЛО НЕ ТАК...')
    return products_info

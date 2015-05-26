
import requests
import json
from time import sleep

from django.utils.http import urlquote

BEST_BUY_BASE_URL = 'http://api.remix.bestbuy.com/v1/'

class BestBuyAPI(object):

    def __init__(self, api_key, linkshare_id=None):
        self.api_key = api_key
        self.linkshare_id = linkshare_id

    def lookup(self, id_type, product_id):

        product_id = urlquote(product_id).replace('/', '%2F')

        show = [
            'sku','name', 'regularPrice', 'salePrice', 'onSale', 'productId', 'linkShareAffiliateUrl','url',
            'customerReviewAverage', 'freeShipping', 'freeShippingEligible', 'onlineAvailability',
            'inStoreAvailability','shippingCost', 'marketplace', 'manufacturer','modelNumber', 'largeFrontImage',
            'image','upc'
        ]
        show = ",".join(show)

        url = '{base_url}products({type_id}=\'{product_id}\'&active=true&onlineAvailability=true&marketplace=*)?show={show}&pageSize=1&apiKey={api_key}&format=json'\
            .format(base_url=BEST_BUY_BASE_URL, type_id=id_type, product_id=product_id, show=show, api_key=self.api_key)

        if self.linkshare_id:
            url = '{0}&LID={1}'.format(url,self.linkshare_id)

        r = requests.get(url=url)
        sleep(0.3)
        try:
            r.raise_for_status()
        except Exception as e:
            print e
            print url

        try:
            j = r.json()
        except Exception as e:
            import traceback
            print traceback.format_exc()
            return

        if j and 'products' in j and len(j['products']) > 0:
            return BestBuyProduct(data=j)


class BestBuyProduct(object):

    def __init__(self, data):
        self.data = data

    @property
    def manufacturer(self):
        if self.__safe_get_value('manufacturer'):
            return self.__safe_get_value('manufacturer')

    @property
    def model(self):
        if self.__safe_get_value('modelNumber'):
            return self.__safe_get_value('modelNumber')

    @property
    def product_id(self):
        if self.__safe_get_value('productId'):
            return self.__safe_get_value('productId')

    @property
    def sku(self):
        if self.__safe_get_value('sku'):
            return self.__safe_get_value('sku')

    @property
    def name(self):
        if self.__safe_get_value('name'):
            return self.__safe_get_value('name')

    @property
    def price(self):

        if self.__safe_get_value('salePrice'):
            return self.__safe_get_value('salePrice')

        if self.__safe_get_value('regularPrice'):
            return self.__safe_get_value('regularPrice')

    @property
    def free_shipping(self):
        if self.__safe_get_value('freeShipping'):
            return self.__safe_get_value('freeShipping')

        return False

    @property
    def free_shipping_eligible(self):
        if self.__safe_get_value('freeShippingEligible'):
            return self.__safe_get_value('freeShippingEligible')

        return False

    @property
    def average_review(self):
        if self.__safe_get_value('customerReviewAverage'):
            return self.__safe_get_value('customerReviewAverage')

    @property
    def shipping_cost(self):
        if self.__safe_get_value('shippingCost'):
            return self.__safe_get_value('shippingCost')

    @property
    def large_picture_url(self):
        if self.__safe_get_value('largeFrontImage'):
            return self.__safe_get_value('largeFrontImage')

    @property
    def thumb_url(self):
        if self.__safe_get_value('image'):
            return self.__safe_get_value('image')

    @property
    def upc(self):
        if self.__safe_get_value('upc'):
            return self.__safe_get_value('upc')

    @property
    def url(self):
        print self.__safe_get_value('linkShareAffiliateUrl')
        if self.__safe_get_value('linkShareAffiliateUrl'):
            return self.__safe_get_value('linkShareAffiliateUrl')

        if self.__safe_get_value('url'):
            return self.__safe_get_value('url')

    def __safe_get_value(self, key):

        try:
            return self.data['products'][0][key]
        except KeyError:
            print 'BestBuyError: did not find {0}'.format(key)
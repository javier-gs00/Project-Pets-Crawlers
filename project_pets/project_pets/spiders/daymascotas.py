"""
Module containing the spiders for http://www.daymascotas.cl
"""
import re
from datetime import datetime
import scrapy
from project_pets.items import ProjectPetsItem

from project_pets.spiders.utils import parse_price


class DaymascotasSpider(scrapy.Spider):
    """ Spider that crawls food, meds and accs for dogs and cats """
    name = 'daymascotas'
    allowed_domains = ['daymascotas.cl']
    

    def start_requests(self):
        urls_dog_food = [
            'http://www.daymascotas.cl/categoria-producto/alimentos-perro/page/%s/' % page for page in range(1, 9)
        ]
        urls_dog_meds = [
            'http://www.daymascotas.cl/perros-2/medicamentos-2?page=%s' % page for page in range(1, 3)
        ]
        urls_dog_accs = [
            'http://www.daymascotas.cl/perros-2/accesorios?page=%s' % page for page in range(1, 8)
        ]
        urls_cat_food = [
            'http://www.daymascotas.cl/gatos-2/alimentos?page=%s' % page for page in range(1, 6)
        ]
        urls_cat_meds = [
            'http://www.daymascotas.cl/gatos-2/medicamentos-1?page=%s' % page for page in range(1, 3)
        ]
        urls_cat_accs = [
            'http://www.daymascotas.cl/gatos-2/accesorios?page=%s' % page for page in range(1, 7)
        ]
        urls = urls_dog_food    \
                + urls_dog_meds \
                + urls_dog_accs \
                + urls_cat_food \
                + urls_cat_meds \
                + urls_cat_accs

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        url_animal = response.url.split("/")[5]
        url_category = response.url.split("/")[5]

        item_animal = ''
        item_category = ''

        if url_animal == 'perro':
            item_animal = 'dog'
        elif url_animal == 'gatos-2':
            item_animal = 'cat'
        
        if url_category.count('alimentos') > 0:
            item_category = 'food'
        elif url_category.count('medicamentos') > 0:
            item_category = 'medicine'
        elif url_category.count('accesorios') > 0:
            item_category = 'accessory'

        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "http://www.daymascotas.cl" + product.css('p.foto a::attr(href)').extract()[0]
            item['price'] = self.parse_price(product.css('p.precio::text').extract()[0])
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Day Mascotas"
            item['category'] = item_category
            item['animal'] = item_animal
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    # @staticmethod
    # def parse_price(work_str):
    #     """ Recieves a string and removes everything except the numbers to transform it to a integer """
    #     return int(re.sub('[A-z$,.]', '', work_str).strip())

class DaymascotasDogFoodSpider(scrapy.Spider):
    """ Spider only for the dog food pages """
    name = 'daymascotas_dog_food'
    allowed_domains = ['http://daymascotas.cl']

    start_urls = [
        'http://daymascotas.cl/categoria-producto/alimentos-perro/page/%s/' % page for page in range(1, 9)
    ]
    # start_urls = [
    #     'http://daymascotas.cl/categoria-producto/alimentos-perro/'
    # ]

 
    def parse(self, response):
        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = product.css('h2::text').extract()[0]
            item['href'] = product.css('a::attr(href)').extract()[0]

            if product.css('del').extract_first(default='not-found') != 'not-found':
                price = product.css('span.price ins span.woocommerce-Price-amount::text').extract()[0]
            else:
                price = product.css('.woocommerce-Price-amount::text').extract()[0]
            item['price'] = parse_price(price)

            item['image_href'] = product.css('img::attr(src)').extract()[0]
            item['store'] = "Day Mascotas"
            item['category'] = "food"
            item['animal'] = "dog"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# class DaymascotasDogMedSpider(scrapy.Spider):
#     name = 'daymascotas_dog_meds'
#     allowed_domains = ['http://daymascotas.cl']

#     start_urls = [
#         'http://www.daymascotas.cl/perros-2/medicamentos-2?page=%s' % page for page in range(1, 3)
#     ]
 
#     def parse(self, response):
#         for product in response.css('div.in'):
#             item = ProjectPetsItem()

#             item['name'] = product.css('h1 a::text').extract_first()
#             item['href'] = "http://www.daymascotas.cl" + product.css('p.foto a::attr(href)').extract()[0]
#             price = product.css('p.precio::text').extract()[0]
#             item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
#             item['image_href'] = product.css('p a img::attr(src)').extract()[0]
#             item['store'] = "Day Mascotas"
#             item['category'] = "medicine"
#             item['animal'] = "dog"
#             item['date'] = datetime.today()
#             item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
#             yield item
    
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)

# class DaymascotasDogAccSpider(scrapy.Spider):
#     name = 'daymascotas_dog_accessories'
#     allowed_domains = ['http://www.daymascotas.cl']

#     start_urls = [
#         'http://www.daymascotas.cl/perros-2/accesorios?page=%s' % page for page in range(1, 8)
#     ]
 
#     def parse(self, response):
#         for product in response.css('div.in'):
#             item = ProjectPetsItem()

#             item['name'] = product.css('h1 a::text').extract_first()
#             item['href'] = "http://www.daymascotas.cl" + product.css('p.foto a::attr(href)').extract()[0]
#             price = product.css('p.precio::text').extract()[0]
#             item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
#             item['image_href'] = product.css('p a img::attr(src)').extract()[0]
#             item['store'] = "Day Mascotas"
#             item['category'] = "accessories"
#             item['animal'] = "dog"
#             item['date'] = datetime.today()
#             item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
#             yield item
    
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)

class DaymascotasCatFoodSpider(scrapy.Spider):
    """ Spider only for the dog food pages """
    name = 'daymascotas_cat_food'
    allowed_domains = ['http://daymascotas.cl']

    start_urls = [
        'http://daymascotas.cl/categoria-producto/alimentos-gato/page/%s/' % page for page in range(1, 5)
    ]
 
    def parse(self, response):
        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = product.css('h2::text').extract()[0]
            item['href'] = product.css('a::attr(href)').extract()[0]

            if product.css('del').extract_first(default='not-found') != 'not-found':
                price = product.css('span.price ins span.woocommerce-Price-amount::text').extract()[0]
            else:
                price = product.css('.woocommerce-Price-amount::text').extract()[0]
            item['price'] = parse_price(price)

            item['image_href'] = product.css('img::attr(src)').extract()[0]
            item['store'] = "Day Mascotas"
            item['category'] = "food"
            item['animal'] = "cat"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# class DaymascotasCatMedSpider(scrapy.Spider):
#     name = 'daymascotas_cat_meds'
#     allowed_domains = ['http://www.daymascotas.cl']

#     start_urls = [
#         'http://www.daymascotas.cl/gatos-2/medicamentos-1?page=%s' % page for page in range(1, 3)
#     ]
 
#     def parse(self, response):
#         for product in response.css('div.in'):
#             item = ProjectPetsItem()

#             item['name'] = product.css('h1 a::text').extract_first()
#             item['href'] = "http://www.daymascotas.cl" + product.css('p.foto a::attr(href)').extract()[0]
#             price = product.css('p.precio::text').extract()[0]
#             item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
#             item['image_href'] = product.css('p a img::attr(src)').extract()[0]
#             item['store'] = "Day Mascotas"
#             item['category'] = "medicine"
#             item['animal'] = "cat"
#             item['date'] = datetime.today()
#             item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
#             yield item
    
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)

# class DaymascotasCatAccSpider(scrapy.Spider):
#     name = 'daymascotas_cat_accessories'
#     allowed_domains = ['http://www.daymascotas.cl']

#     start_urls = [
#         'http://www.daymascotas.cl/gatos-2/accesorios?page=%s' % page for page in range(1, 7)
#     ]
 
#     def parse(self, response):
#         for product in response.css('div.in'):
#             item = ProjectPetsItem()

#             item['name'] = product.css('h1 a::text').extract_first()
#             item['href'] = "http://www.daymascotas.cl" + product.css('p.foto a::attr(href)').extract()[0]
#             price = product.css('p.precio::text').extract()[0]
#             item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
#             item['image_href'] = product.css('p a img::attr(src)').extract()[0]
#             item['store'] = "Day Mascotas"
#             item['category'] = "accessories"
#             item['animal'] = "cat"
#             item['date'] = datetime.today()
#             item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
#             yield item
    
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)
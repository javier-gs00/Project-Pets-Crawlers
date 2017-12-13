"""
Module containing the spiders for http://www.daymascotas.cl
"""
from datetime import datetime
import scrapy
from project_pets.items import ProjectPetsItem
from project_pets.spiders.utils import parse_price, parse_name


class DaymascotasSpider(scrapy.Spider):
    """ Spider that crawls food, meds and accs for dogs and cats """
    name = 'daymascotas'
    allowed_domains = ['daymascotas.cl']
    
    def start_requests(self):
        urls_dog_food = ['http://daymascotas.cl/categoria-producto/alimentos-perro/page/%s/' % page for page in range(1, 9)]
        urls_cat_food = ['http://daymascotas.cl/categoria-producto/alimentos-gato/page/%s/' % page for page in range(1, 5)]
        urls_meds = ['http://daymascotas.cl/categoria-producto/medicamentos-drag-pharma/page/%s/' % page for page in range(1, 7)]
        urls_accs = ['http://daymascotas.cl/categoria-producto/accesorios/page/%s/' % page for page in range(1, 3)]
        urls = urls_dog_food    \
                + urls_cat_food \
                + urls_meds \
                + urls_accs

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        url_animal = response.url.split("/")[4]
        url_category = response.url.split("/")[4]

        item_animal = ''
        item_category = ''

        if url_animal.count('perro'):
            item_animal = 'dog'
        elif url_animal.count('gato'):
            item_animal = 'cat'
        else:
            item_animal = 'unspecified'
        
        if url_category.count('alimentos') > 0:
            item_category = 'food'
        elif url_category.count('medicamentos') > 0:
            item_category = 'medicine'
        elif url_category.count('accesorios') > 0:
            item_category = 'accessory'

        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = parse_name(product.css('h2::text').extract()[0])
            item['href'] = product.css('a::attr(href)').extract()[0]

            if product.css('del').extract_first(default='not-found') != 'not-found':
                price = product.css('span.price ins span.woocommerce-Price-amount::text').extract()[0]
            else:
                price = product.css('.woocommerce-Price-amount::text').extract()[0]
            item['price'] = parse_price(price)

            item['image_href'] = product.css('img::attr(src)').extract()[0]
            item['store'] = "Day Mascotas"
            item['category'] = item_category
            item['animal'] = item_animal
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class DaymascotasDogFoodSpider(scrapy.Spider):
    """ Spider only for the dog food pages """
    name = 'daymascotas_dog_food'
    allowed_domains = ['http://daymascotas.cl']

    start_urls = ['http://daymascotas.cl/categoria-producto/alimentos-perro/page/%s/' % page for page in range(1, 9)]

    def parse(self, response):
        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = parse_name(product.css('h2::text').extract()[0])
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

class DaymascotasCatFoodSpider(scrapy.Spider):
    """ Spider only for the dog food pages """
    name = 'daymascotas_cat_food'
    allowed_domains = ['http://daymascotas.cl']

    start_urls = ['http://daymascotas.cl/categoria-producto/alimentos-gato/page/%s/' % page for page in range(1, 5)]

    def parse(self, response):
        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = parse_name(product.css('h2::text').extract()[0])
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

class DaymascotasMedSpider(scrapy.Spider):
    """ Spider only for the medicine pages """
    name = 'daymascotas_meds'
    allowed_domains = ['http://daymascotas.cl']

    start_urls = ['http://daymascotas.cl/categoria-producto/medicamentos-drag-pharma/page/%s/' % page for page in range(1, 7)]
 
    def parse(self, response):
        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = parse_name(product.css('h2::text').extract()[0])
            item['href'] = product.css('a::attr(href)').extract()[0]

            if product.css('del').extract_first(default='not-found') != 'not-found':
                price = product.css('span.price ins span.woocommerce-Price-amount::text').extract()[0]
            else:
                price = product.css('.woocommerce-Price-amount::text').extract()[0]
            item['price'] = parse_price(price)

            item['image_href'] = product.css('img::attr(src)').extract()[0]
            item['store'] = "Day Mascotas"
            item['category'] = "medicine"
            item['animal'] = "unspecified"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class DaymascotasAccSpider(scrapy.Spider):
    """ Spider only for the accessories pages """
    name = 'daymascotas_accessories'
    allowed_domains = ['http://www.daymascotas.cl']

    start_urls = ['http://daymascotas.cl/categoria-producto/accesorios/page/%s/' % page for page in range(1, 3)]
 
    def parse(self, response):
        for product in response.selector.css('li.show-links-onimage'):
            item = ProjectPetsItem()

            item['name'] = parse_name(product.css('h2::text').extract()[0])
            item['href'] = product.css('a::attr(href)').extract()[0]

            if product.css('del').extract_first(default='not-found') != 'not-found':
                price = product.css('span.price ins span.woocommerce-Price-amount::text').extract()[0]
            else:
                price = product.css('.woocommerce-Price-amount::text').extract()[0]
            item['price'] = parse_price(price)

            item['image_href'] = product.css('img::attr(src)').extract()[0]
            item['store'] = "Day Mascotas"
            item['category'] = "accessory"
            item['animal'] = "unspecified"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

import re
from datetime import datetime
import scrapy
from project_pets.items import ProjectPetsItem


class PethappyFoodSpider(scrapy.Spider):
    name = 'pethappy'
    allowed_domains = ['https://www.pethappy.cl']

    def start_requests(self):
        urls_dog_food = [
            'https://www.pethappy.cl/perros-2/alimentos?page=%s' % page for page in range(1, 9)
        ]
        urls_cat_meds = [
            'https://www.pethappy.cl/gatos-2/medicamentos-1?page=%s' % page for page in range(1, 3)
        ]
        urls = urls_dog_food + urls_cat_meds
        # for url in urls_dog_food:
        #     urls.append(url)
        # for url in urls_cat_food:
        #     urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        url_animal = response.url.split("/")[3]
        url_category = response.url.split("/")[4]

        item_animal = ''
        item_category = ''

        if url_animal == 'perros-2':
            item_animal = 'dog'
        elif url_animal == 'gatos-2':
            item_animal = 'cat'
        
        if url_category.count('alimentos') > 0:
            item_category = 'food'
        elif url_category.count('medicamentos') > 0:
            item_category = 'medicine'

        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            # price = product.css('p.precio::text').extract()[0]
            # item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['price'] = self.parse_price(product.css('p.precio::text').extract()[0])
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = item_category
            item['animal'] = item_animal
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    @staticmethod
    def parse_price(work_str):
        return int(re.sub('[A-z$,.]', '', work_str).strip())

class PethappyDogFoodSpider(scrapy.Spider):
    name = 'pethappy_dog_food'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/perros-2/alimentos?page=%s' % page for page in range(1, 9)
    ]
 
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "food"
            item['animal'] = "dog"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class PethappyDogMedSpider(scrapy.Spider):
    name = 'pethappy_dog_meds'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/perros-2/medicamentos-2?page=%s' % page for page in range(1, 3)
    ]
 
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "medicine"
            item['animal'] = "dog"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class PethappyDogAccSpider(scrapy.Spider):
    name = 'pethappy_dog_accessories'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/perros-2/accesorios?page=%s' % page for page in range(1, 8)
    ]
 
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "accessories"
            item['animal'] = "dog"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class PethappyCatFoodSpider(scrapy.Spider):
    name = 'pethappy_cat_food'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/gatos-2/alimentos?page=%s' % page for page in range(1, 6)
    ]
 
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "food"
            item['animal'] = "cat"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class PethappyCatMedSpider(scrapy.Spider):
    name = 'pethappy_cat_meds'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/gatos-2/medicamentos-1?page=%s' % page for page in range(1, 3)
    ]
 
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "medicine"
            item['animal'] = "cat"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class PethappyCatAccSpider(scrapy.Spider):
    name = 'pethappy_cat_accessories'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/gatos-2/accesorios?page=%s' % page for page in range(1, 7)
    ]
 
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "accessories"
            item['animal'] = "cat"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    # def parse(self, response):
    #     for product in response.xpath('.//div[contains(@class, "in")]'):
    #         item = ProjectPetsItem()

    #         item['name'] = product.xpath('//h1//a/text()').extract()
    #         item['href'] = product.xpath('//p//a/@href').extract()
    #         item['price'] = product.xpath('//p[contains(@class, "precio")]/text()').extract()
    #         item['image_href'] = product.xpath('//p//a//img/@src').extract()
    #         item['store'] = "Pet Happy"
    #         item['category'] = "Food"
    #         item['animal'] = "Dog"
            
    #         yield item
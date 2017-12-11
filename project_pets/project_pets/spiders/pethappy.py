import scrapy
import re
from datetime import datetime
from project_pets.items import ProjectPetsItem

class PethappySpider(scrapy.Spider):
    name = 'pethappy'
    allowed_domains = ['https://www.pethappy.cl']

    start_urls = [
        'https://www.pethappy.cl/perros-2/alimentos?page=%s' % page for page in range(1, 3)
    ]

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
    
    def parse(self, response):
        for product in response.css('div.in'):
            item = ProjectPetsItem()

            item['name'] = product.css('h1 a::text').extract_first()
            item['href'] = "https://www.pethappy.cl" + product.css('p.foto a::attr(href)').extract()[0]
            price = product.css('p.precio::text').extract()[0]
            item['price'] = int(re.sub("[A-z$,.]", "", price).strip())
            item['image_href'] = product.css('p a img::attr(src)').extract()[0]
            item['store'] = "Pet Happy"
            item['category'] = "Food"
            item['animal'] = "Dog"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')
            
            yield item
    
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
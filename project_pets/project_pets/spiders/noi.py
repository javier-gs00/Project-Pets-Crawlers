"""
Module containing the spiders for https://www.noi.la
"""
from datetime import datetime
import scrapy
from project_pets.items import ProjectPetsItem
from project_pets.spiders.utils import parse_name, parse_price

class NoiDogFoodSpider(scrapy.Spider):
    """ Spider only for the dog food pages """
    name = 'noi_dog_food'
    allowed_domains = ['https://www.noi.la']

    start_urls = ['https://www.noi.la/mascotte/perros/alimentos-perros/page/%s/' % page for page in range(1, 2)]

    def parse(self, response):
        for product in response.selector.css('div.product'):
            ## issues with the price extraction. HTML not organized and to get every price
            ## one has to enter the product page and click through some options
            item = ProjectPetsItem()

            item['name'] = parse_name(product.css('div.product-title a::text').extract()[0])
            item['href'] = product.css('a.woocommerce-LoopProduct-link::attr(href)').extract()[0]
            item['price'] = parse_price(product.css('span.woocommerce-Price-amount::text').extract()[0])
            item['image_href'] = product.css('img::attr(src)').extract()[0]
            item['store'] = "Noi"
            item['category'] = "food"
            item['animal'] = "dog"
            item['date'] = datetime.today()
            item['date_str'] = item['date'].strftime('%Y-%m-%d')

            yield item

        next_page = response.css('.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
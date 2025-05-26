import scrapy
from scrapy.crawler import CrawlerProcess
import logging


logging.getLogger('scrapy').propagate = False



class LightsSpider(scrapy.Spider):
    name = "divan_lights"
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        products = response.css("div[data-testid='product-card']")
        for product in products:
            name = product.css("a[class*='ProductName'] span::text").get()
            link = product.css("a[class*='ProductName']::attr(href)").get()
            price = product.css("span[data-testid='price']::text").get()

            name = name.strip() if name else "Нет названия"
            link = response.urljoin(link) if link else "Нет ссылки"
            price = price.strip() + " ₽" if price else "Нет цены"

            print(f" Название: {name}")
            print(f" Ссылка: {link}")
            print(f" Цена: {price}")
            print("-" * 40)

        next_page = response.css("a.Pagination__Next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


process = CrawlerProcess()
process.crawl(LightsSpider)
process.start()

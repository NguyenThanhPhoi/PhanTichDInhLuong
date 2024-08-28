import scrapy
from bs4 import BeautifulSoup

class CrawlDienmayxanhSpider(scrapy.Spider):
    name = "crawl_dienmayxanh"
    allowed_domains = ["www.dienmayxanh.com"]
    start_urls = ["https://www.dienmayxanh.com/tivi"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        products = response.css('li.item')
        for product in products:
            name = product.css('h3 ::text').get()
            price = product.css('.price ::text').get()
            old_price = product.css('.price-old ::text').get()
            discount = product.css('.percent ::text').get()
            image_url = product.css('img ::attr(data-src)').get()
            product_url = response.urljoin(product.css('a ::attr(href)').get())

            yield scrapy.Request(
                url=product_url,
                headers=self.headers,
                callback=self.parse_detail,
                meta={
                    'name': name,
                    'price': price,
                    'old_price': old_price,
                    'discount': discount,
                    'image_url': image_url,
                    'url': product_url
                }
            )

    def parse_detail(self, response):
        product_url = response.meta['url']
        # print("url", product_url)
        description_parts = response.css('div.content-article *::text').getall()
        description = ' '.join(description_parts).strip()
        print(description)

        
        # Lấy các thông tin đã lưu từ trang trước
        name = response.meta['name']
        price = response.meta['price']
        old_price = response.meta['old_price']
        discount = response.meta['discount']
        image_url = response.meta['image_url']
        

        yield {
            'name': name,
            'price': price,
            'old_price': old_price,
            'discount': discount,
            'image_url': image_url,
            'url': product_url,
            'description': description,
        }

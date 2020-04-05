# -*- coding: utf-8 -*-
import scrapy


class TutusecondSpider(scrapy.Spider):
    name = 'tutusecond'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        all_book = response.xpath('//article[@class="product_pod"]')

        for book in all_book:
            book_url = self.start_urls[0] + book.xpath('.//h3/a/@href')[0].extract()
            if 'catalogue' not in book_url:
                book_url = self.start_urls[0]+'catalogue/' + book.xpath('.//h3/a/@href')[0].extract()

            yield scrapy.Request(book_url, callback=self.inside_book)

        next_page_url_partial = response.xpath('//li[@class="next"]/a/@href')[0].extract()
        next_page_url = self.start_urls[0]+next_page_url_partial

        if 'catalogue' not in next_page_url:
            next_page_url = self.start_urls[0]+'catalogue/'+ next_page_url_partial

        yield scrapy.Request(next_page_url, callback=self.parse)

    def inside_book(self, response):
        book_name = response.xpath('//div/h1/text()')[0].extract()
        book_image = self.start_urls[0]+ response.xpath('//div[@class="item active"]/img/@src')[0].extract().replace('../../','')
        book_price = response.xpath('//div[@class="col-sm-6 product_main"]/p[@class ="price_color"]/text()')[0].extract()
        avilable_stock = response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="instock availability"]/text()')[1].extract().strip()
        star_rating = response.xpath('//div/p[contains(@class,"star-rating ")]/@class')[0].extract().replace('star-rating','')
        description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()')[0].extract()
        UPC = response.xpath('//table[@class="table table-striped"]/tr[1]/td/text()')[0].extract()
        product_type = response.xpath('//table[@class="table table-striped"]/tr[2]/td/text()')[0].extract()
        price_not_tax = response.xpath('//table[@class="table table-striped"]/tr[3]/td/text()')[0].extract()
        price_with_tax = response.xpath('//table[@class="table table-striped"]/tr[4]/td/text()')[0].extract()
        tax = response.xpath('//table[@class="table table-striped"]/tr[5]/td/text()')[0].extract()
        Availability = response.xpath('//table[@class="table table-striped"]/tr[6]/td/text()')[0].extract()
        number_of_reviews = response.xpath('//table[@class="table table-striped"]/tr[7]/td/text()')[0].extract()

        yield {
            "Book Name": book_name,
            "Book image": book_image,
            "Book Price": book_price,
            "Avilable stock": avilable_stock,
            "Star Rating": star_rating,
            "Description": description,
            "UPC": UPC,
            "Product Type": product_type,
            "Price NOt Tax": price_not_tax,
            "Price with Tax": price_with_tax,
            "Tax": tax,
            "Avalibility ": Availability,
            "Number Of Reviews": number_of_reviews
        }









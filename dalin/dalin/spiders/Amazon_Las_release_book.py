import scrapy


class Books(scrapy.Spider):
    name = 'top25books'
    start_urls =[
        'https://www.amazon.com/gp/new-releases/books/283155/ref=zg_bsnr_pg_2?ie=UTF8&pg=1',
        'https://www.amazon.com/gp/new-releases/books/283155/ref=zg_bsnr_pg_1?ie=UTF8&pg=2'
                 ]

    def parse(self, response):
        books = response.xpath('//li[@class="zg-item-immersion"]')
        for book in books:
            product_name = book.xpath('.//div[@class="p13n-sc-truncate p13n-sc-line-clamp-1"]/text()').extract_first().strip()
            if book.xpath('.//a[@class="a-size-small a-link-child"]/text()') is not None:
                product_author = book.xpath('.//a[@class="a-size-small a-link-child"]/text()').extract_first()
            else:
                product_author = book.xpath('.//li[@class="zg-item-immersion"]//span[@class= "a-size-small a-color-base"]').extract_first()
            product_price = book.xpath('.//span[@class="p13n-sc-price"]/text()').extract_first()
            image_link = book.xpath('.//div[@class="a-section a-spacing-small"]/img/@src').extract_first()
            lebel = book.xpath('.//span[@class="zg-badge-text"]/text()').extract_first().replace('#','')
            reting = book.xpath('.//span[@class="a-icon-alt"]/text()').extract_first()
            yield {
                'ID': lebel,
                'Name  ': product_name,
                'Author  ': product_author,
                'Price  ': product_price,
                'Image url  ': image_link,
                'Reating': reting
            }







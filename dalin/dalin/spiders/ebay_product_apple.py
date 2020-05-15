import scrapy


class Demo(scrapy.Spider):
    name = 'ebay'
    start_urls = ['https://www.ebay.com/b/Apple/bn_21819543']

    def parse(self, response):
        each_book = response.xpath('//li[@class="s-item   "]/div/div[2]')
        for book in each_book:
            bool_url = book.xpath('.//a/@href').extract_first()
            name = book.xpath('.//a/h3/text()').extract_first()
            price = book.xpath('.//div/div/span[@class="s-item__price"]/text()').extract_first()
            print(bool_url)
            print(name)
            print(price)
            yield scrapy.Request(url=bool_url, callback=self.details, meta={'Name':name, 'Price':price})

        next_page = response.xpath('//a[@rel ="next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.xpath('//a[@rel ="next"]/@href').extract_first()
            yield scrapy.Request(url=next_page, callback=self.parse)

        else:
            pass

    def details(self, response):
        url = response.url
        name = response.meta['Name']
        price = response.meta['Price']
        yield {
            'Name': name,
            'Price': price,
            'URL': url
        }


















#'//a[@rel ="next"]/@href'
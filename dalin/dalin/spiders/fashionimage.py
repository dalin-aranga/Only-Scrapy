import scrapy


class FashionSpider(scrapy.Spider):
    name ='fashionimage'
    allowed_domains = ['fotografen-hamburg.com']
    start_urls = ['https://fotografen-hamburg.com/business/', 'https://fotografen-hamburg.com/portrait/', 'https://fotografen-hamburg.com/fashion/']

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_image)

    def parse_image(self,response):
        for image_url in response.xpath('//div[@class="item_hover-img"]/img'):
            img = image_url.xpath('.//@src').extract_first()
            yield {'Image URL': img}

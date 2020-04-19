# -*- coding: utf-8 -*-
import scrapy


class PhotographySpider(scrapy.Spider):
    name = 'photography'
    allowed_domains = ['www.berufsfotografen.com/fotograf-hamburg?fbclid=IwAR1aAVAV0eaFGE4UXfT9gjgQnTZCBI3mghQnPcBz1vKEwAsL0K7vb1dI6N4']
    start_urls = ['http://www.berufsfotografen.com/fotograf-hamburg?fbclid=IwAR1aAVAV0eaFGE4UXfT9gjgQnTZCBI3mghQnPcBz1vKEwAsL0K7vb1dI6N4/']

    def parse(self, response):
        begain_url ='https://www.berufsfotografen.com'
        photo_urls = response.xpath('//a[@class= "photo-block"]')
        lass_urls = response.xpath('//a[@class= "lass-block"]')
        row_urls = response.xpath('//div[@class="detailsgrid_row"]')
        for photo_url in photo_urls:
            real_url = begain_url+photo_url.xpath('.//@href').extract_first()
            yield scrapy.Request(real_url, callback=self.details , dont_filter=True)
        for lass_url in lass_urls:
            real_url = begain_url + lass_url.xpath('.//@href').extract_first()
            yield scrapy.Request(real_url, callback=self.details , dont_filter=True)
        for raw_url in row_urls:
            real_url = begain_url+ raw_url.xpath('.//a/@href').extract_first()
            yield scrapy.Request(real_url, callback=self.details, dont_filter=True)

    def details(self, response):
        name = response.xpath('//span[@itemprop="name"]/text()').extract_first()
        description = response.xpath('//p[@itemprop="description"]/text()').extract_first()
        place = response.xpath('//div[@itemprop="address"]/p/text()').extract_first()
        postal_code = response.xpath('//span[@itemprop="postalCode"]/text()').extract_first()
        location = response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first()
        mobile_number = response.xpath('//span[@itemprop="telephone"]/text()').extract_first()
        address = place + postal_code + location
        email = response.xpath('//a[@id="email-link"]/text()').extract_first()
        weblink =  response.xpath('//a[@id="website-link"]/text()').extract_first()

        yield {
            'Name':name,
            'Response URL': response.url,
            'Description': description,
            'Address': address,
            'Contact Number':  mobile_number,
            'Email':email,
            'WebSite': weblink,


        }
# -*- coding: utf-8 -*-
import scrapy


class ZorgkSpider(scrapy.Spider):
    name = 'zorgk'
    allowed_domains = ['zorgkaartnederland.nl/overzicht/organisatietypes']
    start_urls = ['http://zorgkaartnederland.nl/overzicht/organisatietypes/']
    all_link = 'https://www.zorgkaartnederland.nl'
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
           'Category Name', 'Name', 'Addres', 'Postal code & city', 'Telephone', 'Website', 'Link'

        ]
    };

    def parse(self, response):
        all_category = response.xpath('//li[@class="list-group-item"]/a')
        for category in all_category:
            a = category.xpath('.//@href').extract_first()
            category_url = self.all_link + a
            category_name = category.xpath('.//text()').extract_first()
            yield scrapy.Request(url=category_url, callback=self.inside_category, dont_filter=True, meta={'Category Name': category_name,'link':category_url})

    def inside_category(self, response):
        url = response.url
        category_name = response.meta['Category Name']
        category_url = response.meta['link']
        all_category_inside = response.xpath('//h4[@class="media-heading title orange"]/a')
        for product_a in all_category_inside:
            a = product_a.xpath('.//@href').extract_first()
            product_link = self.all_link+a
            yield scrapy.Request(url=product_link, callback=self.details, dont_filter=True, meta={'Category Name': category_name, 'link': category_url})

        try:
            if 'pagina' not in url:
                number = response.xpath('//div[@class ="pagination_holder"]//li/a/text()')[-1].extract()
                int_number = int(number)
                if int_number > 1:
                    for i in range(2, int_number+1):
                        next_page = category_url +'/pagina' + str(i)
                        yield scrapy.Request(url=next_page, callback=self.inside_category, dont_filter=True, meta={'Category Name': category_name, 'link': category_url})

                else:
                    pass
        except IndexError:
            pass

    def details(self, response):
        category_name = response.meta['Category Name']
        url = response.meta['link']
        name = response.xpath('//span[@itemprop="name"]/text()').extract_first()
        adres1 = response.xpath('//span[@class="address_content"]/text()').extract_first().split()
        adres2 = response.xpath('//div[@class="address_row"]/span/span/text()').extract()
        tel = response.xpath('//span[@itemprop="telephone"]/text()').extract_first()
        web_link = response.xpath('//a[@itemprop="url"]/text()').extract_first()

        yield {
            'Category Name': category_name,
            'Name': name,
            'Addres': adres1,
            'Postal code & city':adres2,
            'Telephone': tel,
            'Website': web_link,
            'Link': url
        }







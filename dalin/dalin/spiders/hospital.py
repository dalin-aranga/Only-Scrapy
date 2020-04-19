# -*- coding: utf-8 -*-
import scrapy
from ..items import Hospital


class HospitalSpider(scrapy.Spider):
    name = 'hospital'
    allowed_domains = ['findalocalvet.com/Find-a-Veterinarian.aspx']
    start_urls = ['http://findalocalvet.com/Find-a-Veterinarian.aspx']
    city_fist_part = 'http://www.findalocalvet.com/'
    city_fist_part2 = 'http://www.findalocalvet.com'

    custom_settings = {

        'FEED_EXPORT_FIELDS': [
                               'City_name',
                               'Hospital_name',
                               'Hospital_url',
                               'Telephone',
                               'Address',
                               ]
    };

    def parse(self, response):
        all_city = response.xpath('//div[@id="SideByCity"]/div/div/a')
        for city in all_city:
            item = Hospital()
            city_url = self.city_fist_part + city.xpath('.//@href').extract_first()
            city_name = city.xpath('.//text()').extract_first()
            item['City_name'] = city_name
            yield scrapy.Request(url=city_url, callback=self.parse_inside_city, dont_filter=True, meta={'item1': item})

    def parse_inside_city(self, response):
        all_hospital_link = response.xpath('//h3/a[@class="fn org"]')
        for hospital in all_hospital_link:
            try:
                item2 = response.meta['item1']
            except KeyError:
                continue
            hospital_url = hospital.xpath('.//@href').extract_first()
            absolute_url = self.city_fist_part2 + hospital_url
            yield scrapy.Request(url=absolute_url, callback=self.details, dont_filter=True, meta={'item3': item2})
        try:
            next_page_url = self.city_fist_part2+response.xpath('//a[contains(text(),"Next")]/@href').extract_first()
            meta = {'item2': response.meta['item1']}
            yield scrapy.Request(url=next_page_url, callback=self.parse_inside_city, dont_filter=True, meta=meta)
        except TypeError:
            pass

    def details(self, response):
        item4 = response.meta['item3']
        hospital_name = response.xpath('//div[@class="Results-Header"]/h1/text()').extract_first()
        url = response.url
        tel = response.xpath('//strong[@class="tel Phone"]/text()').extract_first()
        add = response.xpath('//div[@class="adr"]/span/text()').extract()
        item4['Hospital_name'] = hospital_name
        item4['Hospital_url'] = url
        item4['Telephone'] = tel
        item4['Address'] = add

        yield item4


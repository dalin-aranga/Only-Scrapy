# -*- coding: utf-8 -*-
import scrapy


class TrouveSpider(scrapy.Spider):
    name = 'trouve'
    allowed_domains = ['trouverunsophrologue.fr/']
    start_urls = ['http://www.trouverunsophrologue.fr']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Catagori Name", "Name", "Address", "Postal code", "TelePhone Number", "Village", "Email", "Profile Link"

        ]
    };

    def parse(self, response):
        for i in range(0, 9):
            url = 'http://www.trouverunsophrologue.fr/mots-acouphenes-m40-p' + str(i)+ '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 10):
            url = 'http://www.trouverunsophrologue.fr/mots-adolescence-m41-p' + str(i)+ '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 7):
            url = 'http://www.trouverunsophrologue.fr/mots-cancer-m42-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 14):
            url = 'http://www.trouverunsophrologue.fr/mots-enfance-m43-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 11):
            url = 'http://www.trouverunsophrologue.fr/mots-entreprise-m44-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 13):
            url = 'http://www.trouverunsophrologue.fr/mots-perinatalite-m45-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 6):
            url = 'http://www.trouverunsophrologue.fr/mots-personnes-agees-m48-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 4):
            url = 'http://www.trouverunsophrologue.fr/mots-sexualite-m47-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 15):
            url = 'http://www.trouverunsophrologue.fr/mots-sommeil-m46-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

        for i in range(0, 5):
            url = 'http://www.trouverunsophrologue.fr/mots-sport-m49-p' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.inside_catagori, dont_filter=True)

    def inside_catagori(self, response):
        all_member = response.xpath('//div[@class="column_in_description_site_category"]/a')
        for member in all_member:
            member_url = self.start_urls[0] + member.xpath('.//@href').extract_first()
            yield scrapy.Request(url=member_url, callback=self.details, dont_filter=True)

    def details(self, response):
        url = response.url
        specilist = response.xpath('//div[@class ="form_details"][1]/div[@class ="infos_details"]/text()').extract_first().split()
        name = response.xpath('//div[@class ="show_arbo"]/a[3]/text()').extract_first()
        try:
            address = response.xpath('//div[@class ="form_details"][1]/div[@class ="infos_details"]/text()')[1].extract().split()
        except IndexError:
            address = response.xpath('//div[@class ="form_details"][1]/div[@class ="infos_details"]/text()')[
                0].extract().split()

        postal_code = response.xpath('//div[@class ="form_details"][2]/div[@class ="infos_details"]/text()').extract_first()
        village = response.xpath('//div[@class ="form_details"][3]/div[@class ="infos_details"]/text()').extract_first()
        tel = response.xpath('//div[@class ="form_details"][4]/div[@class ="infos_details"]/text()').extract_first()
        email = response.xpath('//div[@class ="form_details"][5]/div[@class ="infos_details"]/text()').extract_first()

        yield {
            'Catagori Name': specilist,
            'Name': name,
            'Address': address,
            'Postal code': postal_code,
            'Village': village,
            'TelePhone Number': tel,
            'Email': email,
            'Profile Link': url
        }



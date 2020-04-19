# -*- coding: utf-8 -*-
import scrapy


class ContactgegevensSpider(scrapy.Spider):
    name = 'contactgegevens'
    allowed_domains = ['almanak.overheid.nl']
    start_urls = ["https://almanak.overheid.nl/Provincies/",
        "https://almanak.overheid.nl/Ministeries/",
        "https://almanak.overheid.nl/Staten-Generaal/",
        "https://almanak.overheid.nl/Hoge_Colleges_van_Staat/",
        "https://almanak.overheid.nl/Adviescolleges/",
        "https://almanak.overheid.nl/Openbare_lichamen_voor_beroep_en_bedrijf/",
        "https://almanak.overheid.nl/Koepelorganisaties/",
        "https://almanak.overheid.nl/Kabinet_van_de_Koning/",
        "https://almanak.overheid.nl/Rechtspraak/",
        "https://almanak.overheid.nl/Politie_en_brandweer/",
        "https://almanak.overheid.nl/Caribisch_Nederland/"]
    absolate_url = ['https://almanak.overheid.nl']

    def parse(self, response):
        for page_link in self.start_urls:
            yield scrapy.Request(page_link, callback=self.inside_page)

    def inside_page(self, response):
        page_inside_url = response.xpath('//div[@data-roo-element="organisationtype-content"]/ul[@class="list--linked"]/li')
        for inside_page in page_inside_url:
            two_insideurl = self.absolate_url[0] + inside_page.xpath('.//a/@href').extract_first()
            yield scrapy.Request(two_insideurl, callback=self.inside_page_details)

    def inside_page_details(self, response):
        name = response.xpath('//div[@data-roo-element="organisation-content"]/div/h1/text()').extract_first().strip().replace('\r\n\t\t\t\t\t\r\n\t\t\r\n\t\t\t \r\n\t\t\t\t(','')
        tag = response.xpath('//div[@class="modal__inner alert_inner"]/h2[@class ="alert alert--info"]/text()').extract_first().strip().replace(' \r\n\t\t\t\t\t\t\t\t\t\t','')
        organisatietype = response.xpath('//table[@class="table__data-overview"]/tr[1]/td[@data-before="Organisatietype"]/text()').extract_first().strip()
        telefoon = response.xpath('//table[@class="table__data-overview"]/tr/td[@data-before="Telefoon"]/text()').extract_first(default='No contact NUmber').strip()
        fax = response.xpath('//table[@class="table__data-overview"]/tr[4]/td[@data-before="Fax"]/text()').extract_first(default='No Fax Number').strip()
        email = response.xpath('//table[@class="table__data-overview"]/tr/td[@data-before="E-mail"]/a/@href').extract_first(default='No E-mail').strip()
        internet = response.xpath('//table[@class="table__data-overview"]/tr/td[@data-before="Internet"]/a/@href').extract_first(default='No web Link').strip()
        try:
            beschrijving = response.xpath('//div[@data-roo-element="organisation-content"]/div/p/text()')[1].extract()
        except IndexError:
            beschrijving = 'Non Beschrijving'
        try:
            bezoekadres1 = response.xpath('//table[@class="table__data-overview"]/tr[1]/td[@data-before="Bezoekadres"]/text()').extract_first().strip()
            bezoekadres2 = response.xpath('//table[@class="table__data-overview"]/tr[1]/td[@data-before="Bezoekadres"]/text()')[1].extract().strip()
            bezoekadres = bezoekadres1 + ' ,' + bezoekadres2
        except IndexError:
            bezoekadres = response.xpath('//table[@class="table__data-overview"]/tr[1]/td[@data-before="Bezoekadres"]/text()').extract_first().strip()
        except AttributeError:
            bezoekadres = 'NOn Bezoekadres'
        try:
            postadres1 = response.xpath('//table[@class="table__data-overview"]/tr/td[@data-before="Postadres"]/text()')[0].extract().strip()
            postadres2 = response.xpath('//table[@class="table__data-overview"]/tr/td[@data-before="Postadres"]/text()')[1].extract().strip()
            postadres = postadres1 + ' ,' + postadres2
        except IndexError:
            postadres = response.xpath('//table[@class="table__data-overview"]/tr/td[@data-before="Postadres"]/text()').extract_first()
        except AttributeError:
            postadres = 'Non Postadres'

        yield {
            'Name': name,
            'Tag': tag,
            'Organisatietype': organisatietype,
            'Telefoon': telefoon,
            'Fax': fax,
            'E-mail': email,
            'Internet': internet,
            'Beschrijving': beschrijving,
            'Bezoekadres': bezoekadres,
            'Postadres': postadres

        }




























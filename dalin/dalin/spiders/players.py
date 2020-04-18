# -*- coding: utf-8 -*-
import scrapy
from ..items import DalinItem

#large data in csv
class PlayersSpider(scrapy.Spider):
    name = 'players'
    allowed_domains = ['nfl.com/players/search?category=name']
    start_urls = ['http://www.nfl.com']

    def parse(self, response):

        list =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        for letter in list:
            link = 'http://www.nfl.com/players/search?category=lastName&filter='+letter+'&playerType=current'
            yield scrapy.Request(url=link, callback=self.parse_pofile, dont_filter=True)

    def parse_pofile(self,response):
        profile_link_odd = response.xpath('//tr[@class="odd"]/td[3]')
        profile_link_even = response.xpath('//tr[@class="even"]/td[3]')

        for odd_pofile in profile_link_odd:
            pofile_link = self.start_urls[0]+ odd_pofile.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=pofile_link, callback=self.details, dont_filter= True)

        for even_pofile in profile_link_even:
            pofile_link = self.start_urls[0]+even_pofile.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=pofile_link, callback=self.details, dont_filter= True )

        try:
            next_page = response.xpath('//span[@class="linkNavigation floatRight"]/a[contains(text(),"next")]/@href').extract_first()
            next_page_url = self.start_urls[0]+ next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse_pofile ,dont_filter=True)
        except TypeError:
            pass

    def details(self, response):
        items = DalinItem()
        url = response.url
        player_name = response.xpath('//span[@class="player-name"]/text()').extract_first().strip()
        team_name = response.xpath('//p[@class="player-team-links"]/a/text()').extract_first()
        items['Player_Profile_link'] = url
        items['Player_Name'] = player_name
        items['Team_Name'] = team_name

        profile_link_logos = response.urljoin(url).replace('profile','gamelogs')
        yield scrapy.Request(url=profile_link_logos, callback=self.details_logo, dont_filter=True, meta={'item1': items})

    def details_logo(self, response):
        item2 = response.meta['item1']
        year_list = response.xpath('//select[@id ="season"]/option/text()').extract()
        for year in year_list:
            year_link = response.url + '?season=' + year
            yield scrapy.Request(url=year_link, callback=self.logos_details, dont_filter=True, meta={'item4': item2})

    def logos_details(self, response):
        items3 = response.meta['item4']
        all_seasion = response.xpath('//table[@class ="data-table1"]/tbody/tr')
        ssion_name = response.xpath('//tr[contains(@class,"player-table-header")]')
        for seasion2 in ssion_name:
            seasion_name = seasion2.xpath('.//td[1]/text()').extract_first()
            for seasion in all_seasion:
                week_number = seasion.xpath('.//td[1]/text()').extract_first()
                if week_number is None:
                    continue
                else:
                    week_number = seasion.xpath('.//td[1]/text()').extract_first()
                    game_date = seasion.xpath('.//td[2]/text()').extract_first()
                    try:
                        opp = seasion.xpath('.//td[3]/a[2]/text()').extract_first().strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t \t', '')
                    except AttributeError:
                        continue
                    g = response.xpath('//table[@class ="data-table1"]/tbody/tr/td[5]/text()').extract_first()
                    gs = response.xpath('//table[@class ="data-table1"]/tbody/tr/td[6]/text()').extract_first()

                    items3['Seasion_Name'] = seasion_name
                    items3['Week_Number'] = week_number
                    items3['Game_Date'] = game_date
                    items3['Opp'] = opp
                    items3['G'] = g
                    items3['GS'] = gs
                    yield items3















import scrapy
import re
import json


class Demo(scrapy.Spider):
    name = 'demo'
    start_urls = ['http://quotes.toscrape.com/js/']

    def parse(self, response):
        data = re.findall("var data =(.+?);\n", response.body.decode("utf-8"), re.S)
        if data:
            ls = json.loads(data[0])
            for i in ls:
                tags = i['tags']
                author_name = i['author']['name']
                author_link = i['author']['goodreads_link']
                author_slug = i['author']['slug']
                text = i['text']
                yield {
                    'Tags': tags,
                    'Author Name': author_name,
                    'Author Link': author_link,
                    'Author Slug': author_slug,
                    'Text': text
                }
                try:
                    next_page = 'http://quotes.toscrape.com' + response.xpath('//li[@class="next"]/a/@href').extract_first()
                    yield scrapy.Request(url=next_page, callback=self.parse)

                except:
                    pass

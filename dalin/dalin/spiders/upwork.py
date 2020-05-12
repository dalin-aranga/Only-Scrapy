import scrapy


class Upwork(scrapy.Spider):
    name = 'upwork'
    custom_settings = {
        'FEED_EXPORT_FIELDS': [

            'Title',
            'Price',
            'Duration',
            'Desription',
            'Job URL'

            ]
    };

    def start_requests(self):
        url = 'https://www.upwork.com/search/jobs/?q=Scrapy'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        job_a = response.xpath('//a[@class="job-title-link break visited"]')
        for url in job_a:
            job_link = 'https://www.upwork.com' + url.xpath('.//@href').extract_first()
            print(job_link)
            yield scrapy.Request(url=job_link, callback=self.details)

        for i in range(2, 15):
            url = 'https://www.upwork.com/search/jobs/?q=Scrapy&page='+str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def details(self, response):
        description = ''
        url = response.url
        title = response.xpath('//h2[@class="m-0-bottom"]/text()').extract_first()
        price = response.xpath('//strong/text()').extract_first()
        description1 = response.xpath('//div[@class="job-description break"]/div//text()').extract()
        for i in description1:
            description = description +i.strip().replace('\n','')
        duration = response.xpath('//strong[@class="m-sm-right primary"]/following-sibling::span/text()').extract_first()

        yield {
            'Title': title,
            'Price': price,
            'Duration': duration,
            'Desription': description,
            'Job URL': url
        }

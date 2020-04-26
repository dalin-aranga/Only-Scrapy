# -*- coding: utf-8 -*-
import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com/gp/search/other/ref=sr_in_c_A?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=c&ie=UTF8&qid=1574672143']
    start_urls = ['http://amazon.com/gp/search/other/ref=sr_in_c_A?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=c&ie=UTF8&qid=1574672143']
    all_url = 'http://amazon.com'
    header ={
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '324',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'ubid-main=134-8670089-3937656; session-id=144-2142269-7384406; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:LK"; x-wl-uid=1m5X6m9KH3NDVvfabRJnnJg7IJELzQvbcJZgAvzrhBNNMNJNSPd7dT2rxf/d2Ugnco4eJd6zd9PE=; session-token=fllTDddLJUKyGMvpO5k1gy50OQoX8Ea7L3nP5us6jD0GhqRcFHxGVDpZInZkt1aLMo9ridEyKm/lqOUVC0v9J8bZ5V0wWy09+ePsWfOaYC5B32j+Rtz9zqpcoTJ1crTsRF8VRMQfEzHhguoa0CGIGNIBITNklzk4Mr/8JngbOVYaCVrPjkwXtRDj/3dAQUNq; x-amz-captcha-1=1587683808816062; x-amz-captcha-2=1dgg73Q7/Wkm1UsRyTyvHQ==; skin=noskin; csm-hit=tb:s-SGCP318YGCWEZZKCFFXD|1587857874631&t:1587857875646&adb:adblk_no',
        'origin': 'https://www.amazon.com',
        'pragma': 'no-cache',
        'referer': 'https://www.amazon.com/gp/search/other/ref=sr_in_c_A?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=c&ie=UTF8&qid=1574672143',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def parse(self, response):
        all_cpart = response.xpath('//li/span[@class="a-list-item"]/a')
        for a in all_cpart:
            apart = a.xpath('.//@href').extract_first()
            link = self.all_url+apart
            yield scrapy.Request(url=link, callback=self.inside, dont_filter=True, headers=self.header)

    def inside(self, response):
        all_product = response.xpath('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]')
        for item in all_product:
            item_name = item.xpath('.//a/span[@class="a-size-medium a-color-base a-text-normal"]/text()').extract_first()
            item_url = self.all_url + item.xpath('.//a[@class="a-link-normal a-text-normal"]/@href').extract_first()
            yield {
                'Product Name': item_name,
                'Product Url': item_url
            }
        next_page = response.xpath('//li/a[contains(text(),"Next")]/@href').extract_first()
        if next_page is None:
            pass
        else:
            next_page_url = self.all_url + next_page
            yield scrapy.Request(url=next_page_url, callback=self.inside, dont_filter=True, headers=self.header)
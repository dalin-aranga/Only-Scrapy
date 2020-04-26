# -*- coding: utf-8 -*-
import scrapy
import json


class SchoolSpider(scrapy.Spider):
    name = 'school'
    allowed_domains = ['directory.ntschools.net/#/schools']
    start_urls = ['https://directory.ntschools.net/#/schools']
    headers ={
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'BIGipServerdirectory.ntschools.net_443.app~directory.ntschools.net_443_pool=764084746.20480.0000',
        'Host': 'directory.ntschools.net',
        'Pragma': 'no-cache',
        'Referer': 'https://directory.ntschools.net/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36',
        'X-Requested-With': 'Fetch'
    }

    def parse(self, response):
        url = 'https://directory.ntschools.net/api/System/GetAllSchools'
        yield scrapy.Request(url=url, callback=self.school, headers=self.headers, dont_filter=True)

    def school(self, response):
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
        data_row = response.body
        data = json.loads(data_row)
        for school in data:
            is_school = school['itSchoolCode']
            real_url = base_url + is_school
            yield scrapy.Request(url=real_url,callback=self.details, dont_filter=True, headers=self.headers)

    def details(self, response):
        data_row = response.body
        data = json.loads(data_row)
        yield {
            'Name': data['name'],
            'Physical Address': data['postalAddress']['displayAddress'],
            'Postal  Address': data['postalAddress']['displayAddress'],
            'Email': data['mail'],
            'Phone': data['telephoneNumber']

        }




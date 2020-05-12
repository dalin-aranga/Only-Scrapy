import scrapy
import pandas as pd

df = pd.read_json('/home/dalin/PycharmProjects/scrapy/train/train/spiders/postcodes.json')
list = []
for i in range(0, 2981):
    code = df['postcode'][i]
    list.append(code)


class OnTheMarket(scrapy.Spider):
    name = 'onthemarket'
    custom_settings = {
        'FEED_EXPORT_FIELDS': [

            'Post Code',
            'Miles',
            'Title',
            'Price',
            'Contact',
            'Property',
            'Map',
            'Floor Plan',
            'Address',
            'Home URL',
            'Description',
            'Image',

            ]
    };

    def start_requests(self):
        for i in range(0, 2981):
           code = list[i]
           lower = code.lower()
           url = 'https://www.onthemarket.com/new-homes/property/'+lower+'/'
           yield scrapy.Request(url=url, callback=self.parse,meta={'postcode':code})
           break

    def parse(self, response):
        code = response.meta['postcode']
        miles = response.xpath('//div[@id="radius-clipped"]/text()').extract_first()
        house_url = response.xpath('//p[@class="price-text"]/a')
        for url in house_url:
            price = url.xpath('.//text()').extract_first()
            house_link = 'https://www.onthemarket.com'+url.xpath('.//@href').extract_first()
            yield scrapy.Request(url=house_link,callback=self.details, meta={'Price': price,'postcode':code,'Miles': miles})
            break

        next_page = response.xpath('//div[@class="page-nav"]/ul/li/a/@href')[-1].extract()
        if next_page is not None:
            next_page_url = 'https://www.onthemarket.com'+next_page
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            pass

    def details(self, response):
        miles = response.meta['Miles']
        house_url = response.url
        price = response.meta['Price']
        code = response.meta['postcode']
        title = response.xpath('//div[@class="details-heading"]/h1/text()').extract_first()
        contact = response.xpath('//div[@class="content-phone"]/text()').extract_first().replace('Call ','')
        property = response.xpath('//ul[@class="property-features"]/li/text()').extract()
        description = response.xpath('//div[@class="description"]/text()').extract_first().strip()
        map = response.url+'#map'
        floor_plan = response.xpath('//div[@class="image-wrapper main-image-wrapper"]/img/@src')[-1].extract()
        image = response.xpath('//div[@class="image-wrapper main-image-wrapper"]/img/@src').extract()
        address = response.xpath('//div[@class="details-heading"]/p/text()')[-1].extract()

        yield {
            'Post Code': code,
            'Miles': miles,
            'Title': title,
            'Price': price,
            'Contact': contact,
            'Property': property,
            'Map': map,
            'Floor Plan': floor_plan,
            'Address': address,
            'Home URL': house_url,
            'Description': description,
            'Image': image
        }



import scrapy


class Upwork(scrapy.Spider):
    name = 'sport'
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            'post_title',
            'post_excerpt',
            'post_content',
            'post_status',
            'regular_price',
            'sale_price',
            'Images',
            'tax:product_type',
            'SKU Number',
            'tax:product_cat',
            'tax:product_tag_choose1',
            'Choose Cat1',
            'tax:product_tag_choose2',
            'Choose Cat2',
            'tax:product_tag_choose3',
            'Choose Cat3',
            'tax:product_tag_choose4',
            'Choose Cat4',
            'Additional_info_Cat',
            'Additional_info_value',



        ]

    };

    def start_requests(self):
        for i in range(1,174):
            url = 'https://www.slatergartrellsports.com.au/page/'+str(i)+'/?s&post_type=product'
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        product_link = response.xpath('//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')
        for link in product_link:
            a_link = link.xpath('.//@href').extract_first()
            yield scrapy.Request(url=a_link,callback=self.details)

    def details(self,response):
        title = response.xpath('//h1[@class="product_title entry-title"]/text()').extract_first()
        price = response.xpath('//span[@class="woocommerce-Price-amount amount"]/text()').extract_first()
        try:
            price2 = response.xpath('//span[@class="woocommerce-Price-amount amount"]/text()')[1].extract()
            variation = 'variable'

        except:
            price2 = ''
            variation = 'simple'

        sort_description = response.xpath('//div[@class="woocommerce-product-details__short-description"]/p/text()').extract_first()
        sku = response.xpath('//span[@class="sku"]/text()').extract_first()
        cat = response.xpath('//span[@class="posted_in"]/a/text()').extract()
        img = response.xpath('//img[@class="wp-post-image"]/@src').extract_first()
        l_des = response.xpath('//div[@id="tab-description"]//p/text()').extract()
        try:
            product_tag1 = response.xpath('//tr[1]/td[@class="value"]/select/option/text()').extract_first()
            label1 = response.xpath('//tr[1]/td[@class="label"]/label/text()').extract_first()
            tag_name1 = product_tag1 + '-' + label1
            choose1 = response.xpath('//tr[1]/td[@class="value"]/select/option/text()').extract()
            choose_option1= choose1[1:]
        except:
            tag_name1 = 'None'
            choose_option1 ='None'
        try:
            product_tag2 = response.xpath('//tr[2]/td[@class="value"]/select/option/text()').extract_first()
            label2 = response.xpath('//tr[2]/td[@class="label"]/label/text()').extract_first()
            tag_name2 = product_tag2 + '-' + label2
            choose2 = response.xpath('//tr[2]/td[@class="value"]/select/option/text()').extract()
            choose_option2 = choose2[1:]
        except:
            tag_name2 = 'None'
            choose_option2 ='None'

        try:
            product_tag3 = response.xpath('//tr[3]/td[@class="value"]/select/option/text()').extract_first()
            label3 = response.xpath('//tr[3]/td[@class="label"]/label/text()').extract_first()
            tag_name3 = product_tag3 + '-' + label3
            choose3 = response.xpath('//tr[3]/td[@class="value"]/select/option/text()').extract()
            choose_option3 = choose3[1:]
        except:
            tag_name3 = 'None'
            choose_option3 ='None'

        try:
            product_tag4 = response.xpath('//tr[4]/td[@class="value"]/select/option/text()').extract_first()
            label4 = response.xpath('//tr[4]/td[@class="label"]/label/text()').extract_first()
            tag_name4 = product_tag4 + '-'+label4
            choose4 = response.xpath('//tr[4]/td[@class="value"]/select/option/text()').extract()
            choose_option4 = choose4[1:]
        except:
            tag_name4 = 'None'
            choose_option4 ='None'

        tag_name = response.xpath('//div[@id="tab-additional_information"]//tr/th/text()').extract()
        tag_value= response.xpath('//div[@id="tab-additional_information"]//tr/td[@class="woocommerce-product-attributes-item__value"]/p/a/text()').extract()
        if response.xpath('//div[@class="woo-social-buttons"]'):
            public = 'publish'
        else:
            public = 'Not publish'

        yield {
            'post_title': title,
            'post_excerpt': sort_description,
            'post_content': l_des,
            'post_status': public,
            'regular_price': price,
            'sale_price': price2,
            'Images': img,
            'tax:product_type': variation,
            'SKU Number': sku,
            'tax:product_cat': cat,
            'tax:product_tag_choose1': tag_name1,
            'tax:product_tag_choose2': tag_name2,
            'tax:product_tag_choose3': tag_name3,
            'tax:product_tag_choose4': tag_name4,
            'Choose Cat1': choose_option1,
            'Choose Cat2': choose_option2,
            'Choose Cat3': choose_option3,
            'Choose Cat4': choose_option4,
            'Additional_info_Cat': tag_name,
            'Additional_info_value': tag_value

        }







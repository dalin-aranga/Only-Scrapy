import scrapy


class Demo(scrapy.Spider):
    name = 'ebay'
    start_urls = ['https://www.ebay.com/b/Apple/bn_21819543']

    def parse(self, response):
        each_book = response.xpath('//li[@class="s-item   "]/div/div[2]')
        for book in each_book:
            bool_url = book.xpath('.//a/@href').extract_first()
            name = book.xpath('.//a/h3/text()').extract_first()
            price = book.xpath('.//div/div/span[@class="s-item__price"]/text()').extract_first()
            print(bool_url)
            print(name)
            print(price)
            yield scrapy.Request(url=bool_url, callback=self.details, meta={'Name':name, 'Price':price})
            break

        next_page = response.xpath('//a[@rel ="next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.xpath('//a[@rel ="next"]/@href').extract_first()
            yield scrapy.Request(url=next_page, callback=self.parse)

        else:
            pass

    def details(self, response):
        url = response.url
        name = response.meta['Name']
        price = response.meta['Price']
        product_information = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Information")]/following-sibling::ul/li/text()').extract_first()
        brand = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Identifiers")]/following-sibling::ul/li/div[contains(text(),"Brand")]/following-sibling::div/text()').extract_first()
        mpn = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Identifiers")]/following-sibling::ul/li/div[contains(text(),"MPN")]/following-sibling::div/text()').extract_first()
        upc = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Identifiers")]/following-sibling::ul/li/div[contains(text(),"UPC")]/following-sibling::div/text()').extract_first()
        model = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Identifiers")]/following-sibling::ul/li/div[contains(text(),"Model")]/following-sibling::div/text()').extract_first()
        ebay_pr_id = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Identifiers")]/following-sibling::ul/li/div[contains(text(),"eBay Product ID (ePID)")]/following-sibling::div/text()').extract_first()
        style = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Style")]/following-sibling::div/text()').extract_first()
        storage_Capacity =response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Style")]/following-sibling::div/text()').extract_first()
        color = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Style")]/following-sibling::div/text()').extract_first()
        modelNumber = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Model Number")]/following-sibling::div/text()').extract_first()
        network = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Network")]/following-sibling::div/text()').extract_first()
        screen_size = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Screen Size")]/following-sibling::div/text()').extract_first()
        connectivity = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Connectivity")]/following-sibling::div/text()').extract_first()
        processor = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Processor")]/following-sibling::div/text()').extract_first()
        manufacturer = response.xpath('//div[@class="spec-row"]/h2[contains(text(),"Product Key Features")]/following-sibling::ul/li/div[contains(text(),"Manufacturer")]/following-sibling::div/text()').extract_first()

        yield {
            'Name': name,
            'Price': price,
            'URL': url,
            'product_information': product_information,
            'brand' :brand,
            'MPN': mpn,
            'UPC': upc,
            'Model': model,
            'ID': ebay_pr_id,
            'Syle': style,
            'Storage': storage_Capacity,
            'Color': color,
            'ModelNumber ': modelNumber,
            'Network': network,
            'Screen size': screen_size,
            'Connectivity': connectivity,
            'Processor': processor,
            'Manufacturer': manufacturer
        }


















#'//a[@rel ="next"]/@href'
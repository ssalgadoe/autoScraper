import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from autotrader.items import AutotraderItem
from scrapy.http.request import Request




class AutotraderSpider(scrapy.Spider):
    name = 'autotrader'
    #allowed_domains = ['wwwb.autotrader.ca']
   
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=0&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=15&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=30&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']	
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=45&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=60&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=75&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=195&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=450&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=855&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch']
#    start_urls = ['file:///tmp/tmpk6lop04h.html']
#    start_urls = ["https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=99975&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch"]
#    start_urls = ["https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs=99960&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch"]
    
    counter = 8
    
#    url_str = "https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs="+str(counter*step)+"&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch"
#    print(url_str)
#    start_urls = [url_str]
    
    def start_requests(self):
        step = 15
        for i in range(29,33):
            url_str = "https://www.autotrader.ca/cars/on/bolton/?rcp=15&rcs="+str(i*step)+"&srt=4&prx=100&prv=Ontario&loc=L7E%202E1&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch"
            print(url_str)
            yield Request(url_str, self.parse)

        
    def parse(self, response):
        print('Processing..' + response.url)
             
        #urls = response.xpath("//*[@class='listing-details']/h2/a/@href").extract()
        urls = response.xpath("//*[@class='base-listing-v2']/div[@class='col-xs-12 result-item']/div/div[@class='col-xs-3 fixed-photo-column']/div/a/@href").extract()
        for a in urls:
             url = response.urljoin(a)
             #print(url)
             try:
                 yield scrapy.Request(url, callback=self.parse_details)
             except Exception as err:
                 print("Erro {}".format(err))
                 continue
#        url = response.urljoin(urls[0])
##        print(url)
#        yield scrapy.Request(url, callback=self.parse_details)

    def parse_details(self, response):
        url = response.url
        try:
            title = response.xpath("//h1[@class='at-title']/text()").extract_first().strip()
            print(title)
        except Exception as e:
            title = "n/a"     
 
        try:        
            price = response.xpath("//div[@class='currentPrice']/div[@class='at_floatR']/span/text()").extract_first()
            if price == None:
                price = response.xpath("//span[@class='dealerPrice']/text()").extract()[0]
        except Exception as e:
            price = "n/a"    
        print("Price:", price)            
        item = AutotraderItem()
        item['Title'] = title
        item['Price'] = price
        temp = {}
        for i in range(1,10):
            try:
                key1_path = "//div[@class='specList']/div[@class='at_vehicleSpecs'][1]/div["+str(i)+"]/div[1]/span/text()"
                val1_path = "//div[@class='specList']/div[@class='at_vehicleSpecs'][1]/div["+str(i)+"]/div[2]/text()"
                alt_val1_path = "//div[@class='specList']/div[@class='at_vehicleSpecs'][1]/div["+str(i)+"]/div[2]/span/text()"

                key2_path = "//div[@class='specList']/div[@class='at_vehicleSpecs'][2]/div["+str(i)+"]/div[1]/span/text()"
                val2_path = "//div[@class='specList']/div[@class='at_vehicleSpecs'][2]/div["+str(i)+"]/div[2]/text()"
                alt_val2_path = "//div[@class='specList']/div[@class='at_vehicleSpecs'][2]/div["+str(i)+"]/div[2]/span/text()"

                key1 = response.xpath(key1_path).extract()[0].strip()
                key1=key1.replace(" ","")
                if (key1=='Style/Trim'):
                    key1 = 'Trim'
                val1 = response.xpath(val1_path).extract()[0].strip()
                if len(val1) < 1:
                    val1 = response.xpath(alt_val1_path).extract()[0].strip()

                key2 = response.xpath(key2_path).extract()[0].strip()
                key2= key2.replace(" ","")
                if (key2=='Style/Trim'):
                    key2 = 'Trim'
                
                val2 = response.xpath(val2_path).extract()[0].strip()
                if len(val2) < 1:
                    val2 = response.xpath(alt_val2_path).extract()[0].strip()


               # print("item",i,"-", "kv1:", key1,':', val1,"kv2:", key2,':', val2)
                item[key1] = val1
                item[key2] = val2
                temp[key1] = val1
                temp[key2] = val2
            except Exception as e:
                continue
        print(temp)
        yield item
#        i=2
#        key_path = "//div[@class='specList']/div[@class='at_vehicleSpecs']/div["+str(i)+"]/div[1]/span/text()"
#        val_path = "//div[@class='specList']/div[@class='at_vehicleSpecs']/div["+str(i)+"]/div[2]/text()"
#        alt_val_path = "//div[@class='specList']/div[@class='at_vehicleSpecs']/div["+str(i)+"]/div[2]/span/text()"
#        key = response.xpath(key_path).extract()[0].strip()
#        val = response.xpath(val_path).extract()[0].strip()
        
#        key = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[2]/div[1]/span/text()").extract()[0].strip()
#        val = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[2]/div[2]/text()").extract()[0].strip()

 
        
    def parse_details1(self, response):
        url  =response.url
        #print('inside:', url)
        item = AutotraderItem()
        try:
            item['title'] = response.xpath("//h1[@class='at-title']/text()").extract_first().strip()
            print(item['title'])
        except Exception as e:
            item['tile'] = "n/a"
#        try:            
#            item['milage'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[0].strip()
#            if len(item['milage']) < 1:
#                item['milage'] = response.xpath("//div[@class='at_vehicleSpecs']/div[3]/div[2]/text()").extract()[0].strip()
#        except Exception as e:
#            item['milage'] = "n/a"
#        try:    
#            item['status'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[1].strip()
#            if len(item['status']) < 1:
#                item['status'] = "used"
#        except Exception as e:
#            item['status'] = "used"


#        try:        
#            item['price'] = response.xpath("//div[@class='currentPrice']/div[@class='at_floatR']/span/text()").extract_first()
#            if item['price'] == None:
#                item['price'] = response.xpath("//span[@class='dealerPrice']/text()").extract()[0]
#            print(item['price'])
#        except Exception as e:
#            item['price'] = "n/a"

        try:
            make = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[1]/div[2]/span/text()").extract()[0]
            print("good make", make)
            if len(make) < 1:
                make = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[1]/div[2]/span/text()").extract()[0]
                print("bad make", make)
            item['make'] = make    
        except Exception as e:
            print("something went work")
            item['make'] = "n/a"
#        try:
#            item['trim'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[2].strip()
#            if len(item['trim']) < 1:
#                item['trim'] = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[5]/div[2]/text()").extract()[0].strip()
#        except Exception as e:
#            item['trim'] = "n/a"
#        try:    
#            item['body_type'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[3].strip()                      
#            if len(item['body_type']) < 1:
#                item['body_type'] = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[4]/div[2]/text()").extract()[0].strip()
#        except Exception as e:
#            item['body_type'] = "n/a"
        try:    
            #engine = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[4].strip()
            engine = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[6]/div[2]/text()").extract()[0].strip()
            print("public: ",engine)
            if len(item['engine']) < 1:
                engine = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[6]/div[2]/text()").extract()[0].strip()
                print("private: ",engine)
        except Exception as e:
            item['engine'] = "n/a"
#        try:    
#            item['cylinder'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[5].strip()
#            if len(item['cylinder']) < 1:
#                item['cylinder'] = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[7]/div[2]/text()").extract()[0].strip()
#        except Exception as e:
#            item['cylinder'] = "n/a"
#        try:    
#            item['stock_nr'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[8].strip()
#            if len(item['stock_nr']) < 1:
#                item['stock_nr'] = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[8]/div[2]/text()").extract()[0].strip()
#        except Exception as e:
#            item['stock_nr'] = "n/a"
#        try:    
#            item['drivetrain'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[7].strip()
#            if len(item['drivetrain']) < 1:
#                item['drivetrain'] = response.xpath("//div[@class='specList']/div[@class='at_vehicleSpecs']/div[9]/div[2]/text()").extract()[0].strip()
#        except Exception as e:
#            item['drivetrain'] = "n/a"


        
#        item['engine'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[4].strip()
#        item['cylinder'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[5].strip()
#        item['transmission'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[6].strip()
#        item['drivetrain'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[7].strip()
#        item['stock_nr'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[8].strip()
#        item['ext_col'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[9].strip()
#        item['int_col'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[10].strip()
#        item['passengers'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[11].strip()
#        item['doors'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[12].strip()
#        item['fuel_type'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[13].strip()
#        item['city_fuel'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[14].strip()
#        item['hwy_fuel'] = response.xpath("//div[@class='at_vehicleSpecs']/div/div[@class='at_value at_col']/text()").extract()[15].strip()       
#        item['description'] = response.xpath("//div[@class='vehicleDescription']/p/text()").extract_first().strip()
        
        yield item
        


        

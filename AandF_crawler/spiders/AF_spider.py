import scrapy
from scrapy.http import TextResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

class AFSpider(scrapy.Spider):
    name = 'AF'
    allowed_domains = ['abercrombie.com']
    start_urls = [
        'http://www.abercrombie.com.hk/en_HK/mens-sale?om_mid=011016_AF_ACTIVE_HK_A_PROMO_60OFF&linkid=shopmens1&cmp=EMM_011016ANFHKwinterSale60off&om_rid=RSYS71978211'
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        self.driver.maximize_window()
        self.driver.get(response.url)
        self.driver.set_page_load_timeout(30)
        self.driver.execute_script("return document.documentElement.innerHTML;")
        scheight = 0.1
        while scheight < 9.9:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/{})".format(scheight))
            scheight += .01

        res = TextResponse(url=response.url, body=self.driver.execute_script("return document.documentElement.innerHTML;"), encoding='utf-8')

        for item in res.xpath('//div[@class="product-tile"]'):
            item_name = item.xpath('./div[@class="product-name"]/h3/a/text()').extract()[0].strip()
            item_link = item.xpath('./div[@class="product-name"]/h3/a/@href').extract()[0].strip()
            standard_price = item.xpath('./div[@class="product-pricing"]/div/span[@class="text price-standard"]/text()').extract()
            promoted_price = item.xpath('./div[@class="product-pricing"]/div/span[@class="text promotional-price"]/text()').extract()
            standard_price = float(standard_price[0].strip().split('$')[1].replace(',', ''))
            promoted_price = float(promoted_price[0].strip().split('$')[1].replace(',', ''))
            discount_rate = ((standard_price - promoted_price) / standard_price) * 100
            print item_name, ", ", discount_rate, "% OFF", ", ", item_link

        self.driver.close()

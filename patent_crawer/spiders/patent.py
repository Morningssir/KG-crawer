# -*- coding: utf-8 -*-
import re
import scrapy
from patent_crawer.items import PatentCrawerItem
from scrapy_splash import SplashRequest


class PatentSpider(scrapy.Spider):
    name = 'patent'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://wanfangdata.com.cn/search/searchList.do?searchType=patent&pageSize=50&searchWord=(题名%3A医疗)%2520%25E8%25B5%25B7%25E5%25A7%258B%25E5%25B9%25B4%253A2017&showType=detail&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all&navSearchType=']

    def start_requests(self):
        for url in self.start_urls:
            for i in range(1, 101):
                yield SplashRequest(url=url+'&page='+str(i), callback=self.get_page_data, args={'wait': 4})

    @classmethod
    def get_page_data(self, response):
        try:
            patents = response.xpath('//div[@class="ResultBlock"]/div[@class="ResultList "]')
            for patent in patents:
                target_url = "http://wanfangdata.com.cn" + patent.xpath('./div[@class="ResultCont"]/div[@class="title"]/a[1]/@href').extract()[0]
                yield SplashRequest(url=target_url, callback=self.get_patent_data, args={'wait': 6})
        except Exception as err:
            print(err)

    @classmethod
    def get_patent_data(self, response):
        try:
            details = response.xpath('//div[@class="left_con"]')

            dp_list = details.xpath('./div[@class="left_con_top"]/ul[@class="info"]/li[9]/div[2]/a')
            rl_list = response.xpath('//div[@id="similar_patent_reference"]/table')

            item = PatentCrawerItem()

            item['su'] = details.xpath('normalize-space(./div[@class="left_con_top"]/div[@class="abstract"]/div/text())').extract()[0].split(" ")[1]
            item['nm'] = details.xpath('normalize-space(./div[@class="left_con_top"]/div[@class="title"]/text())').extract()[0]
            item['id'] = details.xpath('./div[@class="left_con_top"]/ul[@class="info"]/li[2]/div[2]/text()').extract()[0]
            item['dt'] = details.xpath('./div[@class="left_con_top"]/ul[@class="info"]/li[3]/div[2]/text()').extract()[0]
            item['dp'] = []
            for dp in dp_list:
                developer = dp.xpath('./text()').extract()[0]
                item['dp'].append(developer)
            item['rl'] = []
            for rl in rl_list:
                relation = re.split('[(",)]', str(rl.xpath('./tbody/tr/td[2]/a[2]/@onclick').extract()[0]))[5]
                item['rl'].append(relation)

            yield(item)
        except Exception as err:
            print(err)
# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.selector import Selector
from meizi.items import  XiciItem

class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']

    start_urls = (
        'http://www.xicidaili.com/nn/1',
    )

    # def start_requests(self):
    #     url = 'http://www.xicidaili.com/nn/1'
    #     scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        table = sel.xpath('//table[@id="ip_list"]')[0]
        trs = table.xpath("//tr")[1:]
        for tr in trs:
            item = XiciItem()
            item['ip'] = tr.xpath("td[2]/text()").extract()[0]
            item['port'] = tr.xpath("td[3]/text()").extract()[0]
            item['scheme'] = tr.xpath("td[6]/text()").extract()[0]
            print('--- xici item is %s://%s:%s  ----'%(item['scheme'],item['ip'],item['port']))

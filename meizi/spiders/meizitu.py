# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.selector import Selector
from meizi.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]

    start_urls = (
        'http://www.meizitu.com/',
    )

    def parse(self, response):
        # sel是页面源代码，载入scrapy.selector
        sel = Selector(response)
        # 每个连接，用@href属性
        count = 0;
        for link in sel.xpath('//h2/a/@href').extract():
            # 请求=Request(连接，parese_item)
            # 测试代码只抓取一页，避免ip 被ban
            if(count < 1) :
                print('--------------------------------------current link is %s -------------------------'%(link))
                request = scrapy.Request(link, callback=self.parse_item)
                count = count + 1
                yield request  # 返回请求

        # # 获取页码集合
        # pages = sel.xpath('//*[@id="wp_page_numbers"]/ul/li/a/@href').extract()
        # print('pages: %s' % pages)  # 打印页码
        # for page in pages:
        #     # if len(pages) > 2:#如果页码集合>2
        #     page_link = page
        #     page_link = page_link.replace('/a/', '')  # 图片连接=page_link（a替换成空）
        #     print('page_link', page_link)
        #     request = scrapy.Request('http://www.meizitu.com/a/%s' % page_link, callback=self.parse)
        #     yield request  # 返回请求

    def parse_item(self, response):
        # l=用ItemLoader载入MeizituItem()
        re = []
        l = ItemLoader(item=MeizituItem(), response=response)
        # 名字
        l.add_xpath('name', '//h2/a/text()')
        # 标签
        l.add_xpath('tags', "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p")
        # 图片连接
        l.add_xpath('image_urls', "//div[@id='picture']/p/img/@src", Identity())
        # url
        l.add_value('url', response.url)
        re.append(l.load_item())
        print("response result is %s" %(re))
        # return re
        return l.load_item()

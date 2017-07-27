# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from meizi import settings
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem

class MeiziPipeline(object):
    def process_item(self, item, spider):
        return item


class ImageDownloadPipeline(ImagesPipeline):
    default_headers = {
        'Host': 'mm.howkuai.com',
        'Connection': 'keep - alive',
        'Upgrade - Insecure - Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 58.0 .3029.110 Safari / 537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
    }

    # http://blog.csdn.net/php_fly/article/details/19688595
    # file path 使用
    def file_path(self, request, response=None, info=None):
        dir_path = '%s' % (settings.IMAGES_STORE)
        # 建立目录名字和项目名称一致
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        us = request.url.split('/')[3:]
        print("-------us is %s------------ ", us)
        image_file_name = '_'.join(us)
        file_path = '%s/%s' % (dir_path, image_file_name)
        print('------file path is %s-------' % (file_path))
        return file_path


    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,headers = self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
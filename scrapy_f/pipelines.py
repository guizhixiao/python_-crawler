# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid

import requests, time, re
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ScrapyFPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 下载图片，如果传过来的是集合需要循环下载
        # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
        yield Request(url=item['imgsrc'], meta={'name': item['title']}, headers={'referer':item['referer']})

    def item_completed(self, results, item, info):
        # 是一个元组，第一个元素是布尔值表示是否成功
        if not results[0][0]:
            raise DropItem('下载失败')
        return item

        # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字

    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 提取url前面名称作为图片名
        image_name = request.url.split('/')[-1]
        # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        folder_strip = re.sub(r'[？\\*|“<>:/]', '', str(name))
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(folder_strip, image_name)
        return filename



#     def process_item(self, item, spider):
#         # print(item)
#         #下载图片并保存图片名称
#         print("item:"+item["href"])
#         r = requests.get(item["href"])
#         filename = str(uuid.uuid4()) + '.jpg'
#         # name = time.time()
#         with open(filename, 'wb') as f:
#             f.write(r.content)
#
#         return item
#
# if __name__ == '__main__':
#     r = requests.get('https://i.meizitu.net/thumbs/2019/06/189408_13a41_236.jpg')
#     filename = str(uuid.uuid4()) + '.jpg'
#     # name = time.time()
#     with open(filename, 'wb') as f:
#         f.write(r.content)
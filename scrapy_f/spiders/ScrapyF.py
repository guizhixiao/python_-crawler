import scrapy
from bs4 import BeautifulSoup

from scrapy_f.items import ScrapyFItem


class ScrapyF(scrapy.Spider):
    name = 'scrapyf'
    allowed_domains = ["www.mzitu.com"]
    start_urls = ['https://www.mzitu.com/taiwan/']

    def parse(self, response):
        liList = response.css('div.postlist ul#pins li')
        for li in liList:
            item = ScrapyFItem()
            item["title"] = li.css('li img::attr(alt)').extract_first()
            item["imgsrc"] = li.css('li img::attr(data-original)').extract_first()
            item["href"] = li.css('li>a').attrib['href']
            item['referer'] = response.url
            yield item


    def cssparse(self, response):
        pass


def beautifulSoupparse(self, response):
    soup = BeautifulSoup(response.body, 'lxml')
    liLists = soup.select('div.postlist ul#pins li')
    for liList in liLists:
        item = ScrapyFItem()
        soup = BeautifulSoup(str(liList), 'lxml')
        item["title"] = soup.select('li span a')[0].string
        item["imgsrc"] = soup.select('li img')[0].attrs['src']
        item["href"] = soup.select('li>a')[0].attrs['href']
        # print(title,' <==> ' ,imgsrc)
        item['referer'] = response.url
        yield item


def test():
    str1 = '''<li><a href="https://www.mzitu.com/189408" target="_blank"><img alt="貌美似景甜，长腿正妹身姿妖娆温婉可人" class="lazy" data-original="https://i.mei19/06/189408_13a41_236.jpg" height="354" src="https://i.meizitu.net/pfiles/img/lazy.png" width="236"/></a><span><a href="https://www.mzitu.com/189408" target="_blank">貌美似景甜，长腿正妹身姿妖娆温婉可人</a></span><span class="time">2019-06-17</span></li>
'''
    href = BeautifulSoup(str1, 'lxml').select('li img')
    print(href[0].contents)


if __name__ == '__main__':
    test()

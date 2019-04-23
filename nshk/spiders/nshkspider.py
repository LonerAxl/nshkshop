# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import re
import nshk.items as items


class Nshkspider(scrapy.Spider):
    name = 'nshkspider'
    allowed_domains = ['store.nintendo.com.hk']
    start_urls = []

    def parse_detail(self, response):
        list = response.css('div.category-product-list').extract_first()
        list = re.sub(">\s*<","><",list)
        list = re.sub("[\s]{2,}", "", list)
        list_Selector = Selector(text=list)
        item_list = list_Selector.css('div.category-product-item').extract()
        for i in item_list:
            selector = Selector(text=i)
            item = items.NshkItem()
            item['name'] = selector.css('a.category-product-item-title-link::text').extract_first()
            item['price'] = selector.css('span.price::text').extract_first()
            item['pubdate'] = selector.css('div.category-product-item-released::text').extract_first()
            yield item

    def start_requests(self):
        yield scrapy.Request(url='https://store.nintendo.com.hk/games/all-released-games', callback=self.parse_detail, dont_filter=True)


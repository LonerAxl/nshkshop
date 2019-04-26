# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import re
import nshk.items as items
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import NewConnectionError
from selenium.common.exceptions import NoSuchElementException

import time
import math

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


class NSJPsalespider(scrapy.Spider):
    name = 'nsjpsalespider'
    allowed_domains = ['store.nintendo.co.jp']
    start_urls = ['https://store.nintendo.co.jp/dl-soft/sale.html?page=1']
    #start_urls = ['https://ec.nintendo.com/JP/ja/titles/70010000005323']
    prefs = {
        'profile.default_content_setting_values':{
            'images':2,
        }
    }

    proxys = ['1.202.245.84:8080', '101.251.215.232:8081']

    def __init__(self):
        options = Options()
        # options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        options.add_argument('--headless')
        options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse_detail(self, response):

        self.driver.get(response.url)

        time.sleep(3)

        try:
            self.driver.find_element_by_css_selector('button.o_c-button-border.o_c-button-size--slim')
            button = self.driver.find_element_by_css_selector('button.o_c-button-fill.o_c-button-size--slim')
            actions = ActionChains(self.driver)
            actions.click(button).perform()
            time.sleep(3)
        except NoSuchElementException:
            pass

        source = re.sub(">\s*<", "><", self.driver.page_source)
        selector = Selector(text=source)
        item = items.NSSaleItem()

        item['name'] = selector.css('div.o_c-page-title>h1::text').extract_first()
        oP = selector.css('div.o_p-product-detail__fixed-price::text').extract_first()
        if oP is None or oP == "":
            item['originalPrice'] = selector.css('span.o_p-aoc-detail__fixed-price::text').extract_first()
        else:
            item['originalPrice'] = oP

        rate = selector.css('div.o_c-tag.o_p-product-detail__label-view::text').extract_first()
        if rate is None or rate == "":
            item['rate'] = selector.css('div.o_c-tag.o_p-aoc-detail__label-view>span::text').extract_first()
        else:
            item['rate'] = rate

        fP = selector.css('div.o_p-product-detail__price--price::text').extract_first()
        if fP is None or fP == "":
            item['finalPrice'] = selector.css('div.o_p-aoc-detail__price--price::text').extract_first()
        else:
            item['finalPrice'] = fP
        enddate = selector.css('div.o_c-accordion__text.o_p-product-detail-accordion__content>ul>li::text').extract_first()
        item['endDate'] = enddate.split(' ')[0]+enddate.split(' ')[1]
        column = selector.css('div.o_c-2col-list-border__row').extract()[-2]
        item['language'] = Selector(text=column).css('div.o_c-2col-list-border__right::text').extract_first()
        yield item

    def parse_list(self, response):
        self.driver.get(response.url)
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.NAME, "item-card"))
            )
        finally:
            self.driver.quit()
        source = re.sub(">\s*<", "><", self.driver.page_source)
        list_Selector = Selector(text=source)
        item_list = list_Selector.css('ext-item-card-list>div>ext-item-card').extract()
        for i in item_list:
            selector = Selector(text=i)
            url = selector.css('item-card::attr(url)').extract_first()
            print(i)
            yield scrapy.Request(url=url, callback=self.parse_detail)
            time.sleep(2)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        source = re.sub(">\s*<", "><", self.driver.page_source)
        list_Selector = Selector(text=source)
        item_list = list_Selector.css('ext-item-card-list>div>ext-item-card').extract()
        url_list=[]

        for i in item_list:
            selector = Selector(text=i)
            url = selector.css('item-card::attr(url)').extract_first()
            url_list.append(url)

        for i in range(190,len(url_list)):
            if i%50==0:
                self.driver.quit()
                self.driver = None
                options = Options()

                options.add_argument('--headless')
                options.add_experimental_option('prefs', self.prefs)
                self.driver = webdriver.Chrome(chrome_options=options)
            yield scrapy.Request(url=url_list[i], callback=self.parse_detail, dont_filter=True)
            time.sleep(2)

        self.driver.quit()


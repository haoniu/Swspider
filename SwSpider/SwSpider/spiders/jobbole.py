# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、获取文章列表页的文章url并交给scrapy下载后并进行解析
        2、获取下一页的url
        :param response:
        :return:
        """

        #解析列表中的所有文章的url并交给scrapy下载后进行解析
        post_urls = response.css('#archive > .floated-thumb > div.post-meta > p:nth-child(1) > a.archive-title::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse_detail)

        #提取下一页
        next_url = response.css('#archive > div.navigation.margin-20 > a.next.page-numbers::attr(href)').extract_first()

        if next_url:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse)


    def parse_detail(self,response):
        re_title = response.css('div.entry-header > h1::text').extract_first()
        create_date = response.css('div.entry-meta > p::text').extract_first().strip().replace("·","").strip()
        content = response.css('div.entry').extract_first()



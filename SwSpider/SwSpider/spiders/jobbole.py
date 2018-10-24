# -*- coding: utf-8 -*-
import scrapy
import datetime

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from SwSpider.items import JobBoleArticleItem
from SwSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、获取文章列表页的文章url并交给scrapy下载后并进行解析
        2、获取下一页的url
        post_url = 'http://blog.jobbole.com/114458/'
        response.url = 'http://blog.jobbole.com/all-posts/'
        :param response:
        :return:
        """

        #解析列表中的所有文章的url并交给scrapy下载后进行解析  #archive > div:nth-child(1) > div.post-thumb > a
        post_nodes = response.css('#archive >div.floated-thumb> div.post-thumb > a')
        for post_node in post_nodes:
            img_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":img_url},callback=self.parse_detail)

        #提取下一页
        next_url = response.css('#archive > div.navigation.margin-20 > a.next.page-numbers::attr(href)').extract_first()

        if next_url:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse)


    def parse_detail(self,response):
        article_item = JobBoleArticleItem()

        re_title = response.css('div.entry-header > h1::text').extract_first()
        create_date = response.css('div.entry-meta > p::text').extract_first().strip().replace("·","").strip()
        content = response.css('div.entry').extract_first()
        front_image_url = response.meta.get("front_image_url",'')  #文章封面

        #处理时间
        try:
            create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        #通过Item_loader加载item
        d = create_date

        article_item['title'] = re_title
        article_item['create_date'] = create_date
        article_item['content'] = content
        article_item['front_image_url'] = [front_image_url]
        article_item['url_object_id'] = get_md5(response.url)
        article_item['url'] = response.url

        yield article_item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

class SwspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8")

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipleline(object):
    '''
    调用scrapy提供的json export 导出文件
    '''
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    '''
    同步存储数据到数据库中
    '''

    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','root','swspider',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = """
            INSERT INTO jobbole_article(url_object_id,title,url,create_time,content)
            VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['url_object_id'],item['title'],item['url'],item['create_date'],item['content']))
        self.cursor.commit()


class MysqlTwistedPipline(object):
    '''
    异步存储数据到数据库中
    '''

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset="utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
                    INSERT INTO jobbole_article(url_object_id,title,url,create_time,content,front_image_url)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,(item['url_object_id'], item['title'], item['url'], item['create_date'], item['content'], item['front_image_path']))

class ArticleImagesPipeline(ImagesPipeline):
    '''
    处理图片
    '''

    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        return item
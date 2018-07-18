# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy.utils.project import get_project_settings
import pymongo

class MySqlPipeline(object):
  """docstring for MySql"""
  def open_spider(self, spider):
    # 连接数据库
    # self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='123456', db='movie', charset='utf8')

    # 将配置文件读到内存中，是一个字典
    settings = get_project_settings()
    host = settings['DB_HOST']
    port = settings['DB_PORT']
    user = settings['DB_USER']
    password = settings['DB_PASSWORD']
    dbname = settings['DB_NAME']
    dbcharset = settings['DB_CHARSET']

    self.conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=dbname, charset=dbcharset)

  def process_item(self, item, spider):
    # 写入数据库中
    sql = 'insert into movie_table(post, name, socre, type, director, editor, actor, long_time, introduce) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (item['post'], item['name'], item['score'], item['_type'], item['director'], item['editor'], item['actor'], item['long_time'], item['introduce'])
    # 执行sql语句
    self.cursor = self.conn.cursor()
    try:
      self.cursor.execute(sql)
      print('#' * 10)
      self.conn.commit()
    except Exception as e:
      print('*' * 10)
      print(e)
      self.conn.rollback()

    return item

  def close_spider(self, spider):
    self.cursor.close()
    self.conn.close()

class MyMongoDbPipeline(object):
  def open_spider(self, spider):
    # 链接数据库
    self.conn = pymongo.MongoClient(host='localhost', port=27017)
    # 选择数据库
    # 没有这个库会自动创建
    db = self.conn.movie
    # 选择集合
    self.collection = db.movie_col


  def process_item(self, item, spider):
    # 来一个item，就应该写入到mongodb中
    self.collection.insert(dict(item))

  def close_spider(self, spider):
    self.conn.close()
    


class MovieprojectPipeline(object):
    def open_spider(self, spider):
        self.fp = open('movie.txt', 'w', encoding='utf8')

    def process_item(self, item, spider):
        obj = dict(item)
        string = json.dumps(obj, ensure_ascii=False)
        self.fp.write(string + '\n')
        return item

    def close_spider(self, spider):
        self.fp.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class EcigforumPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = 'localhost',
            db = 'XXXX', #database name
            user = 'XXXX', #user name
            passwd = 'XXXX', #password
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute("""select 1 from EcigForum where PostID = %s""", (item['postID'],))
        ret = tx.fetchone()
        if ret:
            tx.execute("""update EcigForum set forum_name=%s, threadID = %s,title=%s,postID=%s,content=%s,username=%s,userTitle=%s,userJoinDate=%s,userLocation=%s,time=%s where postID = %s
                """,(item['forum_name'],item['threadID'],item['title'],item['postID'],item['content'],item['username'],item['userTitle'],item['userJoinDate'],item['userLocation'],item['time'],item['postID']))
        else:
            tx.execute("""insert into EcigForum(forum_name,threadID,title,postID,content,username,userTitle,userJoinDate,userLocation,time)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,(item['forum_name'],item['threadID'],item['title'],item['postID'],item['content'],item['username'],item['userTitle'],item['userJoinDate'],item['userLocation'],item['time']))



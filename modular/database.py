# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import os
import pymysql
import re
import time

class DataBase:
    def __init__(self):
        '''
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'username': 'root',
            'password': 'root',
            'databaseName': 'db',
            'prefix': 'h2o_short_url_'
        }
        self.prefix = config.get('prefix')
        self.connect = pymysql.connect(host=config.get('host'), port=config.get('port'), user=config.get('username'), passwd=config.get('password'), db=config.get('databaseName'))
        '''
        self.prefix = os.environ.get('PREFIX')
        self.connect = pymysql.connect(host=os.environ.get('HOST'), port=int(os.environ.get('PORT')), user=os.environ.get('USERNAME'), passwd=os.environ.get('PASSWORD'), db=os.environ.get('DATABASE_NAME'))
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.connect.close()
    
    def existenceTable(self, name):
        sql = 'show tables'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = re.findall('(\'.*?\')', str(data))
        data = [re.sub("'", '', data_count) for data_count in data]
        return f'{self.prefix}{name}' in data

    def createCoreTable(self):
        sql = f'''
            CREATE TABLE `{self.prefix}core` (
                `key_` varchar(255) NOT NULL,
                `value_` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`key_`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)
        sql = f'insert into `{self.prefix}core` VALUES ("title", "氧化氢短网址");'
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'insert into `{self.prefix}core` VALUES ("keyword", "氧化氢短网址");'
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'insert into `{self.prefix}core` VALUES ("description", "一切是那么的简约高效.");'
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'insert into `{self.prefix}core` VALUES ("domain", "");'
        self.cursor.execute(sql)
        self.connect.commit()

    def createUrlTable(self):
        sql = f'''
            CREATE TABLE `{self.prefix}url` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `type_` varchar(255) DEFAULT NULL,
                `domain` varchar(255) DEFAULT NULL,
                `long_url` varchar(255) DEFAULT NULL,
                `signature` varchar(255) DEFAULT NULL,
                `valid_time` int(10) DEFAULT NULL,
                `count` bigint(255) DEFAULT NULL,
                `timestmap` int(10) DEFAULT NULL,
                PRIMARY KEY (`id`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def insert(self, type_, domain, longUrl, validTime):
        sql = f'''
            insert into {self.prefix}url (type_, domain, long_url, valid_time, count, timestmap) 
                    VALUES ("{type_}", "{domain}", "{longUrl}", {validTime}, 0, {int(time.time())})
        '''
        self.cursor.execute(sql)
        id_d = self.connect.insert_id()
        self.connect.commit()
        return id_d
    
    def update(self, id_, signature):
        sql = f'update {self.prefix}url set signature = "{signature}" where id = {id_}'
        self.cursor.execute(sql)
        self.connect.commit()
    
    def addCount(self, domain, signature):
        sql = f'update {self.prefix}url set count = count + 1 where domain = "{domain}" and signature = "{signature}"'
        self.cursor.execute(sql)
        self.connect.commit()
    
    def queryWebsiteInformation(self):
        sql = f'select * from {self.prefix}core where key_ = "title" or key_ = "keyword" or key_ = "description" limit 3'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        information = {}
        for dataItem in data:
            information[dataItem.get('key_')] = dataItem.get('value_')
        return information

    def queryDomain(self):
        sql = f'select * from {self.prefix}core where key_ = "domain" limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = data[0].get('value_')
        data = data.split(',')
        return data

    def queryUrlByLongUrl(self, domain, longUrl):
        sql = f'select * from {self.prefix}url where domain = "{domain}" and long_url = "{longUrl}" limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False

    def queryUrlBySignature(self, domain, signature):
        sql = f'select * from {self.prefix}url where domain = "{domain}" and signature = "{signature}" limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False
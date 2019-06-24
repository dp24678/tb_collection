# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import pymysql
from scrapy_redis.pipelines import RedisPipeline
from tb_collection import settings
from tb_collection.settings import \
    MYSQL_DBNAME,\
    MYSQL_PASSWD,\
    MYSQL_USER,\
    MYSQL_HOST,\
    MYSQL_PORT,\
    MONGODB_HOST,\
    MONGODB_PORT
from tb_collection.utils.handle_redis import redis_queue


class TbCollectionPipeline(object):  # MYSQL
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=MYSQL_HOST,  # 数据库地址
            port=MYSQL_PORT,  # 数据库端口
            db=MYSQL_DBNAME,  # 数据库名
            user=MYSQL_USER,  # 数据库用户名
            passwd=MYSQL_PASSWD,  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    # pipeline默认调用
    def process_item(self, item, spider):
        insert_sql = "insert into tb_data(search_uuid," \
                     "page_order," \
                     "rank_order," \
                     "title," \
                     "is_tmall," \
                     "price," \
                     "location," \
                     "shop_name," \
                     "shop_link," \
                     "view_sales," \
                     "pic_url," \
                     "detail_url," \
                     "comment_url," \
                     "comment_count," \
                     "goods_id," \
                     "categories_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 提交事务
        try:
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql, (
                item['search_uuid'],
                item['page_order'],
                item['rank_order'],
                item['title'],
                item['is_tmall'],
                item['price'],
                item['location'],
                item['shop_name'],
                item['shop_link'],
                item['view_sales'],
                item['pic_url'],
                item['detail_url'],
                item['comment_url'],
                item['comment_count'],
                item['goods_id'],
                item['categories_id'])
                                )
            self.connect.commit()  # 提交
            print("保存成功")
        except Exception as e:
            print(e)
            print('异常回滚')
            self.connect.rollback()

            return item  # 必须实现返回
        return item


class TbCollectionRedisPipeline(object):

    # pipeline默认调用
    def process_item(self, item, spider):
        with open("tb_collection/rely/temp.json", "r", encoding="utf8") as f:
            data = json.loads(f.read())  # 当前商品以及对应的所有数据

        goods = data["goods"]  # 商品详情数据
        shop = data["shop"]  # 对应店铺数据
        seller = data["seller"]  # 对应卖家数据

        data['search_uuid'] = item['search_uuid']
        print("页码：", item['page_order'],"排序：",item['rank_order'])
        data['page_order'] = item['page_order']
        data['rank_order'] = item['rank_order']
        data['search_args'] = item['search_args']
        if item['search_args']['data_sources'] == 'APP':
            data['now_page_total'] = item['now_page_total']

        goods["title"] = item["title"]
        goods["is_tmall"] = item['is_tmall']
        goods["price"] = item['price']
        goods['shop_location'] = item['location']
        goods["shop_name"] = item['shop_name']
        goods["shop_click_url"] = item['shop_link']
        goods['confirm_sales_count'] = item['view_sales']
        goods['sales_count'] = item['pay_count']
        goods['picSrc'] = item['pic_url']
        goods['goods_detail_url'] = item['goods_detail_url']
        goods['comment_url'] = item['comment_url']
        goods['comment_count'] = item['comment_count']
        goods['id'] = item['goods_id']
        goods['categoryId'] = item['categories_id']
        seller['sellerId'] = item['seller_id']
        seller['sellerCredit'] = item['seller_credit']
        shop['name'] = item['shop_name']
        shop['location'] = item['location']
        shop['dsr']['description'] = item['dsr_description']
        shop['dsr']['service'] = item['dsr_service']
        shop['dsr']['delivery'] = item['dsr_delivery']

        redis_queue.lpush_item(data)  # 将数据添加到队列中
        spider.loger.info('返回item数据插入redis成功')
        redis_queue.lpush_page_data(data)  # 将数据按照页码的规则插入到对应的页面数据key内
        spider.loger.info('返回页面缓存数据插入redis成功')
        return item



# class TbCollectionMongodbPipeline(object):
#     def __init__(self):
#         # 创建MONGODB数据库链接
#         client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
#         # 指定数据库
#         mydb = client[MONGODB_DBNAME]
#         # 存放数据的数据库表名
#         self.collection = mydb[MONGODB_SHEETNAME]
#
#     def process_item(self, item, spider):
#         data = dict(item)
#         self.collection.insert_one(data)  # 向该集合中插入一条数据
#
#         return item



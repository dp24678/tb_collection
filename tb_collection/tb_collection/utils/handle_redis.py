# _*_coding:utf-8 _*_
#@Time? ? :2019/5/6 15:10
#@Author? :Dapan
#@Email : 248312738@qq.com

"""从网站后台获取到的 搜索词，一个一个添加到 redis 缓存池中"""
import json
import asyncio
import redis
import scrapy
from tb_collection.settings import REDIS_HOST, REDIS_PORT
from threading import Thread
import time


class RedisQueue():
    def __init__(self):
        self.redisPool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            # db=1,
            decode_responses=True  # 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        )
        self.client = redis.StrictRedis(connection_pool=self.redisPool)
        # self.pipeline = self.client.pipeline()  # 创建管道

    def lpush_args(self,args_info):
        self.client = redis.Redis(connection_pool=self.redisPool)
        self.client.lpush("tb_spider:search_args", args_info)

    def brpop_args(self):
        self.client  = redis.Redis(connection_pool=self.redisPool)
        search_args = self.client.brpop("tb_spider:search_args")
        print(search_args)
        print("search_args:",search_args[1])
        return search_args


    def lpush_url(self, uuid, keyword, data_sources, sort_type, page_num):
        self.client = redis.Redis(connection_pool=self.redisPool)
        url_temp = "https://s.taobao.com/search?q={}&sort={}&s={}"
        sort_types_ = {
            "综合排序":"default",
            "销量排序":"sale-desc",
            "信用由高到低":"credit-desc",
            "价格从低到高":"price-asc",
            "价格从高到低":"price-desc",
            "总价从低到高":"total-asc",
            "总价从高到低":"total-desc",
        }

        if data_sources == "PC":
            for i in range(page_num):
                # self.client.lpush("tb_spider:urls", url_temp.format(keyword, sort_types_[sort_type], i*44))
                self.client.lpush("tb_spider:urls-{}".format(uuid), url_temp.format(keyword, sort_type, i*44))
        elif data_sources == "APP":
            pass  # TODO APP
        else:
            pass  # TODO H5


    def brpop_url(self):
        self.client  = redis.Redis(connection_pool=self.redisPool)
        url = self.client.brpop("tb_spider:urls")
        print("url:",url[1])
        return url

    def lpush_page_data(self,data):
        now_page_num = data['page_order']
        query = data['search_args']['keyword']
        data_sources = data['search_args']['data_sources']
        sort_type = data['search_args']['sort_type']
        redis_key = "tb_spider:cache_page_data:{}-{}-{}-{}".format(query, data_sources, sort_type, now_page_num)
        data = json.dumps(data)  # 将数据转换成json字符串插入redis
        print(21,data)
        self.client.lpush(redis_key, data)
        self.client.expire(redis_key,3600)  # 有效期3600s



    def lpush_item(self, item):
        print('00')
        search_uuid = item['search_uuid']
        print(search_uuid)
        print('01')
        print('02')
        data = json.dumps(item)  # 将数据转换成json字符串插入redis
        print('03')
        self.client.lpush("tb_spider:item:{}".format(search_uuid), data)
        print('04')

    def brpop_item(self,search_uuid):
        self.client  = redis.Redis(connection_pool=self.redisPool)
        item = self.client.brpop("tb_spider:item_{}".format(search_uuid))
        print("url:",item[1])
        return item

    def set_page_data(self, key, page_data):
        """
        从redis队列中获取key对应的value，没有时返回none
        :param key:
        :return:
        """
        self.client = redis.Redis(connection_pool=self.redisPool)
        self.client.set('tb_spider:cache_page_data:{}'.format(key), page_data)

    # def get_cookie(self):
    #     """
    #     从cookie池中获取cookie字典，并将获取到的cookie 放在列表最前面
    #     :return:cookie字典
    #     """
    #     cookie_value = self.client.brpoplpush("cookiePool:cookie","cookiePool:cookie")
    #     return cookie_value['cookie_dict']  # 这里使用brpoplpush 与cookie池耦合度比较高后期可以优化


redis_queue = RedisQueue()


if __name__ == '__main__':
    # args_li = [{"keyword": "眼药水", "data_sources": "PC", "sort_type": "销量排序", "page_num": 6},
    #            {"keyword": "数据线", "data_sources": "PC", "sort_type": "销量排序", "page_num": 3}
    #            ]
    #
    # for args in args_li:
    #     redis_queue.lpush_args(args)
    # redis_queue.lpush_args({"sd":1175286518652865387156872586})
    # print(1)
    # while True:
    #     print(redis_queue.brpop_args())
    # # for i in range(100):
    #     # redis_queue.Brpop_url()
    redis_queue.get_cookie( )
# _*_coding:utf-8 _*_
#@Time    :2019/5/6 15:10
#@Author  :Dapan
#@Email : 248312738@qq.com

"""从网站后台获取到的 搜索词，一个一个添加到 redis 缓存池中"""
import json
import redis

from config import REDIS_HOST, REDIS_PORT


class RedisQueue():
    def __init__(self,db):
        self.redisPool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=db,
            decode_responses=True  # 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        )
        self.client = redis.StrictRedis(connection_pool=self.redisPool)


    def lpush_urls_info(self, all_urls_info_data):
        """
        批量将要加入请求队列里的url以及相关数据，添加到redis中
        :param all_urls_info_data: 要添加到队列中的urls_info列表
        :return:
        """
        for urls_info_data in all_urls_info_data:
            self.client.lpush("tb_spider:urls_info", json.dumps(urls_info_data))

        # for urls_info_data in all_urls_info_data:
        #     if urls_info_data not in self.client.get('tb_spider:urls_info'):
        #         print("url lpush失败")


    def brpop_item(self,search_uuid):
        item = self.client.brpop("tb_spider:item:{}".format(search_uuid))
        data = item[1].replace('\n', "")
        return data

    def brpop_page_data(self, key):
        item = self.client.brpop("tb_spider:cache_page_data:{}".format(key))
        data = item[1].replace('\n', "")
        return data


    def get_cache_keys(self):
        """
        获取所有缓存有关的key
        :return: 所有关于缓存的key列表
        """
        self.client = redis.Redis(connection_pool=self.redisPool)
        list_ = []
        for key in self.client.keys():
            if "cache_page_data" in key:
                list_.append(key)
        return list_


    def get_page_data(self,key):
        """
        从redis队列中获取key对应的value，没有时返回none
        :param key:
        :return:
        """
        redis_key = 'tb_spider:cache_page_data:{}'.format(key)
        print('redis_key:',redis_key)
        # length = self.client.llen(redis_key)   # 列表长度
        # print("缓存redis_key对应的列表长度-{}".format(length))
        page_data = []
        linshi_list = self.client.lrange(redis_key, 0, -1)  # 获取指定key对应的列表中所有元素
        print('get_page_data:', linshi_list)
        page_data += [json.loads(i) for i in linshi_list]
        print(111,len(page_data))
        print(112, page_data[0])
        print(113, type(page_data[0]))
        return page_data




redis_queue = RedisQueue(db=0)

if __name__ == '__main__':
    redisPool = redis.ConnectionPool(
        host='192.168.3.11',
        port=6379,
        decode_responses=True  # 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
    )
    client = redis.StrictRedis(connection_pool=redisPool)
    page_data = []
    a = "tb_spider:cache_page_data:{}-{}-{}-{}".format('女装', "APP", '_mix', 3)
    item = client.brpop(a)
    linshi_list = client.lrange(a, 0, -1)  # 获取指定key对应的列表中所有元素
    print('get_page_data:', linshi_list)
    page_data += [json.loads(i) for i in linshi_list]
    print(111, len(page_data))
    print(112, page_data[0])
    print(113, type(page_data[0]))



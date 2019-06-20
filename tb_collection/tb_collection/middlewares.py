# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import re
import time
from urllib import parse
import string

import redis
import requests
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from tb_collection.settings import proxyServer, proxyAuth, UA_LIST
from tb_collection.utils.handle_redis import redis_queue


class TbCollectionSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TbCollectionDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        这是下载中间件中 拦截请求 的方法
        :param request: 拦截到的请求
        :param spider:
        :return:
        """
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        data_sources = request.meta['search_args']['data_sources']

        ua = self.polling_get_ua(UA_LIST)  # 生成随机UA,use_cache_server:使用缓存服务器
        request.headers['User-Agent'] = ua  # 将生成的UA写入请求头中
        # 设置代理
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth

        if data_sources == 'APP':
            self.set_header(request)
        else:
            self.cookie_info_str = requests.get('http://192.168.221.160:5000/get_cookie').text
            cookie_info_dict = json.loads(self.cookie_info_str)
            print(type(json.loads(self.cookie_info_str)))
            # self.username = cookie_info_dict['username']
            cookie_str = cookie_info_dict['cookie']
            cookie_dict = json.loads(cookie_str)
            request.cookies = cookie_dict  # 设置cookie

        # 设置cookie
        # cookie = transCookie(COOKIES)
        # request.cookies = cookie.stringToDict()
        # request.cookies = redis_queue.get_cookie()   #设置cookie

        print("request.headers['User-Agent']:",request.headers['User-Agent'])
        print("request.cookies:",request.cookies)

        return None

    def process_response(self, request, response, spider):
        data_sources = request.meta['search_args']['data_sources']
        print('数据来源：', data_sources)
        # 根据数据来源判断无返回数据的情况
        if data_sources == 'PC':
            data_str = re.search(r'g_page_config = ({.*?"shopcardOff":true}})', response.text)
        elif data_sources == 'APP':
            try:
                text_dict = json.loads(response.text)
                print(text_dict)
                items_list = text_dict["data"]["itemsArray"]
                print(items_list)
                data_str = None if len(items_list) < 0 else 2
            except:
                data_str = None
                print("=========获取异常 data_str：%s==========" % data_str)

        else:
            data_str = None
            print("=========获取异常 data_str：%s==========" % data_str)


        if data_str == None:
            requests.get('http://192.168.221.160:5000/delete_cookie/{}'.format(self.cookie_info_str))
            # 重新发起请求
            request_retry = request.copy()
            cookie_info_str = requests.get('http://192.168.221.160:5000/get_cookie').text
            cookie_info_dict = json.loads(cookie_info_str)
            print(type(json.loads(cookie_info_str)))
            self.username = cookie_info_dict['username']
            cookie_str = cookie_info_dict['cookie']
            cookie_dict = json.loads(cookie_str)
            request_retry.cookies = cookie_dict  # 设置cookie
            return request_retry

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def polling_get_ua(self, list):
        return_ua = list[0]
        list.pop(0)
        list.append(return_ua)
        return return_ua

    def set_header(self, request):
        print('---------请求sign----------')
        deviceId=self.stringRandom(44)
        utdid=self.stringRandom(24)
        t=str(time.time())[:10]
        lng = '119.99023'
        lat = '30.275328'
        data_quote=re.findall('data=(.*)',request.url)[0]
        unquote_data=parse.unquote(data_quote)
        data=json.loads(unquote_data)
        arr=self.get_sign(data,t,utdid,lat,lng,deviceId)
        x_sign=arr['sign']
        request.headers.setdefault('x-appkey','21646297')
        request.headers.setdefault('x-t',t)
        request.headers.setdefault('x-pv','5.1')
        request.headers.setdefault('x-sign',x_sign)
        request.headers.setdefault('x-features', '27')
        request.headers.setdefault('x-ttid', '10005934@taobao_android_8.7.0')
        request.headers.setdefault('x-utdid', utdid)
        request.headers.setdefault('x-devid', deviceId)
        request.headers.setdefault('x-uid', '')

    def get_sign(self, data, t, utdid, lat, lng, deviceId):
        postData = {
            "data": data,
            "xuid": '',
            "t": t,
            "utdid": utdid,
            "appkey": '2164297',
            "lat": lat,
            "lng": lng,
            "api": 'mtop.taobao.wsearch.appsearch',
            "v": '1.0',
            "sid": '',
            "ttid": '10005934@taobao_android_8.7.0',
            "deviceId": deviceId,
            "features": '27',
        }
        url = 'http://47.100.60.78/app/sign?key=763092&data=' + parse.quote(json.dumps(postData))
        response = requests.get(url)
        arr = response.text
        return json.loads(arr)

    def stringRandom(self,n):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, n))
        return ran_str



# class _RetryMiddleware(RetryMiddleware):
#
#     # 当遇到以下Exception时进行重试
#     EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError, ResponseFailed, IOError, TunnelError)
#
#     def __init__(self, settings):
#         '''
#         这里涉及到了settings.py文件中的几个量
#         RETRY_ENABLED: 用于开启中间件，默认为TRUE
#         RETRY_TIMES: 重试次数, 默认为2
#         RETRY_HTTP_CODES: 遇到哪些返回状态码需要重试, 一个列表，默认为[500, 503, 504, 400, 408]
#         RETRY_PRIORITY_ADJUST：调整相对于原始请求的重试请求优先级，默认为-1
#         '''
#         if not settings.getbool('RETRY_ENABLED'):
#             raise NotConfigured
#         self.max_retry_times = settings.getint('RETRY_TIMES')
#         self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
#         self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
#
#     def process_response(self, request, response, spider):
#         # 在之前构造的request中可以加入meta信息dont_retry来决定是否重试
#         if request.meta.get('dont_retry', False):
#             return response
#
#         # 检查状态码是否在列表中，在的话就调用_retry方法进行重试
#         if response.status in self.retry_http_codes:
#             reason = response_status_message(response.status)
#             # 在此处进行自己的操作，如删除不可用代理，打日志等
#             return self._retry(request, reason, spider) or response
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # 如果发生了Exception列表中的错误，进行重试
#         if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
#                 and not request.meta.get('dont_retry', False):
#             # 在此处进行自己的操作，如删除不可用代理，打日志等
#             return self._retry(request, exception, spider)


# class MyRetryMiddleware(RetryMiddleware):
#     logger = logging.getLogger(__name__)
#
#     def delete_cookie(selroxy):
#             requests.get('http://192.168.3.11:5000/delete_cookie/{}'.format(self.username))
#
#
#     def process_response(self, request, response, spider):
#         if request.meta.get('dont_retry', False):
#             return response
#         if response.status in self.retry_http_codes:
#             reason = response_status_message(response.status)
#             # 删除该代理
#             self.delete_proxy(request.meta.get('proxy', False))
#             time.sleep(random.randint(3, 5))
#             self.logger.warning('返回值异常, 进行重试...')
#             return self._retry(request, reason, spider) or response
#         return response
#
#
#     def process_exception(self, request, exception, spider):
#         if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
#                 and not request.meta.get('dont_retry', False):
#             # 删除该代理
#             self.delete_proxy(request.meta.get('proxy', False))
#             time.sleep(random.randint(3, 5))
#             self.logger.warning('连接异常, 进行重试...')
#
#             return self._retry(request, exception, spider)












class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


# class CookiesMiddleware(RetryMiddleware):
#     #cookie池维护
#     def __init__(self, settings, crawler):
#         RetryMiddleware.__init__(self, settings)
#         self.rconn = settings.get("RCONN", redis.Redis(crawler.settings.get('REDIS_HOST', 'localhsot'), crawler.settings.get('REDIS_PORT', 6379)))
#         # saveCookie(self.rconn)
#         print('-------------创建cookie池------------------')
#
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings, crawler)
#
#     def process_request(self, request, spider,):
#         redisKeys = self.rconn.keys()
#         while redisKeys:
#             elem = random.choice(redisKeys)
#             if b"--" in elem:
#                 cookie = json.loads(self.rconn.get(elem))
#                 request.cookies = cookie
#                 request.meta["accountText"] = elem.decode('utf-8')
#                 #时间戳唯一性  开启n个会话
#                 request.meta["cookiejar"]=time.time()   #单spider对应多个会话   cookiejar设置唯一值
#                 # request.meta["cookiejar"]=random.randint(1,100)   #最多保留100个会话
#                 request.meta['cookie']=cookie
#                 break
#
#     def process_response(self, request, response, spider):
#         """
#         请求失败两种情况：
#         1，cookie过期重新登陆获取cookie  firefox无头模式获取cookie
#         2，cookie需要验证，firefox无头模式滑块验证
#         """
#         page_config = re.findall('g_page_config = (.*?);', response.text)
#         if not page_config:
#             try:
#                 redirect_url = response.headers[b"location"]
#                 if b"login.taobao" in redirect_url :  # Cookie失效
#                     #cookie失效等待更新cookie
#                     regetCookie(request.meta['accountText'],self.rconn)
#                 else:
#                     #出现滑块验证
#                     updateCookie(self.rconn,request.meta['accountText'],request.url,request.meta['cookie'])
#                 reason = response_status_message(response.status)
#                 return self._retry(request, reason, spider) or response   # 重试
#             except :
#                 raise IgnoreRequest #忽略该request
#         else:
#             return response


# class RandomUserAgentMiddlware(UserAgentMiddleware):
#     #随机更换user-agent
#     def __init__(self, user_agent=''):
#         super().__init__(user_agent)
#         self.user_agent = user_agent
#         self.ua = UserAgent()
#
#     def process_request(self, request, spider):
#         # a = self.ua.Firefox
#         a = self.ua.random
#         print(117,"产生的UA：",a)
#         request.headers['User-Agent'] = a


# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         request.meta["proxy"] = proxyServer
#
#         request.headers["Proxy-Authorization"] = proxyAuth


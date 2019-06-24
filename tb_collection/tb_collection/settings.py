# -*- coding: utf-8 -*-

# Scrapy settings for tb_collection project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import json

BOT_NAME = 'tb_collection'

SPIDER_MODULES = ['tb_collection.spiders']
NEWSPIDER_MODULE = 'tb_collection.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # 不遵守robots协议

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay


# 设置下载延迟
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3


# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)  不使用中间件中的cookie
# COOKIES_ENABLED = True  # 启用中间件中的cookie，enabled：启用
# COOKIES = 't=289b9bff13131fcda0792c7e61e89795; cna=9Q9jFVeeyEcCAXPDPIULiCCo; tg=0; enc=xJW07sAKdw%2Bvj9p3kkmoWg9FOaSvTgEQINZAnnvcHFVsFq%2FDX%2FjsZmfJG8Ulkz1d%2F3DssPDmX81iHH5XlNsZbQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; _uab_collina=155807347640459462952474; swfstore=160132; x5sec=7b227365617263686170703b32223a226430333362626365656130373638643134343337326134623866383738303836434b757a6a75634645496a7a6b3947657972475649686f4c4f446b7a4d7a59344e4467784f7a453d227d; cookie2=1e268c52d46b6ba6a215dbe6718d3530; _tb_token_=31755886de057; v=0; unb=893368481; sg=%E6%9C%AC1f; _l_g_=Ug%3D%3D; skt=37e328b6e58675b0; publishItemObj=Ng%3D%3D; cookie1=UoH5ZGEDhBUn9eYPhONyOxEUqFtpFH7Wr0LJ48y%2FGzg%3D; csg=4bf8a127; uc3=vt3=F8dBy3vKtbgvWet%2BUns%3D&id2=W8COv7k0Tqmr&nk2=pMflc9G1iSapD%2FulRlU%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; existShop=MTU1ODQyMDQxMg%3D%3D; tracknick=%5Cu94C5%5Cu7B14%5Cu5934%5Cu548C%5Cu4F5C%5Cu4E1A%5Cu672C; lgc=%5Cu94C5%5Cu7B14%5Cu5934%5Cu548C%5Cu4F5C%5Cu4E1A%5Cu672C; _cc_=Vq8l%2BKCLiw%3D%3D; dnk=%5Cu94C5%5Cu7B14%5Cu5934%5Cu548C%5Cu4F5C%5Cu4E1A%5Cu672C; _nk_=%5Cu94C5%5Cu7B14%5Cu5934%5Cu548C%5Cu4F5C%5Cu4E1A%5Cu672C; cookie17=W8COv7k0Tqmr; alitrackid=login.taobao.com; lastalitrackid=login.taobao.com; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=V32FPkk%2FhoypzrZtAqoZbA%3D%3D&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTZ7HEGdtF4bg%3D%3D&tag=8&lng=zh_CN; mt=ci=47_1; JSESSIONID=58EF69C05816E5756998F3C22A557106; whl=-1%260%260%260; l=bBaaGs2cvVnLe8J9BOCgquI8YN_OHIRfguPRwhfMi_5dJ1T_zsQOln4Tte96Vj5P968B4xWabNptzeHb8yvf.; isg=BPr6FaoVcpa7Xf7DAxqoU-IjSyDcA32In6e7vgTz2Q1Z95sx7DsHlDcFQ8OO5_Yd; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0'

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tb_collection.middlewares.TbCollectionSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'tb_collection.middlewares.TbCollectionDownloaderMiddleware': 543,
   # 'tb_collection.middlewares.RandomUserAgentMiddlware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'tb_collection.pipelines.TbCollectionPipeline': 300,
   'tb_collection.pipelines.TbCollectionRedisPipeline': 400
   # 'scrapy_redis.pipelines.RedisPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H0026G1TP41J843D"
proxyPass = "830B52D7F46DA75C"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


# MySQL database config
MYSQL_HOST = '192.168.3.11'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'test'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'dp123'






# scrapy-redis 配置

#使用scrapy-redis里面的去重组件.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 改用scrapy-redis里面的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 指定排序爬取地址时使用的队列，默认是按照优先级排序
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# 可选的先进先出排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# 可选的后进先出排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'            # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
# SCHEDULER_QUEUE_KEY = '%(spider)s:requests'                         # 调度器中请求存放在redis中的key
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"                  # 对保存到redis中的数据进行序列化，默认使用pickle
SCHEDULER_PERSIST = True                                            # 是否在关闭时候保留原来的调度器和去重记录，True=保留，False=清空
# SCHEDULER_FLUSH_ON_START = False                                    # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
# SCHEDULER_IDLE_BEFORE_CLOSE = 10                                    # 去调度器中获取数据时，如果为空，最多等待时间（最后没数据，未获取到）。
# SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'                  # 去重规则，在redis中保存时对应的key
# SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'# 去重规则对应处理的类


# redis 数据库配置
REDIS_HOST = "192.168.3.11"   # 主机名
REDIS_PORT = 6379          # 端口
REDIS_ENCODING = "utf8"   # 编码
# REDIS_PARAMS = {   # 指定数据库
#    'db':1
# }

# MONGODB 主机名
MONGODB_HOST = "192.168.3.11"
# MONGODB 端口号
MONGODB_PORT = 27017


def get_ua_data(file_path):

   with open(file_path,'r') as f:
      f_str = f.read()

   browsers_ua_data = json.loads(f_str)['browsers']
   ua_data = []
   for i in browsers_ua_data:
      ua_data += browsers_ua_data[i]
   return ua_data

# UA 数据,用于创建cookie池
UA_LIST = get_ua_data('./tb_collection/rely/fake_useragent-0.1.11.json')

# app x-sign 数据获取接口
SIGN_API_TEMP = 'http://47.100.60.78/app/sign?key=763092&data='

# 邮件预警系统相关信息
MAIL_CONFIG = {
    'sender_email':'13503998870@163.com', #发送预警邮件的邮箱账号
    'sender_password':'wangyi123',  #邮箱授权码
    'receive_email':'248312738@qq.com',  #要接收邮件的地址
    'mail_title':'Master端-异常预警',  #邮件标题
    'mail_content_1':'获取sign失败,请检查sign服务器是否可用或请求参数' # 预警邮件内容1
}

# 日志功能配置信息
LOG_FILE = "tb_spider.log"
# LOG_LEVEL = "INFO"
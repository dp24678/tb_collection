# _*_coding:utf-8 _*_
#@Time    :2019/5/23 14:09
#@Author  :Dapan
#@Email : 248312738@qq.com

# Redis数据库地址
REDIS_HOST = '192.168.3.11'
# Redis端口
REDIS_PORT = 6379
# Redis密码，如无填None
REDIS_PASSWORD = None
# Redis数据库索引号
REDIS_DB = 2

# 配置信息，无需修改
REDIS_DOMAIN = '*'
REDIS_NAME = '*'

# 代理服务器
proxyHost = "http-pro.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息
proxyUser = "H0026G1TP41J843D"
proxyPass = "830B52D7F46DA75C"


# 账号对应获取手机验证码的查询码  ACCESS_CODE:查询码
ACCESS_CODE={
'tb604869689':'3JK2AARUL',
'tb371219426':'YCWUP12VT'
}

# 账户密码

ACCOUNT_PASSWORD = [
    # ('铅笔头和作业本','taobao19911103@'),

    # ('tb871563600','a570500602','TRK4UGLY7'),  # 获取不到验证码
    # ('tb013825459','a00998','L41AF9CXS'),  # 获取不到验证码
    # ('tb601388587','a570500602','LUA79AJR9'),  # 获取不到验证码
    # ('tb474248673','a570500602','1TJ6H4P0E'),  # 冻结
    # ('tb604869689','a570500602','3JK2AARUL'),  # 冻结
    ('tb236848759','a570500602','8GN2T2YW5'),
    # ('tb832164211','a570500602','WEQT3M4F7'),  # 冻结
    # ('tb645592441','a570500602','5IO2O8UCE'),  # 刮小鸡
    #('tb371219426','a570500602','YCWUP12VT'),  #账号冻结
    # ('tb899403692','a570500602','1OELCJCWO'),  # 刮小鸡
    # ('tb608655067','a570500602','SUNKUHTKZ'),  # 刮小鸡
    # ('tb012675564','a570500602','JRCR0N3E9'),  # 刮小鸡
]


js1 = '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''
js2 = '''() =>{ window.navigator.chrome = { runtime: {},  }; }'''
js3 = '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] }); }'''
js4 = '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [0,1,2], }); }'''

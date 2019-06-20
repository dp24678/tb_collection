import time
from flask import Flask, render_template, request
import json
import uuid
from flask.json import jsonify
from api.utils.handle_redis import redis_queue
from scheduler import scheduler_
from urllib import parse



app = Flask(__name__)

before_total_goods = 0 # 全局变量 当前页之前所有页面数据总量


@app.route('/')
def show_search_page():
    guid = uuid.uuid1()
    search_page_data = {
        "guid":guid
    }
    return render_template("search_page.html", **search_page_data)


@app.route('/get_search', methods=['POST'])
def get_search():
    data = {}  # 所有搜索参数
    search_uuid = request.values["guid"]
    data['search_uuid'] = search_uuid
    data['keyword'] = request.values["key"]
    data['data_sources'] = request.values["type"]
    data['sort_type'] = request.values["sort"]
    page_num_list = [i+1 for i in range(int(request.values["page"]))]
    print("所有要获取的页码列表:",page_num_list)

    # 2、区分出区分出数据要从哪里获取
    cache_page_num_list, request_page_num_list = qufen_data_get_type(page_num_list, data)

    # 3、将请求数据push到队列中，请求数据
    data['page_num_list'] = request_page_num_list

    all_urls_info_list = make_all_urls_info(data)
    redis_queue.lpush_urls_info(all_urls_info_list)  # 把所有需要添加进队列的数据添加进redis

    # # 从缓存中读取要返回的数据
    # for cache_page_num in cache_page_num_list:
    #     key2 = "{}-{}-{}-{}".format(data['keyword'], data['data_sources'], data['sort_type'], cache_page_num)
    #     print('需要在缓存中读取数据的key：',key2)
    #     each_cache_page_data = redis_queue.get_page_data(key2) # 每一个缓存页面数据
    #     print('获取的本页缓存的数据：',len(each_cache_page_data),each_cache_page_data)
    #     search_data += each_cache_page_data
    # 4、读取到缓存中有的所有数据
    search_data = get_data_from_cache(cache_page_num_list, data)
    print('读取所有缓存后的总返回数据:',len(search_data), search_data)

    # 5、读取发起请求获取的数据，从队列中取出
    search_data += get_data_from_request(request_page_num_list, data)

    # for i in range(len(request_page_num_list) * 44):  # TODO 将发起请求的所有数据
    #     each_data = redis_queue.brpop_item(search_uuid).replace('\'', '\"')
    #     each_data_ = json.loads(each_data)
    #     search_data.append(each_data_)
    # # for request_page_num in range(len(request_page_num_list)):  # TODO 将发起请求的所有数据
    # #     key_ = "{}-{}-{}-{}".format(data['keyword'], data['data_sources'], data['sort_type'], request_page_num + 1)
    # #     print(key_)
    # #     a = redis_queue.brpop_page_data(key_)
    # #     print(a)
    # #     search_data.append(a)
    # #     time.sleep(0.1)  # 等待插入所有数据
    # #     each_request_cache_page_data = redis_queue.get_page_data(key_)  # 每一个缓存页面数据
    # #     search_data += each_request_cache_page_data
    # 6、规整两个地方获取到的数据，然后返回给前端页面
    return_data = make_order_data(search_data)
    with open('return_data.json', 'w') as f:
        f.write(json.dumps(return_data))


    return jsonify(return_data)  # jsonify() 方法用于返回json数据比较方便


@app.route('/get_cookie')
def get_cookie():
    cookieInfo = scheduler_.get_one_cookie_info()
    print('请求获得cookie信息：',cookieInfo)
    return jsonify(cookieInfo)


@app.route('/delete_Cookie/<cookie_info_str>', methods=['GET'])
def delete_Cookie(cookie_info_str):
    cookie_info_dict = json.loads(cookie_info_str)
    username = cookie_info_dict['username']
    cookie = cookie_info_dict['cookie']
    print('请求获得cookie信息：',cookie_info_str)
    return scheduler_.delete_and_set_Cookie(username, cookie)




def make_all_urls_info(data):   # 将所有搜索参数转换成redis队列里需要存储的参数字典
    keyword = data["keyword"]
    data_sources = data["data_sources"]
    sort_type = data["sort_type"]
    page_num_list = data["page_num_list"]
    search_uuid = data["search_uuid"]

    all_urls_info = [] # 所有需要被push到数据库中的参数字典列表
    if data_sources == "PC":
        print('pc')
        print(sort_type)
        # 1.1、获取所有集合名称
        url_temp_pc = "https://s.taobao.com/search?q={}&sort={}&s={}"
        for now_page_num in page_num_list:
            url = url_temp_pc.format(keyword, sort_type, (now_page_num-1) * 44)
            each_urls_info= {"search_args": data, "url": url, "now_page_num":now_page_num}
            all_urls_info.append(each_urls_info)

    elif data_sources == "APP":
        print('app')
        print(sort_type)
        data_app_requests = {
            "URL_REFERER_ORIGIN": "https://s.m.taobao.com/h5entry",
            "ad_type": "1.0",
            "apptimestamp": "1559367992",
            "areaCode": "CN",
            "brand": "Xiaomi",
            "countryNum": "156",
            "device": "MI 8",
            "editionCode": "CN",
            "filterEmpty": "true",
            "filterUnused": "true",
            "from": "nt_history",
            "homePageVersion": "v54",
            # "imei":"123456789012344",
            # "imsi":"460028363829028",  无用参数
            "index": "5", "info": "wifi",
            "itemfields": "commentCount,newDsr",
            "jarvisDisable": "true",
            # "latitude":"30.275328",   无用
            # "layeredSrp":"true",
            # "longitude":"119.99023",
            "n": "10", "needTabs": "true",
            "network": "wifi",
            "new_shopstar": "true",
            "page": "1",
            "q": keyword,  # 根据搜索的关键字填写
            "rainbow": "13031,13503,12995,11833,13159,13544,13104,12782,13406,12827,12674",
            "referrer": "com.taobao.taobao",
            "schemaType": "all",
            "searchFramework": "true",
            "search_action": "initiative",
            "search_wap_mall": "false",
            "setting_on": "imgBanners,userdoc,tbcode,pricerange,localshop,smartTips,firstCat,dropbox,realsale,insertTexts,tabs",
            "showspu": "true",
            "sort": sort_type,  # 排序方式
            "sputips": "on",
            "style": "list",
            "subtype": "",
            "sugg": "_5_1",
            "sversion": "6.9",
            "ttid": "10005934@taobao_android_8.7.0",
            # "utd_id":utdid,
            "vm": "nw"}
        url_temp_app = 'https://api.m.taobao.com/gw/mtop.taobao.wsearch.appsearch/1.0/?data={}'
        for now_page_num in page_num_list:
            data_app_requests['page'] = now_page_num
            url = url_temp_app.format(parse.quote(json.dumps(data_app_requests)))
            each_urls_info= {"search_args": data, "url": url, "now_page_num":now_page_num}
            all_urls_info.append(each_urls_info)

    else:
        print('请求H5')
        pass  # TODO H5


    return all_urls_info

def make_order_data(data):
    """
    将获取到的无序数据，进行排序处理
    :param data:排序前的数据
    :return:排序后的数据
    """
    print('===开始规整数据的排序===')
    print('规整前的返回-数据', len(data), data)
    data_return = []  # 排好序的数据
    while len(data) > 0:
        page = data[0]['page_order']
        if page == 1:
            data_return.append(data[0])
            data.pop(0)
            data_return.sort(key=lambda k: k['rank_order'])  # 根据xx排名
        elif page <= data_return[-1]['page_order'] + 1:
            data[0]['rank_order'] = 1 + data_return[-1]['rank_order']
            data_return.append(data[0])
            data.pop(0)
            data_return.sort(key=lambda k: k['rank_order'])  # 根据xx排名
        else:
            el = data.pop(0)
            data.append(el)
            print(data)

    return data_return


def get_data_from_cache(page_num_list, data):
    # 从缓存中读取要返回的数据
    return_data = []  # 需要返回给页面的数据列表
    for page_num in page_num_list:
        key2 = "{}-{}-{}-{}".format(data['keyword'], data['data_sources'], data['sort_type'], page_num)
        print('需要在缓存中读取数据的key：', key2)
        each_cache_page_data = redis_queue.get_page_data(key2)  # 每一个缓存页面数据
        print('获取的本页缓存的数据：', len(each_cache_page_data), each_cache_page_data)
        return_data.extend(each_cache_page_data)
    return return_data

def get_data_from_request(request_page_num_list, data):
    search_uuid = data['search_uuid']
    data_sources = data["data_sources"]
    search_data = [] # 请求获取到的数据

    if data_sources == "PC":
        for i in range(len(request_page_num_list) * 44):
            each_data = redis_queue.brpop_item(search_uuid).replace('\'', '\"')
            each_data_ = json.loads(each_data)
            search_data.append(each_data_)
    elif data_sources == "APP":

        for i in request_page_num_list:
            print("len(request_page_num_list):",len(request_page_num_list))
            #app每页数据量不定，先获取一条，从中拿到本页的总量，然后等待获取
            # 第一条数据
            first_data = redis_queue.brpop_item(search_uuid).replace('\'', '\"')
            first_data_ = json.loads(first_data)
            search_data.append(first_data_)
            print(first_data_)
            now_page_total = first_data_['now_page_total']  # 本页面宝贝数据总量

            # 根据总量，等待获取剩余的所有数据
            print('now_page_total:',now_page_total)
            for i in range(now_page_total - 1):
                print('wkjh',i)
                each_data = redis_queue.brpop_item(search_uuid).replace('\'', '\"')
                print(i)
                each_data_ = json.loads(each_data)
                search_data.append(each_data_)
    else:
        pass
    print("获取监听到的数据后的总返回数据：",len(search_data),search_data)

    return search_data



def qufen_data_get_type(page_num_list, data):
    cache_page_num_list = []  # 需要在缓存读取数据的页面页码列表
    request_page_num_list = []  # 缓存没有，需要发起请求获取的也米娜页码列表
    cache_keys = redis_queue.get_cache_keys()  # 获取缓存相关的所有key
    print('与缓存相关的所有key:', cache_keys)
    for now_page_num in page_num_list:  # 确定每一页的数据如何获取，缓存数据/请求数据
        key1 = "tb_spider:cache_page_data:{}-{}-{}-{}".format(data['keyword'], data['data_sources'], data['sort_type'],
                                                              now_page_num)
        if key1 in cache_keys:  # 找出已经存在的缓存数据
            cache_page_num_list.append(now_page_num)
        else:
            request_page_num_list.append(now_page_num)
    print('需要发起请求的所有页码：', request_page_num_list)
    print('需要在缓存中获取数据的所有页码：', cache_page_num_list)

    return cache_page_num_list, request_page_num_list




if __name__ == '__main__':
    # launch_cookies_pool()
    app.run(host='0.0.0.0', port=5000)


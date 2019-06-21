# -*- coding: utf-8 -*-
import asyncio
import json
import re
import time
from threading import Thread
import scrapy
from scrapy import Spider
from scrapy_redis.spiders import RedisSpider
from tb_collection.items import TbCollectionItem
from tb_collection.utils.handle_redis import redis_queue




class TbSpiderSpider(RedisSpider):
    name = 'tb_spider'
    allowed_domains = ['taobao.com']
    redis_key = "tb_spider:urls_info"

    page_data_list = []  # 每一页的所有商品数据，列表
    headers = {
        'Connection': 'keep - alive',
    }


    def make_requests_from_url(self, data):
        data__ = data.replace('\'','\"')
        print(data__)
        data_ = json.loads(data__)

        search_args = data_["search_args"]  # 搜索参数
        url = data_["url"]
        now_page_num = data_['now_page_num']
        print("当前页：",now_page_num)
        data_sources = search_args['data_sources']
        print(data_sources)

        if data_sources == "PC":
            callback=self.parse_pc
        elif data_sources == "APP":
            callback=self.parse_app
        else:
            callback=self.parse_h5

        return scrapy.Request(
            url=url,
            headers=self.headers,
            callback=callback,
            meta={'search_args': search_args, "now_page_num": now_page_num},
            dont_filter=True
        )




    def parse(self,response):
        print("parse" + "="*50)



    def parse_pc(self, response):
        print('进入parse——pc')
        search_args = response.meta['search_args']
        # now_page_num = response.meta['now_page_num']

        search_uuid = search_args['search_uuid']
        # query = search_args['keyword']
        # data_sources = search_args['data_sources']

        page_str = response.text
        # 将抓取到的页面数据插入到Mongodb数据库中
        # with open("./html/a_{}.html".format(time.time()), "w", encoding='utf8') as f:
        #     f.write(page_str)
        # print(res_data)

        print("请求头携带的UA：",response.request.headers["User-Agent"],"\n")
        data_str = re.search(r'g_page_config = ({.*?"shopcardOff":true}})', page_str).group(1)
        data_dict = json.loads(data_str)
        with open("data.json", "w", encoding='utf8') as f:
            f.write(data_str)
        # page_order：当前页码
        page_order = data_dict["mods"]["pager"]["data"]["currentPage"]  # 页码序号
        print('page_order:',page_order)
        data_list_info = data_dict["mods"]["itemlist"]["data"]["auctions"] # 商品列表
        print("data_list_info:",len(data_list_info))
        page_goods_count = data_dict["mods"]["pager"]["data"]["pageSize"]  # 页面商品总数
        print("页面商品总数:",page_goods_count)

        for i in data_list_info:
            # 相同数据
            index = data_list_info.index(i)
            rank_order = (index + 1) + (page_order-1)*44  # 总排名
            title = i["raw_title"]  # 标题
            is_tmall = 1 if  i["shopcard"]["isTmall"] is True else 0  # 是否是天猫
            price = i["view_price"]  # 价格
            location = i["item_loc"]  # 地址
            shop_name = i["nick"]  # 店铺名
            shop_link = "http:" + i["shopLink"]  # 店铺链接
            pic_url = "http:" + i["pic_url"]  # 主图url
            detail_url = "http:" + i["detail_url"]  # 详情页url
            comment_url = "https://item.taobao.com" + i["comment_url"]  # 评论url
            print("评论总量字符串:",i["comment_count"])
            comment_count = i["comment_count"]  # 评论总数量
            goods_id = i['nid']
            print(goods_id)
            categories_id = i["category"]
            print(categories_id)
            seller_id = i["user_id"]
            if 'sellerCredit' in i["shopcard"].keys():
                seller_credit = i["shopcard"]["sellerCredit"]
            else:
                seller_credit = None

            dsr_description = i["shopcard"]['description'][0]/100  # 宝贝描述
            dsr_delivery = i["shopcard"]['delivery'][0]/100  # 物流服务
            dsr_service = i["shopcard"]['service'][0]/100  # 卖家服务

            # 区别数据
            try:
                sales_str = i["view_sales"]
                if sales_str != "":
                    view_sales,pay_count = self.parse_sales_str_pc(sales_str)
            except Exception as e:
                print(245,e)

                # view_sales = 0
            # pay_count = 0
            # print("sales_str:",sales_str)
            # if "万+" in sales_str:
            #     sales_str = sales_str.replace("万+", "")
            #     if "收货" in sales_str:
            #         view_sales = float(sales_str.replace("人收货", ""))*10000
            #     else:
            #         pay_count = float(sales_str.replace("人付款", ""))*10000
            # elif "+" in sales_str:
            #     sales_str = sales_str.replace("+", "")
            #     if "收货" in sales_str:
            #         view_sales = int(sales_str.replace("人收货", ""))
            #     else:
            #         pay_count = int(sales_str.replace("人付款", ""))
            # else:
            #     if "收货" in sales_str:
            #         view_sales = int(sales_str.replace("人收货", ""))
            #     else:
            #         pay_count = int(sales_str.replace("人付款", ""))
            # hh



            # if "万" in sales_str:
            #     view_sales = float(re.search("([\d.]*?)万", sales_str).group(1)) * 10000
            # elif "+" in sales_str:
            #     view_sales = float(re.search("(\d*?)\+", sales_str).group(1))
            # else:
            #     if search_data['sort'] == "sale-desc":  # 销量排序
            #         view_sales = int(i["view_sales"].replace("人收货", ""))  # 收货人数
            #     else:
            #         pay_count = int(i["view_sales"].replace("人付款", ""))  # 付款人数
            # # if sort_type == "sale-desc":  # 销量排序
            # #     if "万" in sales_str:
            # #         view_sales = float(re.search("([\d.]*?)万",sales_str).group(1))*10000
            # #     elif "+" in sales_str:
            # #         view_sales = float(re.search("(\d*?)\+", sales_str).group(1))
            # #     else:
            # #         view_sales = int(i["view_sales"].replace("人收货",""))  # 收货人数
            # # else:  # 否则都是，，人付款
            # #     if "万" in sales_str:
            # #         view_sales = float(re.search("([\d.]*?)万",sales_str).group(1))*10000
            # #     elif "+" in sales_str:
            # #         view_sales = float(re.search("(\d*?)\+", sales_str).group(1))
            # #     else:
            # #         view_sales = int(i["view_sales"].replace("人付款",""))  # 收货人数
            #
            #
            #
            # # if sort_type == "sale-desc":  # 销量排序
            # #     if "万" in sales_str:
            # #         view_sales = float(re.search("([\d.]*?)万",sales_str).group(1))*10000
            # #     elif "+" in sales_str:
            # #         view_sales = float(re.search("(\d*?)\+", sales_str).group(1))
            # #     else:
            # #         view_sales = int(i["view_sales"].replace("人收货",""))  # 收货人数
            # # elif sort_type == "default":  # 默认排序
            # #     if "万" in sales_str:
            # #         view_sales = float(re.search("([\d.]*?)万",sales_str).group(1))*10000
            # #     elif "+" in sales_str:
            # #         view_sales = float(re.search("(\d*?)\+", sales_str).group(1))
            # #     else:
            # #         view_sales = int(i["view_sales"].replace("人付款",""))  # 收货人数
            # # elif sort_type == "credit-desc":  # 信用排序
            # #     pass
            # # elif sort_type == "price-asc":  # 价格从低到高
            # #     pass
            # # elif sort_type == "price-desc":  # 价格从高到低
            # #     pass
            # # else:
            # #     print(230,"=====排序类型错误=====")
            print(page_order)
            print(rank_order)
            print(title)
            print(is_tmall)
            print(price)
            print(location)
            print(shop_name)
            print(shop_link)
            print(view_sales)
            print(pic_url)
            print(detail_url)
            print(comment_url)
            print(comment_count)
            print(goods_id)
            print(categories_id)
            print("===="*50)

            # 1.数据解析到items对象(先导入)
            item = TbCollectionItem()
            item['search_uuid'] = search_uuid
            item['page_order'] = page_order
            item['rank_order'] = rank_order
            item['title'] = title
            item['is_tmall'] = is_tmall
            item['price'] = price
            item['location'] = location
            item['shop_name'] = shop_name
            item['shop_link'] = shop_link
            item["seller_id"] = seller_id
            item['seller_credit'] = seller_credit
            item['view_sales'] = view_sales
            item['pay_count'] = pay_count
            item['pic_url'] = pic_url
            item['goods_detail_url'] = detail_url
            item['comment_url'] = comment_url
            item['comment_count'] = comment_count
            item['goods_id'] = goods_id
            item['categories_id'] = categories_id
            item['dsr_description'] = dsr_description
            item['dsr_service'] = dsr_service
            item['dsr_delivery'] = dsr_delivery
            item['search_args'] = search_args

            # 2.将item对象提交给管道
            yield item


        # if page_goods_count >= 44:
        #     nextpage_url = "https://s.taobao.com/search?q=鞋子男潮流&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s={}".format(self.i_)
        #     print(99, nextpage_url)
        #     yield scrapy.Request(
        #         url=nextpage_url,
        #         headers=self.headers,
        #         # cookies=self.stringToDict(),
        #         callback=self.parse,
        #         dont_filter=True
        #     )
        #     self.i_ += 44

    # t = GetArgs(headers,parse_)
    # t.start()
    #

    # import asyncio
    # loop = asyncio.get_event_loop()  # 创建一个事件循环
    # loop.run_until_complete(get_args(headers,parse_))  # 将协程加入到事件循环loop
    # new_loop.run_until_complete(get_args(headers,parse_))

    def parse_app(self,response):
        print('进入parse——app')
        search_args = response.meta['search_args']
        now_page_num = response.meta['now_page_num']
        sort_type = search_args['sort_type']
        search_uuid = search_args['search_uuid']

        page_str = response.text
        print(page_str)
        page_data_dict = json.loads(page_str)
        items_list = page_data_dict["data"]["itemsArray"]
        with open('a-{}.json'.format(now_page_num),'w') as f:
            f.write(json.dumps(page_data_dict["data"]))
        items_list_ = [x for x in items_list if 'item_id' in x]  # 包含可用数据的item列表
        print(283, len(items_list_), len(items_list))
        for item_ in items_list_:
            iconList_str = item_['iconList']
            isTmall = 1 if 'tmall' in iconList_str else 0
            seller_id = re.search(r'seller_id:(\d*?);', item_['clickTrace']).group(1)
            category = re.search(r'cat_id:(\d*?);', item_['clickTrace']).group(1)
            dsr_description, dsr_service, dsr_delivery = self.get_app_dsr_list(item_)

            page_order = response.meta['now_page_num']
            rank_order = items_list_.index(item_) + 1 # 总排名
            print('排序：', page_order, rank_order)

            if sort_type == '_sale': # 销量排序展示收获人数，其他展示付款人数
                view_sales = self.parse_sales_str_app(item_['realSales'])
            else:
                view_sales = 0


            item = TbCollectionItem()
            item['search_uuid'] = search_uuid
            item['page_order'] = page_order
            item['rank_order'] = rank_order  # 每一页的数据量不固定，数据完全获取后，前端排序
            item['title'] = item_['title']
            item['is_tmall'] = isTmall
            item['price'] = item_['priceWap']
            item['location'] = item_['location']
            item['shop_name'] = item_['nick']
            item['shop_link'] = item_['shopInfo']['url']
            item["seller_id"] = seller_id
            item['seller_credit'] = int(item_['ratesum'])
            item['view_sales'] = view_sales
            item['pay_count'] = item_['sold']
            item['pic_url'] = item_['pic_path'].replace('_60x60.jpg', '')
            item['goods_detail_url'] = item_['auctionURL']
            item['comment_url'] = ""  # app搜索列表无此数据，待定
            item['comment_count'] = item_['commentCount'] if 'commentCount' in item_ else 0
            item['goods_id'] = item_['item_id']
            item['categories_id'] = category
            item['dsr_description'] = dsr_description
            item['dsr_service'] = dsr_service
            item['dsr_delivery'] = dsr_delivery
            item['search_args'] = search_args
            item['now_page_total'] = len(items_list_)

            # 将item对象提交给管道处理
            yield item

    def parse_h5(self,response):
        print('进入parse——h5')


    def get_app_dsr_list(self, item_):
        dsr_list = []
        dsr_list_str = item_['newDsr'].split(',')
        for i in dsr_list_str:
            dsr = float(i.split(':')[0])
            dsr_list.append(round(dsr, 1))

        return dsr_list


    def parse_sales_str_pc(self,sales_str):
        view_sales = 0
        pay_count = 0
        print("sales_str:", sales_str)
        if "万+" in sales_str:
            sales_str = sales_str.replace("万+", "")
            if "收货" in sales_str:
                view_sales = float(sales_str.replace("人收货", "")) * 10000
            else:
                pay_count = float(sales_str.replace("人付款", "")) * 10000
        elif "+" in sales_str:
            sales_str = sales_str.replace("+", "")
            if "收货" in sales_str:
                view_sales = int(sales_str.replace("人收货", ""))
            else:
                pay_count = int(sales_str.replace("人付款", ""))
        else:
            if "收货" in sales_str:
                view_sales = int(sales_str.replace("人收货", ""))
            else:
                pay_count = int(sales_str.replace("人付款", ""))

        return view_sales,pay_count


    def parse_sales_str_app(self,sales_str):
        print("sales_str:", sales_str)
        if "万" in sales_str:
            sales_str = sales_str.replace("万", "")
            if "收货" in sales_str:
                view_sales = float(sales_str.replace("人收货", "")) * 10000
            else:
                view_sales = 0
        else:
            if "收货" in sales_str:
                view_sales = int(sales_str.replace("人收货", ""))
            else:
                view_sales = 0

        return view_sales












# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbCollectionItem(scrapy.Item):
    # define the fields for your item here like:
    search_uuid = scrapy.Field()  # 全局唯一识别码
    page_order = scrapy.Field()  #  页码
    rank_order = scrapy.Field()  #  全局排序序号
    title = scrapy.Field()  # 1、标题
    is_tmall = scrapy.Field()  # 1、标题
    price = scrapy.Field()  # 2、价格
    location = scrapy.Field()  # 3、地址
    shop_name = scrapy.Field()  # 4、店铺名
    shop_link = scrapy.Field()  # 5、店铺链接
    seller_id = scrapy.Field()  # 卖家ID
    seller_credit = scrapy.Field() # 卖家信用
    view_sales = scrapy.Field()  # 6、确认收货人数
    pay_count = scrapy.Field()  # 付款人数
    pic_url = scrapy.Field()  # 7、主图url
    goods_detail_url = scrapy.Field()  # 8、详情页url
    comment_url = scrapy.Field()  # 9、评论url
    comment_count = scrapy.Field()  # 10、评论总数量
    goods_id = scrapy.Field()  # 11、商品ID
    categories_id = scrapy.Field()  # 12、商品分类ID
    dsr_description = scrapy.Field()  # 宝贝描述
    dsr_service = scrapy.Field()  # 卖家服务
    dsr_delivery = scrapy.Field()  # # 物流
    search_args = scrapy.Field()  # 搜索参数
    now_page_total = scrapy.Field() # 本页总宝贝数量

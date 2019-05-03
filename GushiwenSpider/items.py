# _*_ coding:utf-8 _*_

import scrapy


class GushiwenItem(scrapy.Item):
    """
    主程序只需要提取出作品链接即可,每页最多十个
    送入redis队列view:start_urls
    """
    view_urls = scrapy.Field()


class ViewItem(scrapy.Item):
    """
    提取作品名称、朝代、作者名、正文、部分注释及翻译
    """
    poetry_name = scrapy.Field()
    poetry_link = scrapy.Field()
    poetry_dynasty = scrapy.Field()
    author_name = scrapy.Field()
    poetry_fanyi_list = scrapy.Field()
    # 正文
    poetry_mainbody_meta_content = scrapy.Field()
    # 翻译 注释
    trans = scrapy.Field()
    notation = scrapy.Field()
    fanyi_id = scrapy.Field()


class FanyiItem(scrapy.Item):
    """
    通过翻译链接
    https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id=1
    提取译文及注释内容
    """
    fanyi = scrapy.Field()
    zhushi = scrapy.Field()
    fanyi_url = scrapy.Field()

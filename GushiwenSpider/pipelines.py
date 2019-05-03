# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from w3lib.html import remove_tags
import pymysql
import redis
import re
import logging

"""
定义公用变量
"""
rooturl = 'https://so.gushiwen.org'
# 数据库表结构见 数据库表结构.xlsx
conn = pymysql.connect(
    host='47.95.199.35',
    port=3306,
    user='tyj',
    passwd='tyj',
    db='gushiwen',
    charset='utf8',
)
cur = conn.cursor()
logging.info("-------------连接 mysql------------")
# redis
rds = redis.Redis(host='localhost', port=6379, db=0)


# 文本处理方法
def extract_poetry_mainbody(text):
    """
    调用w3lib.html.remove_tags()处理正文
    部分作品的文本内容放在了p标签外面，div.son2内，通过<br>分隔
    <br>标签不是完整标签，在remove_tags()函数中会被去掉，无法通过keep保留
    先remove其他标签（div，a，span，p...） 再用'\n'替换<br>
    """
    mainbody_text = remove_tags(text=text, which_ones=('div', 'a', 'span', 'p'))
    mainbody_text = mainbody_text.replace(' +', '').replace('\n', '', 16).replace('<br>', '\n')
    # mainbody_text = remove_needless_sysmbols(mainbody_text)
    return mainbody_text


# 翻译注释提取方法
def extract_fanyi_text(text):
    text = text.replace('<strong>译文</strong>', '').replace('<strong>注释</strong>', '')  # 去除<strong>译文 </strong>
    return remove_needless_sysmbols(remove_tags(text.replace('<br>', '\n')).replace(' +', ''))


def remove_needless_sysmbols(text):
    # 删除多余的符号
    text = text.replace('\r\n', '\r')
    for sysmbol in ['\r', '\n']:
        double_sysmbols = sysmbol * 2
        while double_sysmbols in text:
            text = text.replace(double_sysmbols, sysmbol)
        return text


def lpush_fanyi_url_by_id(id):
    url = rooturl + '/shiwen2017/ajaxfanyi.aspx?id=' + id
    rds.lpush('fanyi:start_urls', url)
    return url


class GushiwenPipeline(object):
    """
    提取作品链接 https://so.gushiwen.org/shiwenv_4c5705b99143.aspx
    存入redis队列
    """

    def process_item(self, item, spider):
        if item['view_urls']:
            # print item['view_urls']
            # 列表不为空
            for it in item['view_urls']:
                # url = 'https://so.gushiwen.org' + it
                # rds.lpush('view:start_urls', url)
                rds.lpush('view:start_urls', it)


class ParseViewPipeline(object):
    view_list = []
    main_list = []
    fanyi_list = []

    def process_item(self, item, spider):
        """
        提取: https://so.gushiwen.org/shiwenv_d3e3283daac5.aspx
        1、作品名
        2、朝代
        3、作者
        4、正文部分，送入数据库
        5、先提取当前view中的翻译赏析，送入数据库。有翻译、赏析链接,送入redis队列,fanyi:start_urls,后续更新翻译赏析
        """

        # 部分的作品名中含有‘/’，如 梅花/梅 在建立文件时会报错，替换为空格
        poetry_name = item['poetry_name'][0].replace('/', ' ')
        poetry_link = item['poetry_link'][0]
        view_pa = 'https://so.gushiwen.org/(.*?).aspx.*'
        view_num = re.match(view_pa, poetry_link).groups()[0]  # shiwenv_d3e3283daac5
        poetry_dynasty = item['poetry_dynasty'][0]

        # 提取正文，写入数据库
        poetry_mainbody = extract_poetry_mainbody("".join(item['poetry_mainbody_meta_content']))  # list
        self.main_list.append((view_num, poetry_mainbody))
        if len(self.main_list) >= 10:
            sqli = 'insert into main_content values(%s,%s)'
            self.insert_data(sqli, self.main_list)
            self.main_list.clear()

        # 提取翻译链接并送入redis
        if 'fanyi_id' in item:  # 存在翻译链接
            fanyi_id = item['fanyi_id'][0][5:]  # fanyi1 https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id=1
            fanyi_link = lpush_fanyi_url_by_id(fanyi_id)
        else:  # 无翻译链接     https://so.gushiwen.org/shiwenv_9936770100ef.aspx(较短)
            fanyi_id = view_num
            fanyi_link = ''

        # 提取译文及鉴赏,写入数据库
        if 'trans' in item:  # 有译文
            trans = extract_fanyi_text(''.join(item['trans'][0]))
            notation = extract_fanyi_text(''.join(item['notation'][0]))
            # 插入翻译数据
            self.fanyi_list.append((fanyi_id, fanyi_link, trans, notation))
        elif 'trans' not in item and 'notation' in item:  # 译文太长
            logging.debug("=======》无 trans item")
            trans = extract_fanyi_text(''.join(item['notation'][0]))
            notation = ''
            self.fanyi_list.append((fanyi_id, fanyi_link, trans, notation))
        else:  # 无译文及注释
            fanyi_id = ''
            logging.debug("=======》无 trans item 及 notation")
        # logging.debug("============>" + sqli)
        logging.debug("====> fanyi_id: " + fanyi_id)
        # 插入翻译数据
        sql = 'insert into fanyi(fanyi_id, fanyi_link, fanyi, zhushi) values(%s,%s,%s, %s)'
        if len(self.fanyi_list) >= 10:
            self.insert_data(sql, self.fanyi_list)
            self.fanyi_list.clear()

        # 提取view_num, view_link, dynasty, view_name. maint_content等内容写入数据
        author_name = item['author_name'][0]
        view_sql = 'insert into view ' \
                   '(view_num,view_link,dynasty,view_name,author_name,main_content, fanyi_id)' \
                   'values (%s,%s,%s,%s,%s,%s, %s)'
        values = (view_num, poetry_link, poetry_dynasty,
                  poetry_name, author_name, view_num, fanyi_id)
        self.view_list.append(values)
        if len(self.view_list) >= 10:
            self.insert_data(view_sql, self.view_list)
            self.view_list.clear()

    # 批量插入数据
    def insert_data(self, sql, data):
        try:
            num = cur.executemany(sql, data)
            logging.debug("===> insert {} {}".format(num, sql))
            conn.commit()
        except Exception as e:
            logging.error("====> " + str(e))
            conn.rollback()
        return


class ParseFanyiPipeline(object):
    """
    处理译文及注释部分，存入数据库
    # https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id=1607
    """
    fan_yi_list = []

    def process_item(self, item, spider):
        fanyi_url = item['fanyi_url'][0]
        fanyi_id = fanyi_url[fanyi_url.index('=') + 1:]

        if 'zhushi' not in item:  # 有些翻译链接无效，打不开
            logging.debug("===> visit url error: " + fanyi_url)
            return
        if 'fanyi' not in item:  # 可能只有译文，把注释提取到的内容作为译文
            fanyi = item['zhushi'][0]
            zhushi = ''
            logging.debug("===> no zhushi: " + fanyi_id)
        else:
            fanyi = ''.join(item['fanyi'])
            zhushi = item['zhushi'][0]

        # 内容清洗提取
        extract_content_text = extract_fanyi_text(fanyi)
        extract_zhushi = extract_fanyi_text(zhushi)

        values = (extract_content_text, extract_zhushi, fanyi_id)
        sql = 'update fanyi set fanyi = %s, zhushi = %s where fanyi_id = %s'
        self.fan_yi_list.append(values)
        if len(self.fan_yi_list) == 1:
            self.update_many(sql, self.fan_yi_list)
            self.fan_yi_list.clear()

    # 批量插入数据
    def update_many(self, sql, data):
        try:
            num = cur.executemany(sql, data)
            logging.debug("======> update success: " + num)
            conn.commit()
        except Exception as e:
            logging.error("======> update error" + str(e))
            conn.rollback()

# _*_ coding:utf8 _*_

from scrapy_redis.spiders import RedisSpider
from GushiwenSpider.items import FanyiItem
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class FanyiSpider(RedisSpider):
    """
    从redis队列 fanyi:start_urls
    获取链接：
        https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id=57808
    提取翻译和注释正文部分，存入数据库
    """
    name = 'fan_yi_spider'
    redis_key = 'fanyi:start_urls'
    redis_batch_size = 1
    custom_settings = {
        'ITEM_PIPELINES': {
            'GushiwenSpider.pipelines.ParseFanyiPipeline': 300,
        },
    }

    def parse(self, response):
        ld = ItemLoader(item=FanyiItem(), response=response)
        ld.add_xpath('fanyi', '//div[@class="contyishang"]/p[position()<last()]')
        ld.add_xpath('zhushi', '//div[@class="contyishang"]/p[last()]')
        ld.add_value('fanyi_url', response.url)
        return ld.load_item()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(FanyiSpider)
    process.start()

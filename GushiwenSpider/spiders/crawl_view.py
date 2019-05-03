# _*_ coding:utf8 _*_

from scrapy_redis.spiders import RedisSpider
from scrapy.loader import ItemLoader
from GushiwenSpider.items import ViewItem
from scrapy.crawler import CrawlerProcess


class ViewSdier(RedisSpider):
    """
    提取View页面主要内容：
    作品名称、作者、朝代、作品正文、翻译链接(fanyi_123.aspx, shangxi_123.aspx)
    链接部分提交到redis，供爬虫fanyi_spider爬取
    https://so.gushiwen.org/shiwenv_4c5705b99143.aspx
    """
    name = 'view_spider'
    redis_key = 'view:start_urls'
    redis_batch_size = 1
    custom_settings = {
        'ITEM_PIPELINES': {
            'GushiwenSpider.pipelines.ParseViewPipeline': 300,
        },
    }

    def parse(self, response):
        view_item = ItemLoader(item=ViewItem(), response=response)
        view_item.add_xpath('poetry_name', '//div[@class="left"]/div[@class="sons"][1]/div[@class="cont"]/h1/text()')
        view_item.add_value('poetry_link', response.url)
        view_item.add_xpath('poetry_dynasty',
                            '//div[@class="left"]/div[@class="sons"][1]/div[@class="cont"]/p[1]/a[1]/text()')
        view_item.add_xpath('author_name',
                            '//div[@class="left"]/div[@class="sons"][1]/div[@class="cont"]/p[1]/a[2]/text()')
        view_item.add_xpath('poetry_mainbody_meta_content',
                            '//div[@class="left"]/div[@class="sons"][1]/div[@class="cont"]/div[@class="contson"]')
        view_item.add_xpath('trans',
                            '//div[@class="left"]/div[@class="sons"][2]/div[@class="contyishang"]/p[position() < last()]')
        view_item.add_xpath('notation',
                            '//div[@class="left"]/div[@class="sons"][2]/div[@class="contyishang"]/p[last()]')
        view_item.add_xpath('fanyi_id', '//div[@class="left"]/div[@class="sons"][2]/@id')
        return view_item.load_item()


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ViewSdier)
    process.start()

"""
调用scrapy 命令行执行爬虫
crawl url -> crawl view -> crawl fan_yi
"""
from scrapy import cmdline


def craw_url():
    """
    提取网页链接
    :return:
    """
    print("Crawling url...")
    cmdline.execute("scrapy crawl url_spider".split())


def crawl_view():
    """
    爬取网页标题、正文，提取附件链接
    :return:
    """
    print("Crawling view...")
    cmdline.execute("scrapy crawl view_spider".split())


def crawl_fan_yi():
    """
    爬取译文及注释
    :return:
    """
    print("Crawling file...")
    cmdline.execute("scrapy crawl fan_yi_spider".split())


if __name__ == '__main__':
    craw_url()
    # crawl_view()
    # crawl_fan_yi()

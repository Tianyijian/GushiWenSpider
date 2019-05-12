
# 古诗文爬虫


为了构建古诗文语料库，本项目尝试爬取了[古诗文网](https://www.gushiwen.org/)，使用 [scrapy](https://scrapy.org/) 爬虫框架并结合 [scrapy_redis](https://github.com/rolando/scrapy-redis) 部署分布式爬虫，最后将数据存储到了MySQL数据库。

爬取的主要内容：

	作品：名称、朝代、作者、原文
	参考翻译：译文及注释

环境
	
	Scrapy==1.6.0
	scrapy_redis==0.6.8
	redis==3.2.1
	PyMySQL==0.9.3
	w3lib==1.20.0

## 爬虫

   一共三只爬虫，采用分布式部署：
    
	 爬虫执行顺序：
        url_spider --> view_spider --> fan_yi_spider
   

[crawl_url](https://github.com/Tianyijian/GushiWenSpider/blob/master/GushiwenSpider/spiders/crawl_url.py)
     
	本程序为起始程序，提取作品链接 https://so.gushiwen.org/shiwenv_4c5705b99143.aspx
    存入redis队列 view:start_urls
     
[crawl_view](https://github.com/Tianyijian/GushiWenSpider/blob/master/GushiwenSpider/spiders/crawl_view.py)
     
    提取页面主要内容：
    作品名称、作者、朝代、作品正文、翻译链接(fanyi_123.aspx, shangxi_123.aspx)
    链接部分提交到redis，供爬虫fanyi_spider爬取
       
[crawl\\_fan_yi](https://github.com/Tianyijian/GushiWenSpider/blob/master/GushiwenSpider/spiders/crawl_fan_yi.py)

    从redis队列 fanyi:start_urls
    获取链接：
        https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id=57808
    提取翻译和注释正文部分，存入数据库

## 说明

- 本项目参考了[GushiwenSpider](https://github.com/PChief/GushiwenSpider)，仅做为爬虫练手项目。由于古诗文网的改版，本项目更改了其中的xpath定位，适用于2019年的古诗文网。
- 完整的数据可以参考[古诗词数据库](https://github.com/Tianyijian/poetry)。
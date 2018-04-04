# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import random
# from zhihuuser.settings import PROXY_POOL_URL
import time
import base64
from zhihuuser.settings import DEFAULT_REQUEST_HEADERS
from fake_useragent import UserAgent
ua = UserAgent()

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

    # 代理隧道验证信息
proxyUser = ""
proxyPass = ""
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class RandomUserAgent(object):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers.setdefault("User-Agent", ua.random)
        print(request.headers['User-Agent'])


class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.


    # def get_proxy(self):
    #     try:
    #         # response = requests.get(PROXY_POOL_URL)
    #         if response.status_code == 200:
    #             return response.text
    #         return None
    #     except ConnectionError:
    #         return None

    def process_request(self, request, spider):    #20180403修改，新增代理
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth
        print("this is response ip:" + proxyServer)

        #thisip = self.get_proxy()
        # print("this is ip:" + thisip)
        # proxy = self.get_random_proxy()
        # print("this is request ip:" + proxy)
        # request.meta["proxy"] = proxy

    # def process_response(self, request, response, spider):  #20180403修改，新增代理
    #     '''对返回的response处理'''
    #     # 如果返回的response状态不是200，重新生成当前request对象
    #     if response.status != 200:
    #         # if response.status == 301:                  #排除无法爬取org用户（301页面）的问题
    #         #     return response
    #         # proxy = self.get_random_proxy()
    #         # print("this is response ip:" + proxy)
    #         # 对当前request加上代理
    #         request.meta['proxy'] = "http://"+proxy
    #         return request
    #     return response

    # def get_random_proxy(self):   #20180403修改，新增代理
    #     '''随机从文件中读取proxy'''
    #     while 1:
    #         with open('E:\ProxyPool\\proxies.txt', 'r') as f: #需要修改文件路径
    #             proxies = f.readlines()
    #         if proxies:
    #             break
    #         else:
    #             time.sleep(1)
    #     proxy = random.choice(proxies).strip()
    #     return proxy

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).

        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

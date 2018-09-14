# -*- coding: utf-8 -*-
import json
import re

import scrapy

from WeiBoLuHan.items import WeiboluhanItem
def subHtml(value):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', value)
    return dd

class LuhanSpider(scrapy.Spider):
    name = 'luHan'
    allowed_domains = ['m.weibo.cn']
    # start_urls = ['https://m.weibo.cn/comments/hotflow?id=4262111301211421&mid=4262111301211421&max_id_type=0']

    headers = {
        "HOST": "m.weibo.cn",
        "Referer": "https://m.weibo.cn/status/4262111301211421",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }
    url_comment = "https://m.weibo.cn/comments/hotflow?id=4262111301211421&mid=4262111301211421&max_id={0}&max_id_type={1}"
    start_urls = ["https://m.weibo.cn/comments/hotflow?id=4262111301211421&mid=4262111301211421&max_id=190918095587076&max_id_type=0"]
    def parse(self, response):

        yield scrapy.Request(response.url, headers=self.headers, callback=self.parse_comment)


    def parse_comment(self, response):
        comment_json = json.loads(response.text)
        ok = comment_json['ok']
        if(ok==0):
            # 如果是0的话，修改max_id_type可能会访问到
            reg = re.compile(r'.*(max_id_type=(\d)).*')
            match = reg.match(response.url)
            max_id_type_cur = match.group(2)#当前的值
            max_id_type = abs(int(max_id_type_cur)-1)#如果为1，修改为0，如果为0则修改为1
            url = str(response.url).replace("max_id_type=" + str(max_id_type_cur),"max_id_type=" + str(max_id_type))
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_comment)

        if(ok==1):
            max_id_type = comment_json['data']['max_id_type']
            max_id = comment_json['data']['max_id']
            commen_list = comment_json["data"]["data"]
            for cl in commen_list:
                weiComent_item = WeiboluhanItem()
                # weiComent_item = (item=WeiboluhanItem(), response=response)
                weiComent_item['comment'] = subHtml(cl["text"])
                yield weiComent_item
            if max_id!=0:
                #说明还没有加载完评论
                url_comment = self.url_comment.format(max_id,max_id_type)#下一个加载的评论页面
                yield scrapy.Request(url_comment, headers=self.headers, callback=self.parse_comment)


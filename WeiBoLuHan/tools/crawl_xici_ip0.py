# -*- coding: utf-8 -*-

import requests
import pprint
from scrapy.selector import Selector


def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
    with open('123.csv','w') as f:
        for i in range(1, 10):
            print(i)
            re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            print(re.url,re.status_code)#,re.text)
            selector = Selector(text=re.text)
            all_trs = selector.css("#ip_list tr")
            ip_list = []
            for tr in all_trs[1:]:
                speed_str = tr.css(".bar::attr(title)").extract()[0]
                if speed_str:
                    speed = float(speed_str.split("秒")[0])
                all_texts = tr.css("td::text").extract()

                ip = all_texts[0]
                port = all_texts[1]
                proxy_type = all_texts[5]
                f.write(ip +','+ port +','+ proxy_type + '\n')


class GetIP(object):
    # def delete_ip(self, ip):
    #     #从数据库中删除无效的ip
    #     delete_sql = """
    #         delete from proxy_ip where ip='{0}'
    #     """.format(ip)
    #     cursor.execute(delete_sql)
    #     conn.commit()
    #     return True

    def judge_ip(self, ip, port, proxy_type):
        #判断ip是否可用
        http_url = "https://m.weibo.cn/comments/hotflow?id=4262111301211421&mid=4262111301211421&max_id_type=0"
        proxy_url = "{0}://{1}:{2}".format(proxy_type, ip, port)
        try:
            proxy_dict = {
                proxy_type:proxy_url,
            }
            headers = {
                'Connection': 'close',
            }
            response = requests.get(http_url, proxies=proxy_dict,headers=headers)

        except Exception as e:
            print(e)
            print ("invalid ip and port")
            # self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print  ("invalid ip and port")
                # self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        #crawl_ips()

        with open('I:/code/scrapyPrac/WeiBoLuHan/WeiBoLuHan/tools/123.csv','r') as f:
            ip_info = f.readline()[:-1].split(',')
            print("ip*********")
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[2]
            judge_re = self.judge_ip(ip, port, proxy_type)
            # judge_re = self.judge_ip("125.120.9.154", "6666", "https")
            if judge_re:
                print("{0}://{1}:{2}".format(proxy_type.lower(), ip, port))
                return "{0}://{1}:{2}".format(proxy_type.lower(), ip, port)
            else:
                return self.get_random_ip()
        #     print("http://{0}:{1}".format(tmp[0], tmp[1]))
        # return "http://{0}:{1}".format(tmp[0], tmp[1])
        # random_sql = """
        #       SELECT ip, port, proxy_type FROM proxy_ip
        #     ORDER BY RAND()
        #     LIMIT 1
        #     """#从数据库中随机取数据
        # result = cursor.execute(random_sql)
        # for ip_info in cursor.fetchall():
        #     ip = ip_info[0]
        #     port = ip_info[1]
        #     proxy_type = ip_info[2]
        #     judge_re = self.judge_ip(ip, port,proxy_type)
        #     if judge_re:
        #         return "http://{0}:{1}".format(ip, port)
        #     else:
        #         return self.get_random_ip()


if __name__ == "__main__":
    # crawl_ips()
    get_ip = GetIP()
    print(get_ip.get_random_ip())

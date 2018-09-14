
from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))#获取当前的父目录
print(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","luHan"])#在cmd中输入改命令 + name
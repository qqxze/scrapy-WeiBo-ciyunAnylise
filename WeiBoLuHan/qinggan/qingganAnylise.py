import codecs
import re
import numpy as np
import pymysql
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp.sentiment import Sentiment

comment = []
with open('I:/code/scrapyPrac/WeiBoLuHan/comment1.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        if row not in comment:
            comment.append(row.strip('\n'))
def snowanalysis(self):
    sentimentslist = []
    for li in self:
        #text = re.sub(r'(?:回复)?(?://)?@[\w\u2E80-\u9FFF]+:?|\[\w+\]', ',',li)
        print(li)
        s = SnowNLP(li)
        print(s.sentiments)
        sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01))
    plt.show()
snowanalysis(comment)
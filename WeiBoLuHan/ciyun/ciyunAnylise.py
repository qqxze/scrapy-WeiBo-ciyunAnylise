import os
from os import path
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def wordCount(segment_list):
    '''
        该函数实现词频的统计，并将统计结果存储至本地。
        在制作词云的过程中用不到，主要是在画词频统计图时用到。
    '''
    word_lst = []
    word_dict = {}
    with open('count.txt','w', encoding='UTF-8') as wf2:
        word_lst.append(segment_list.split(' '))
        for item in word_lst:
            for item2 in item:
                if item2 not in word_dict:
                    word_dict[item2] = 1
                else:
                    word_dict[item2] += 1

        word_dict_sorted = dict(sorted(word_dict.items(), \
        key = lambda item:item[1], reverse=True))#按照词频从大到小排序
        for key in word_dict_sorted:
            wf2.write(key+' '+str(word_dict_sorted[key])+'\n')
    wf2.close()


def make_worldcloud(file_path):
    text_from_file_with_apath = open(file_path,'r',encoding='UTF-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=False)
    wl_space_split = " ".join(wordlist_after_jieba)
    wordCount(wl_space_split)
    wordText = open(file_path, 'r', encoding='UTF-8').read()
    # print(wl_space_split)
    backgroud_Image = plt.imread('l.jpg')
    print('加载图片成功！')
    '''设置词云样式'''
    stopwords = STOPWORDS.copy()
    stopwords.add("哈哈")
    stopwords.add("啊啊啊")
    # stopwords.add("鹿晗")#可以加多个屏蔽词
    FONT_PATH = "STXINGKA.TTF"
    wc = WordCloud(
        width=1024,
        height=768,
        background_color='white',# 设置背景颜色
        mask=backgroud_Image,# 设置背景图片
        font_path=FONT_PATH,  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=600, # 设置最大现实的字数
        stopwords=stopwords,# 设置停用词
        max_font_size=400,# 设置字体最大值
        random_state=50,# 设置有多少种随机生成状态，即有多少种配色方案
    )
    # wc.generate_from_text(wl_space_split)#开始加载文本
    # wc.generate_from_frequencies(wordText)
    wc.generate(wl_space_split)
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)#字体颜色为背景图片的颜色
    plt.imshow(wc, interpolation="bilinear")# 显示词云图
    plt.axis('off')# 是否显示x轴、y轴下标
    plt.show()#显示
    # 获得模块所在的路径的
    d = path.dirname(__file__)
    # os.path.join()：  将多个路径组合后返回
    wc.to_file(path.join(d, "h12.jpg"))
    print('生成词云成功!')

if __name__ == '__main__':

    make_worldcloud('I:/code/scrapyPrac/WeiBoLuHan/comment1.txt')

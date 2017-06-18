# -*- coding: utf-8 -*-
import codecs
import urllib2
# 解析文件，下载图片
# 输入：每行为一个图片的url，将图片下载到本地


def download_pic(file_path,out_path):
    count = 0
    with codecs.open(file_path, 'r', encoding="utf-8") as file_db:
        for temp in file_db:
            count += 1
            out_path = temp.split('/')[-1].strip()
            with open(out_path, "wb") as file_out:
                pic_data = urllib2.urlopen(temp).read()
                file_out.write(pic_data)
                print count

if __name__ == "__main__":
    pic_list = {}
    file_path = "new100.csv"
    out_path = "pic100"
    download_pic(file_path, out_path)
    print "over"

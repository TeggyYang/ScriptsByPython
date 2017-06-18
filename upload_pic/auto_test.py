# coding=utf-8

import glob
import os
import json
import time
import operator

import requests


if __name__ == "__main__":
    start_time = time.time()
    pic_path = "/Volumes/Transcend/auto_test200"
    server = 'http://101.200.204.30:8080/'  # wangxiao
    right = 0
    total = 0
    wrong_ids = []
    no_json_ids = []
    total_dict = {}
    img_path = '{}/'.format(pic_path)
    imgs = [img for img in glob.glob(img_path + "*")]
    for img in imgs[:50]:
        if os.path.isdir(img):
            continue
        q_id = os.path.splitext(os.path.basename(img))[0]
        time.sleep(1)
        with open(img, 'rb') as f:
            r = requests.post(server, files={'picture': f}, data={'pic_source': 'auto_test200'})
        try:
            result = json.loads(r.text)
            for r in result['timer']:
                if r['name'] in total_dict:
                    total_dict[r['name']] += float(r['range'])
                else:
                    total_dict[r['name']] = float(r['range'])
            if "?" not in result['url']:
                result_id = result['url'].split("/")[-3]
            else:
                result_id = result['url'].split("=")[-1]
            if str(q_id) == str(result_id):
                right += 1
            else:
                wrong_ids.append(q_id)
            total += 1
        except Exception, e:
            no_json_ids.append(q_id)
            print e
            print img
        print (total, right),
    total_time = (time.time() - start_time)
    if total == 0:
        print "total is zero, exit"
        exit()
    print "\r"
    print u"服务地址：{}".format(server)
    print u"正确率:{}".format(float(right) / total)
    print u"测试题目数量：{}".format(total)
    print u"测试总耗时:{}".format(total_time)
    print u"平均每个题目耗时：{}".format(total_time / total)
    sorted_x = sorted(total_dict.items(), key=operator.itemgetter(1), reverse=True)
    print u"各个阶段耗时平均值："
    for a in sorted_x:
        print a[0], a[1] / total
    print u"未正确识别图片id:{}".format(wrong_ids)
    print u"无结果图片id:{}".format(no_json_ids)

# coding=utf-8
from aip import AipOcr
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import hashlib
import base64




ACCESS_TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
SECRET_KEY = 'mqaj3c9YrsGEnl1OjM4eEucdcBjMXnpZ'
API_KEY = 'Y04QyPI8rvpR4Wy6TcszHH22'
APP_ID = '9500821'


def get_img(img_file):
    """
    获取图片文件
    :param img_file:
    :return: 返回file对象
    :rtype: file object
    """
    # with open(img_file, 'rb') as fp:
    #     return fp.read()

    fp = open(img_file, 'rb')
    # output = open('./tmp', 'wb')
    # base64.encode(fp, output)

    return fp.read()


def get_text_content(img_locate):
    """
    返回文字内容
    :param img_locate:
    :return:
    """
    aip_ocr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # print aip_ocr
    result = aip_ocr.basicGeneral(get_img(img_locate))
    # result = aip_ocr.general(img_locate)
    txt = ''
    # print 1
    # print unicode(result)
    for each in result['words_result']:
        txt += each['words'] + '\n'
    return txt.encode('utf-8')
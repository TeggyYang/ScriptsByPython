# -*- coding: utf-8 -*-
"""字符串去除标签"""

import re
import codecs
from bs4 import BeautifulSoup

# 常见标签列表
HTML_TAG_LIST = ['<body>|', '<br>|', '<dd>|', '<dir>|', '<div>|', '<dl>|', '<dt>|', '<em>|', '<figure>|', '<font>|',
                 '<form>|', '<h[1-10]>|', '<hr>|', '<head>|', '<header>|', '<hr>|', '<html>|', '<i>|', '<img>|', '<input>|',
                 '<label>|', '<li>|', '<main>|', '<map>|', '<output>|', '<p>|', '<param>|', '<pre>|', '<progress>|', '<s>|',
                 '<style>|', '<sub>|', '<table>|', '<tbody>|', '<td>|', '<thead>|', '<title>|', '<tr>|', '<tt>|', '<u>|',
                 '<var>|', '<strong>|', '<span>|', '<sup>|', '<ul>|'
                 ]

for i in range(len(HTML_TAG_LIST)):
    tag_close = '<' + '/' + HTML_TAG_LIST[i][1:]
    HTML_TAG_LIST.append(tag_close)
HTML_TAG_LIST.insert(0, '<[a-z\s]*=[^<>]*?>|')
HTML_TAG_LIST.insert(1, '&#13;|&nbsp;|')


PATTERN_HTML = re.compile(r'<[^<>]*>')
PATTERN_FILTER = re.compile(r'<[^<]*/>')
PATTERN_MY_TAG = re.compile(r'<my_tag>|</my_tag>')
PATTERN_TAG = re.compile(r'<[a-z][^>]*>')
PATTERN_BACK_TAG = re.compile(r'</[^>]+>')
PATTERN_INTERVAL_TAG = re.compile(r'<[a-z][^<>,_+()]+>')
PATTERN_NO_TAG = re.compile(''.join(HTML_TAG_LIST)[:-1])


class DataIn(object):
    """声明一个存放待返回数据的类"""
    location = 0
    set_list = []
    set_back = []

    def __init__(self, line):
        self.line = line

    def handle(self):
        """示例"""
        pass

    def get_data(self):
        """示例"""
        pass


def pre_handle(line):
    """预处理数据"""
    # 添加一个my_tag标签防止传入字符串如：hello! a<b，小于号以及后面的字符<b会被bs解析抹除。
    line += '<my_tag>'
    # 利用bs把字符串解析成html5lib格式
    soup = BeautifulSoup(line, 'html5lib')
    html = soup.prettify()

    html_list = []
    for i in html.split('\n'):
        i = i.lstrip()
        # 解析的网页每一行不是自己添加的my_tag标签就存入html_list作为后续判断
        if PATTERN_MY_TAG.match(i) is None:
            # my_tag标签会被bs解析成<my_tag="">隐藏在疑似标签中和<my_tag>隐藏在内容中。
            html_list.append(i.replace('<my_tag="">', '').replace('\r', '').replace('<my_tag>', ''))
        else:
            pass
    return line, html_list


def data_tag(i, data, d_in):
    """在源字符串中找到疑似html标签的信息"""
    # 下面这个正则表达式匹配标签中的标签如：<html <tag>
    tag_in_tag = PATTERN_INTERVAL_TAG.search(i[1:].replace('=""', ''))
    if tag_in_tag is not None:
        # 获取标签
        tag = tag_in_tag.group()
        # 找到内容在字符串中对应的位置
        front = d_in.line.find(i.split(' ')[0], d_in.location)
        back = d_in.line.find('>', front)
        if front > 0:
            d_in.location = back
            data.append(d_in.line[front: (back + 1)].replace(tag, ''))
        else:
            pass
    else:
        front = d_in.line.find(i.split(' ')[0][:8], d_in.location)
        back = d_in.line.find('>', front)
        if front > 0:
            d_in.location = back
            data.append(d_in.line[front: (back + 1)])
        else:
            pass


def like_tag(i, data, d_in):
    """疑似标签判断是否重复，对标签的特征进行判断"""
    if i not in d_in.set_list:
        # 部分内容如：a<b,c>d中的<b,c>可能在解析网页的时候解析成两个
        d_in.set_list.append(i)
        # i的关闭标签
        i_back = i[0] + '/' + i[1:]
        # 记录每一个标签的关闭标签，最后把所有关闭标签去掉，防止关闭标签被解析成网页内容
        d_in.set_back.append(i_back)
        # 关闭标签在字符串中没有，判定为a<b,c>d中的<b,c>被解析为标签
        if d_in.line.find(i_back[:10]) == -1:
            data_tag(i, data, d_in)
        else:
            pass
    else:
        pass


def bs_parse_tag(line):
    line, html_list = pre_handle(line)
    data = []
    d_in = DataIn(line)

    for i in html_list:
        i = i.encode('utf8')
        # 下面这个正则表达式是标签匹配如：<html>等
        flag_tag = PATTERN_TAG.match(i)
        # 下面这个正则表达式是关闭标签的匹配如：</html>
        flag_back_tag = PATTERN_BACK_TAG.match(i)
        if flag_tag is None and flag_back_tag is None:
            # 不是标签和关闭标签，就是实际内容，把实际内容放入data数组
            data.append(i)
        elif flag_tag is not None:
            # 被bs解析为标签形式的，可能是标签，也可能是诸如：a<b,c>d中的<b,c>
            like_tag(i, data, d_in)
        else:
            pass
    # 下面这个正则表达式是最后滤除没有关闭标签的标签，如：<tablestyle="20">, 以及滤除html中的格式"&#13;"包含的内容
    # 链接所有字符串，bs把">"解析成"&gt;"， 把"<"解析成"&lt;"，需要替换回来
    problem = ''.join(data).replace('&gt;', '>').replace('&lt;', '<')
    # 把部分关闭标签被错误解析为内容的部分删除
    for j in d_in.set_back:
        question = problem.replace(j, '')
    return question


def remove_tags(line):
    """移除字符串中的标签"""
    # 下面这个正则表达式是首先检测字符串中是否包含html格式，如：<任意内容>
    if PATTERN_HTML.search(line) is None:
        return line, False
    else:
        line = PATTERN_FILTER.sub('', line)
        line = PATTERN_NO_TAG.sub('', line)
        return line, True
        # 下面这个捕获异常是捕获字符串过长造成RuntimeError问题
        try:
            line = PATTERN_FILTER.sub('', line)
            line = PATTERN_NO_TAG.sub('', line)
            if PATTERN_HTML.search(line) is None:
                return line, True
            else:
                question = bs_parse_tag(line)
                return question, True
        except RuntimeError:
            print line
            print '文本过长，超出BeautifulSoup解析范围。'
            return line, False


def handle_text(file_name):
    """打开文件，读取并处理字符串"""
    with codecs.open(file_name, 'r', encoding="utf-8") as file_db:
        all_sum = 0
        for temp in file_db:
            temp = temp.encode('utf8')
            for itr in range(1):
                all_sum += 1
                print all_sum
                line, flag = remove_tags(temp)
                print temp
                print line, flag


if __name__ == '__main__':
    demo = '1<2,3>2<title="a">这是</a>一个<br>测</hr>试<html> <p> end !'
    returned_str, processed = remove_tags(demo)
    if processed:
        print returned_str
    else:
        print "not processed"
    handle_text(r'D:\data\text_with_html.txt')
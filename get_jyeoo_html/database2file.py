# -*- coding: UTF-8 -*-
import MySQLdb
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def data2file():
    # with codecs.open(output_file_path, "w", encoding="utf-8") as fout:
    try:
        print "aa"
        conn1 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', db='iax_sql', port=3306)
        cur1 = conn1.cursor()
        # cur.execute('select * from iax_data')
        cur1.execute('select * from iax_data')
        temp = cur1.fetchall()
        count = 0
        for row in temp:
            count += 1
            jid = row[0]
            jdata = row[1]
            jresult = json.loads(jdata)["result"]
            soup = BeautifulSoup(jresult, "html.parser")
            jtext = unicode(soup.find_all('div', class_='item-body')[0]).replace("\n", "")\
                .replace(" ", "").replace("\r", "")
            # print jtext
            janswer = unicode(soup.find_all('div', class_='item-help')[0]).replace("\n", "")\
                .replace(" ", "").replace("\r", "")
            # print janswer
            janalysis = unicode(soup.find_all('div', class_='item-help')[1]).replace("\n", "")\
                .replace(" ", "").replace("\r", "")
            # print janalysis
            jcomment = unicode(soup.find_all('div', class_='item-help')[2]).replace("\n", "")\
                .replace(" ", "").replace("\r", "")
            # print jcomment
            jkeypoint = unicode(soup.find_all('div', class_='item-help')[3]).replace("\n", "")\
                .replace(" ", "").replace("\r", "")
            # print jkeypoint
            conn2 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', db='jyeoo_all_courses'
                                    , port=3306)
            cur2 = conn2.cursor()
            cur2.execute(("insert into question_detail_0 (q_id,q_text,q_answer,q_analysis,q_comment,q_pt) "
                          "values ('{}','{}','{}','{}','{}','{}')").format(jid, jtext.replace("'", "&apos;"),
                                                                           janswer.replace("'", "&apos;"),
                                                                           janalysis.replace("'", "&apos;"),
                                                                           jcomment.replace("'", "&apos;"),
                                                                           jkeypoint.replace("'", "&apos;")))

            conn2.commit()
            # print count

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur1.close()
        conn1.close()
        cur2.close()
        conn2.close()


if __name__ == "__main__":
    output_file_path = "D:/get_jyeoo_html/database2file.txt"
    data2file()
    print "over"

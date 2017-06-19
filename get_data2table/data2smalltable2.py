# coding=utf-8
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

MYSQL_TABLE = "question_detail"
SPLIT_NUM = 100
NAME_PREFIX = "question_detail_"
# 每次数据库读的次数
SELECT_NUM = 1000
# 总表数据量
SUM_COUNT = 25461659


def get_count(db):  # 统计分表数
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', # db='all_courses_latex',
                               port=3306)
        cur = conn.cursor()
        count = 0
        for i in range(0, 100):
            cur.execute('select count(*) from {}.question_detail_{} '.format(db, i))
            temp = cur.fetchone()[0]
            count += int(temp)
            # print str(i) + " " + str(temp)
        print count
        cur.close()
        conn.close()
        return count
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def ord_hash(x): # 获取分表id
    s = 0
    for c in x:
        s += ord(c)
    return s % SPLIT_NUM


def data2table(scount, plus):  # 分库到分表
    try:
        conn1 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', db='jyeoo_all_courses',
                                port=3306)
        # db1 = 'jyeoo_all_courses'
        cur1 = conn1.cursor()
        # print "aa"
        conn2 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', db='all_courses_latex',
                                port=3306)
        # db2 = 'all_courses_latex'
        cur2 = conn2.cursor()
        # print "bb"
        cur1.execute('select * from question_detail limit {},{}}'.format(scount, plus))

        temp = cur1.fetchall()
        print temp
        for row in temp:
            bq_id = row[1]
            bcourse = row[2]
            bgrade = row[3]
            bkn_pt = row[4]
            burl = row[5]
            boriginal = row[6]
            bq_source = row[7]
            bq_source_url = row[8]
            bq_text = row[9]
            bq_pt = row[10]
            bq_analysis = row[11]
            bq_answer = row[12]
            bq_comment = row[13]
            bis_choice = row[14]
            bright_choice = row[15]
            if row[16]:
                bmust_vip = row[16]
            else:
                bmust_vip = 0
            if row[17]:
                bdifficulty_degree = row[17]
            else:
                bdifficulty_degree = 0.5
            bq_choice_A = row[18]
            bq_choice_B = row[19]
            bq_choice_C = row[20]
            bq_choice_D = row[21]
            bq_choice_E = row[22]
            bq_choice_F = row[23]
            bq_choice_G = row[24]
            bq_choice_H = row[25]
            bq_choice_I = row[26]
            bq_choice_J = row[27]
            bq_fill_in_1 = row[28]
            bq_fill_in_2 = row[29]
            bq_fill_in_3 = row[30]
            bq_fill_in_4 = row[31]
            bq_fill_in_5 = row[32]
            bq_fill_in_6 = row[33]
            bq_fill_in_7 = row[34]
            bq_fill_in_8 = row[35]
            bq_fill_in_9 = row[36]
            bq_fill_in_10 = row[37]
            bcreate_timestamp = row[38]
            bsource = row[39]
            print "bb"
            num = ord_hash(str(bq_id))
            cur2.execute('insert into question_detail_{} (q_id,course,grade,kn_pt,url,original_html,q_source,'
                         'q_source_url,q_text,q_pt,q_analysis,q_answer,q_comment,is_choice,right_choice,must_vip,'
                         'difficulty_degree,q_choice_A,q_choice_B,q_choice_C,q_choice_D,q_choice_E,q_choice_F,'
                         'q_choice_G,q_choice_H,q_choice_I,q_choice_J,q_fill_in_1,q_fill_in_2,q_fill_in_3,'
                         'q_fill_in_4,q_fill_in_5,q_fill_in_6,q_fill_in_7,q_fill_in_8,q_fill_in_9,q_fill_in_10,'
                         'create_timestamp,source) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",'
                         '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",'
                         '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(num, bq_id, bcourse, bgrade,
                                                                                          bkn_pt,
                                                                                          burl, boriginal, bq_source,
                                                                                          bq_source_url, bq_text, bq_pt,
                                                                                          bq_analysis, bq_answer,
                                                                                          bq_comment, bis_choice,
                                                                                          bright_choice, bmust_vip,
                                                                                          bdifficulty_degree,
                                                                                          bq_choice_A, bq_choice_B,
                                                                                          bq_choice_C, bq_choice_D,
                                                                                          bq_choice_E, bq_choice_F,
                                                                                          bq_choice_G, bq_choice_H,
                                                                                          bq_choice_I, bq_choice_J,
                                                                                          bq_fill_in_1, bq_fill_in_2,
                                                                                          bq_fill_in_3, bq_fill_in_4,
                                                                                          bq_fill_in_5, bq_fill_in_6,
                                                                                          bq_fill_in_7, bq_fill_in_8,
                                                                                          bq_fill_in_9, bq_fill_in_10,
                                                                                          bcreate_timestamp, bsource))

        # bq_id = temp[0]
        # num = ord_hash(str(bq_id))
        # bgrade = temp[3]
        # print temp[3]
        # cur2.execute('insert into question_detail_{} (q_id,grade) values ("{}","{}")'.format(num, bq_id, bgrade))
        # cur2.execute('insert into question_detail_{}'.format(num))

        # temp = cur1.fetchall()
        # for row in temp:
        #     cur2.execute()
        conn1.commit()
        conn2.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur1.close()
        conn1.close()
        cur2.close()
        conn2.close()

if __name__ == "__main__":
    db1 = 'all_courses_latex'
    count = get_count(db1)
    # db2 = 'jyeoo_all_courses'
    # sum = get_count(db2)
    tloop = (SUM_COUNT-count)/SELECT_NUM
    for i in range(1, tloop+1):
        data2table(count, SELECT_NUM)
        count += SELECT_NUM
        print str(i)+"aaa"
    tcount = get_count(db1)
    data2table(tcount, SUM_COUNT-tcount)
    print count
    print "over"

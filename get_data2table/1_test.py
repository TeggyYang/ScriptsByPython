# coding = "utf-8"
import MySQLdb

MYSQL_TABLE = "question_detail"
SPLIT_NUM = 3
NAME_PREFIX = "question_detail_"


def get_count():
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', db='all_courses_latex', port=3306)
        cur = conn.cursor()
        count = 0
        for i in range(0, 100):
            cur.execute('select count(*) from question_detail_{} '.format(i))
            temp = cur.fetchone()[0]
            count += int(temp)
            print str(i) + " " + str(temp)
        print count
        cur.close()
        conn.close()
        return count
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def ord_hash(x):
    s = 0
    for c in x:
        s += ord(c)
    return s % SPLIT_NUM


def data2table(count):
    try:
        conn1 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='hwl413',  # db='jyeoo_all_courses',
                                port=3306)
        db1 = 'db009'
        cur1 = conn1.cursor()

        # print "aa"

        conn2 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='hwl413',  # db='all_courses_latex',
                                port=3306)
        db2 = 'jyeoo_all_courses'
        cur2 = conn2.cursor()

        # print "bb"

        cur1.execute('select * from {}.question_detail limit {},10'.format(db1, count))

        i = 0
        # print "cc"
        temp = cur1.fetchall()
        for box in temp:
            bq_id = box[1]
            num = ord_hash(str(bq_id))
            cur2.execute('insert into {}.question_detail_{} select * from {}.question_detail where q_id="{}"'.format(db2, num, db1, bq_id))
            i += 1
            if i == 1:
                print i
            if i % 10000 == 0:
                print i
        conn1.commit()
        conn2.commit()
        # sql = 'insert into {}.question_detail_{} (q_id) values("9009")'.format(db2, 0)
        # print sql
        # cur2.execute(sql)

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur1.close()
        conn1.close()
        cur2.close()
        conn2.close()

if __name__ == "__main__":
        # count = get_count()
        count = 1
        for i in range(1, 12):
            data2table(count)
            count += 10
            print str(i)+"aaa"
        print "over"

# coding = "utf-8"
import MySQLdb


def get_jyeoo_url():
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='***', db='jyeoo_all_courses', port=3306)
        cur = conn.cursor()
        cur.execute('select url from question_detail WHERE source="jyeoo" ')
        i = 0
        for row in cur.fetchall():
            fout.write(row[0]+"\n")
            i += 1
            if i % 10000 == 0:
                print i
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__ == "__main__":
    with open("get_url.txt", "w") as fout:
        get_jyeoo_url()
        print "over"

# coding=utf-8
import csv
import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def get_filenum(db_file_parent):
    file_list = os.listdir(db_file_parent)
    # print file_list
    count = 0
    for name in file_list:
        if name.startswith("question"):
            count += 1
    return count


def merge():
    with codecs.open(output_file_path, "w", encoding="utf-8") as fout:
        for i in range(1, file_num+1):
            if i == 2 or i == 3 or i == 12 or i == 21:
                subject = "math"
            elif i == 1 or i == 11 or i == 22:
                subject = "chinese"
            elif i == 4 or i == 13 or i == 20:
                subject = "english"
            elif i == 5 or i == 14:
                subject = "physics"
            elif i == 6 or i == 15:
                subject = "chemistry"
            elif i == 7 or i == 16:
                subject = "history"
            elif i == 8 or i == 17:
                subject = "politics"
            elif i == 9 or i == 18:
                subject = "geography"
            elif i == 10 or i == 19:
                subject = "bio"
            csv_file_path = "D:/xiao/question_cource_{}.csv".format(i)
            csvfile = file(csv_file_path, 'rb')
            reader = csv.reader(csvfile)
            count = 0
            for line in reader:
                # print line
                count += 1
                if(count != 1):
                    id = line[0].encode("utf8")
                    text = line[1].encode("utf8").replace("\n", "")
                    if line[2]:
                        id = line[2].split(",")[0]
                    fout.write(id + " " + subject + " " + text + "\n")
            print i


if __name__ == "__main__":
    db_file_parent = "D:/xiao"
    # 获取文件数
    file_num = get_filenum(db_file_parent)
    output_file_path = "D:/xiao/merge_change_id.txt"
    merge()
    print "over"

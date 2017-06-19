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
        with codecs.open(output_list_path, "w", encoding="utf-8") as fout_3list:
            for i in range(1, file_num+1):
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
                        fout.write(id + " " + text + "\n")
                        # fout.write(line[0]+" "+line[1])
                    if line[2]:
                        if(count != 1):
                            # fout_3list.write(line[0].encode("utf-8") + "\n")
                            fout_3list.write(line[0]+"\n")
                print i

    # test
    # csvfile = file('D:/xiao/question_cource_10.csv', 'rb')
    # reader = csv.reader(csvfile)
    # for line in reader:
    #     fout.write(line[0]+" "+line[1])
    #     if line[2]:
    #         fout_3list.write(line[0] + "\n")
    # csvfile.close()

if __name__ == "__main__":
    db_file_parent = "D:/xiao"
    # 获取文件数
    file_num = get_filenum(db_file_parent)
    output_file_path = "D:/xiao/merge_csv.txt"
    output_list_path = "D:/xiao/3list.txt"
    # fout = open(output_file_path, "w")
    # fout_3list = open(output_list_path, "w")
    merge()
    print "over"

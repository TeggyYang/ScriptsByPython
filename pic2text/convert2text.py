# coding: utf-8
import os
import GetOcrFromBaidu


def get_orc_result(pic_path):
    content = GetOcrFromBaidu.get_text_content(pic_path)
    fout.write(pic_path.split("\\")[-1].encode("utf8")+" "+content.replace("\n", "").encode("utf8")+"\n")

if __name__ == '__main__':
    db_file_parent = "D:\data_qus_qid_ch\d8"
    output_file_path = "D:\data_qus_qid_ch\pic2txt8.txt"
    file_list = os.listdir(db_file_parent)
    i = 0
    with open(output_file_path, "w") as fout:
        for pic in file_list:
            print pic
            pic_path = "D:\data_qus_qid_ch\d8\\" + pic
            # print pic_path
            get_orc_result(pic_path)
            i += 1
            print i
    # get_orc_result("D:\data_qus_qid_ch\\3MDNT0gk.png")
    print "over"
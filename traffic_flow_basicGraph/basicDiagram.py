# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：9:01
# 文件名：basicDiagram.py
# 开发工具：PyCharm
import numpy as np
import matplotlib.pyplot as plt
import os
import xlrd
import csv
import codecs
import argparse
import time


def args_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f","--file",required=True,help="excel file name")
    args = vars(ap.parse_args())
    return args

def xlsx_to_csv(filepath):
    filedir,filename = os.path.split(filepath)
    fn,ext = os.path.splitext(filename)
    workbook = xlrd.open_workbook(filepath)
    sheets =workbook.sheet_by_name()
    for i in range(len(sheets)):
        table = workbook.sheet_by_index(i)
        sht = fn+"_"+sheets[i]+".csv"
        with codecs.open(sht,"w",encoding="utf-8") as f:
            write = csv.writer(f)
            for row_num in range(table.nrows):
                row_value = table.row_values(row_num)
                write.writer(row_value)
        print(sht,"created")

if __name__ == '__main__':
    st = time.time()
    args = args_parse()
    filepath = args["file"]
    xlsx_to_csv(filepath)
    print("completed to convert",filepath,"to csv files")
    nd = time.time()
    tm =nd-st
    print("spend time",tm)



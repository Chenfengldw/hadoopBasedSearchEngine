import re
import os
import string
import xlrd
import xlwt
info_book = xlrd.open_workbook('info.xls')
info_sheet = info_book.sheets()[0]


def get_date(str):#get the information corresponding to the file name
    row_num = 0
    for name in info_sheet.col_values(0):
        if str == name:
            tmp = info_sheet.cell(row_num,1).value
            return tmp
        row_num = row_num+1


def get_index(str):#get the information corresponding to the file name
    row_num = 0
    for name in info_sheet.col_values(0):
        if str == name:
            tmp = info_sheet.cell(row_num,2).value
            return tmp
        row_num = row_num+1

def get_url(str):#get the information corresponding to the file name
    row_num = 0
    for name in info_sheet.col_values(0):
        if str == name:
            tmp = info_sheet.cell(row_num,3).value
            return tmp
        row_num = row_num+1






def main():

    input_file = open('out1.txt','r')
    output_table = xlwt.Workbook()
    sheet = output_table.add_sheet('Sheet1', cell_overwrite_ok=True)
    line = input_file.readline()
    row = 0

    while(line):
        if(line[0:3] != '8-k'):

            #get the word
            end1 = line.find('8-k')
            current = line[0:end1]
            sheet.write(row,0,current)

            #get the file name
            end2 = line.find(':')
            file_name = line[end1:end2]
            #print file_name
            date = get_date(file_name)
            index = get_index(file_name)
            url = get_url(file_name)
            sheet.write(row,1,date)
            sheet.write(row,2,index)
            sheet.write(row,3,url)

        else:
            sheet.write(row,0,current)
            end = line.find(':')
            file_name = line[0:end]
            #print file_name
            date = get_date(file_name)
            index = get_index(file_name)
            url = get_url(file_name)
            sheet.write(row,1,date)
            sheet.write(row,2,index)
            sheet.write(row,3,url)


        line = input_file.readline()
        row = row +1

    output_table.save("out1.xls")


main()






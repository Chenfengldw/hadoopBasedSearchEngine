#-*- coding: utf-8 -*-

import urllib
import urllib2
import time
import string
import re
import os
import sys
import xlwt
import xlrd
from BeautifulSoup import BeautifulSoup


class LoveBridge:
    def __init__(self):

        self.siteURL = "https://bbs.sjtu.edu.cn/"


        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

        self.subjects = []

        self.preurl = ""

    def clean(self,document):#clean the tokens of html and get the text we want
        #but this may exists some problems
        #soup = BeautifulSoup(document,fromEncoding="utf-8")
        #document = soup.getText().encode('utf-8')
        #document = document.replace('&#160;', ' ')
        #document = document.replace('&#163;', ' ')
        #document = document.replace('&#254;', ' x ')
        #document = document.replace('&#253;', ' x ')
        #document = document.replace('&#120;', ' x ')
        #document = document.replace('&#9746;', ' x ')
        #document = document.replace('&nbsp', ' ')
        #document = document.replace(';', ' ')
        #document = re.sub('<.*>', '',document)
        document = document.replace('\r\n', ' ')
        document = document.replace('\n', ' ')
        document = document.replace('\r', ' ')
        document = document.replace('    2312     ', ' ')
        #document = re.sub("<[ 0-9A-Za-z\-\=\/]+>", "", document)

        #document = re.sub("function jumpUrlx[ \n\t0-9A-Za-z]+", "", document)
        #document = re.sub("[!]", "", document)
        document = re.sub("[A-Za-z|\<|\>|\$|\}|\{|\(|\)|.|\=|\&|\~|\`|\:|\[|\]|\/|\'|\"|\?|\,|\+|\;|\!|\-|\_]","",document)
        #document = re.sub(u"^([\u4e00-\u9fa5]+)","",document)
        #print document
        #document=document.encode('utf-8')
        return document


    def open_url(self,url_address):
        global recursive_count
        try:
            tmp = urllib2.urlopen(url_address, timeout=5)
            result = tmp.read()
        except Exception, e:
            time.sleep(3)
            print url_address+'fail!'
            recursive_count += 1
            if recursive_count == 4:
                recursive_count = 0
                print "fail to recursive"
                return -2
            result = self.open_url(url_address)
            print str(e)
        return result

    def get_web_address(self,ft):
        pattern = re.compile("bbstcon,board,LoveBridge,reid,[0-9]+.html")
        document_add = pattern.findall(ft)
        return document_add

    def get_info(self,ft):
        pattern = re.compile('<tr><td>[0-9]+<td>[A-Z]<td><a href="bbsqry?userid=SJTUBBS">SJTUBBS</a><td>[a-zA-Z]+ [0-9]+ [0-9]+:[0-9]+<td>')
        info = pattern.findall(ft)
        return info

    def get_index(self,ft):
        pattern = re.compile('<td>[0-9]+<td>')
        index = pattern.findall(ft)

        pattern2 = re.compile('[0-9]+')
        index = pattern2.findall(str(index))

        return index

    def get_state(self,ft):
        pattern = re.compile('<td>[A-Z]<td>')
        state = pattern.findall(ft)

        pattern2 = re.compile('[A-Z]')
        state = pattern2.findall(str(state))

        return state

    def get_name(self,ft):
        pattern = re.compile('userid=[a-zA-Z]+')
        name = pattern.findall(ft)
        #del name[0]
        return name

    def get_date(self,ft):
        pattern = re.compile('[a-zA-Z]+ [0-9]+ [0-9]+:[0-9]+')
        date = pattern.findall(ft)
        return date

    def get_title(self,ft):
        pattern = re.compile('标  题 .* 发信站 饮水思源')
        title = pattern.findall(ft)
        return title
        

    def start(self, pages):
        output_xls = xlwt.Workbook()
        output_table = output_xls.add_sheet('Sheet1', cell_overwrite_ok=True)
        row = 0
        output_table.write(row,0,'index')
        output_table.write(row,1,'title')
        output_table.write(row,2,'name')
        output_table.write(row,3,'date')
        output_table.write(row,4,'state')
        output_table.write(row,5,'url')
        row = row+1

        reload(sys)
        sys.setdefaultencoding('utf-8')
        global recursive_count
        recursive_count = 0

        document_add = []#document address
        state = []#the state of one item
        name = []# the author's name
        date = []# the date of the item
        index= []#the index of the item
        title = []#the title of the item
        if pages < 1:

            return None
        else:
            for i in range(pages):
                url = self.siteURL + 'bbstdoc,board,LoveBridge,page,'+str(i)+'.html'
                ft = self.open_url(url)
                tmpdocument_add = self.get_web_address(ft)
                tmpstate = self.get_state(ft)
                tmpname = self.get_name(ft)
                tmpdate = self.get_date(ft)
                tmpindex = self.get_index(ft)

                document_add = document_add + tmpdocument_add
                state = state + tmpstate
                date = date + tmpdate
                name = name + tmpname
                index = index + tmpindex

        row = 1
        for j in range(1400):
            text = self.open_url(self.siteURL+document_add[j])
            output_file = open(str(index[j])+".txt",'w')
            text = self.clean(text)

            text = text.decode('gbk','ignore').encode('utf-8')
            #print text
            tmptitle = self.get_title(text)
            title = title +tmptitle
            #print tmptitle
            '''print index.__len__()
            print name.__len__()
            print date.__len__()
            print document_add.__len__()'''
            if (tmptitle.__len__() != 0):
                tmp = tmptitle[0]
                output_table.write(row,1,tmp.decode('utf-8'))
            output_table.write(row,0,index[j].decode('utf-8'))
            output_table.write(row,2,name[j].decode('utf-8'))
            output_table.write(row,3,date[j].decode('utf-8'))
            output_table.write(row,4,state[j].decode('utf-8'))
            output_table.write(row,5,document_add[j].decode('utf-8'))
            row = row+1


            output_file.write(text)
            output_file.close()
        output_xls.save('info.xls')
lb = LoveBridge()

lb.start(100)#this number means how many pages you want to get (from 1 to xxx)


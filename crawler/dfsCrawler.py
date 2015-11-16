# encoding=utf8
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
#  a crawler to search company information in their 10K form
#
#  first input excel file, use BeautifulSoup to parse and get basic information,
#  get the 10-K file, and filter, then analyize
#
#  input: input.xls
#  output: output.xls
#
#  write by Zhenyu
#
# --------------------------------------------------------------------


from BeautifulSoup import BeautifulSoup
import urllib2
import re
import string
import xlrd
import xlwt
import sys
import time

'''output_list = ['CIK', 'Filings', 'Period_of_Report', 'Filing_Date', 'Well_Known_Seasoned_Issuer',
               'Not_Required_to_File', 'Large_Accelerated_Filer', 'Accelerated_Filer', 'Non_Accelerated_Filer',
               'Smaller_Reporting_Company', 'Shell_Company', 'Proxy_Incorporated_by_Reference', 'Used_COSO',
               'Version_of_COSO']'''

output_list =['CIK', 'Filings', 'Period_of_Report', 'Filing_Date','Item7.0.1','Item8.0.1']

symbol = 'x'








# initial (load and write)


def progress(width, percent):
    print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * '='), percent),
    if percent >= 100:
        print
        sys.stdout.flush()


def open_url(url_address):
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
        result = open_url(url_address)
        print str(e)
    return result


def get_cik_list():
    input_file = xlrd.open_workbook('inputdfs.xls')
    sheet = input_file.sheets()[0]
    cik_list = []
    for i in range(sheet.nrows - 1):
        cik_list += [int(sheet.cell(i + 1, 0).value)]
    return cik_list
    # tmp_list = [1961]
    # return tmp_list

    

def get_item_list(cik_num, filing_type):
    aim_web1 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + str(
        cik_num) + '&type=' + filing_type + '&dateb=&owner=exclude&start=0&count=100'
    ct = open_url(aim_web1)
    if ct == -2:
        return -2
    soup = BeautifulSoup(ct)

    aim_web2 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + str(
        cik_num) + '&type=' + filing_type + '&dateb=&owner=exclude&start=100&count=100'
    ct2 = open_url(aim_web2)
    if ct2 == -2:
        return -2
    soup2 = BeautifulSoup(ct2)

    table1 = soup.findAll('tr')
    flag = ct.find('No matching CIK')#check whether this CIK is empty
    if flag > 0 or len(table1) < 4:
        table = []
        return table1
    
    del table1[table1.__len__()-1]
    for i in range(3):
        del table1[0]

    table2 = soup2.findAll('tr')
    for i in range(3):
        del table2[0]

    table=table1+table2
    return table


def get_item_fileNo(item):
    ft = item.contents[9].contents[2]
    return ft

def get_item_date(item):

    filing_date = item.contents[7].contents[0][0:4]+item.contents[7].contents[0][5:7]+item.contents[7].contents[0][8:10]
    return filing_date
    
def get_web_address(item, time_threshold):
    base_address = 'https://www.sec.gov'
    filing_date = item.contents[7].contents[0][0:4]+item.contents[7].contents[0][5:7]+item.contents[7].contents[0][8:10]
    #print item.contents[7].contents[0]
    if string.atoi(filing_date) <= string.atoi(time_threshold):
        return 0
    item_address = base_address+item.a['href']
    return item_address


def get_general(web_address, cik, filing_type):
    et = open_url(web_address)
    if et == -2:
        return -2
    soup_each = BeautifulSoup(et)
    form_content = soup_each.findAll('div', {'class': 'formGrouping'})

    
    tr_all = soup_each.findAll('tr', {})
    flag = False
    tr = 0
    for tr in tr_all:
        for td in tr:
            if not td.string:
                continue
            if filing_type in td.string:
                flag = True
                break
        if flag:
            break

    # actually I do not consider the case the tr_all has nothing
    file_name = tr.contents[5].a.string
    if file_name is None:
        return -1
    file_address = web_address[0:web_address.rindex("/")+1]+file_name
    return file_address


def clean(document, document_type):
    if document_type == 0:
        soup = BeautifulSoup(document)
        document = soup.getText()
        document = document.replace('&#160;', ' ')
        document = document.replace('&#163;', ' ')
        document = document.replace('&#254;', ' x ')
        document = document.replace('&#253;', ' x ')
        document = document.replace('&#120;', ' x ')
        document = document.replace('&#9746;', ' x ')
        document = document.replace('&nbsp', ' ')
        document = document.replace(';', ' ')
    document = document.replace('\t', ' ')
    document = document.replace('\r\n', ' ')
    document = document.replace('\n', ' ')
    document = document.replace('\r', ' ')
    document = re.sub(' +', ' ', document)
    #document = document.lower()
    return document





def main(filing_type, time_threshold):
    # for each cik get the web list
    print "start "+filing_type+"collection"
    cik_list = get_cik_list()
    global output_table
    global symbol

    # for each available item get basic information
    global row_num
    global recursive_count
    recursive_count = 0
    row_num = 1
    cik_count = 0
    cik_total = len(cik_list)
    for cik in cik_list:
        item_list = get_item_list(cik, filing_type)
        if item_list == -2:
            continue

        # check if no filings
        if len(item_list) == 0:
            print 'error'
            row_num += 1
            continue

        for item in item_list:
            
            #symbol = 'x'

            if item.contents[1].contents[0]!='8-K':
                continue
            form_web = get_web_address(item,time_threshold)
  
            # form_web = "https://www.sec.gov/Archives/edgar/data/1800/000104746913003504/0001047469-13-003504-index.htm"
            if form_web == 0:
                continue 
            document_web = get_general(form_web, cik, filing_type)
            if document_web == -1 or document_web == -2:
                continue
                
            # get the general information and return if the document is html(0) or txt(1) or other(2)
            if '.htm' in document_web:
                file_type = 0
            elif '.txt' in document_web:
                file_type = 1
            else:
                file_type = 2



            # go to the 8-K file

            ft = open_url(document_web)
            #print ft
            if ft == -2:
                continue
            document = clean(ft, file_type)
            filing_date = get_item_date(item)
            fileNo = get_item_fileNo(item)
            str = "C:\Users\Administrator\Desktop\company_search-master\in\8-k_date" + filing_date + "_fileNO" +fileNo+ ".txt"
            output_file = open(str,'w')
            output_file.write(document)
            output_file.close();
            row_num += 1

    cik_count += 1
    print "%d of %d" % (cik_count, cik_total)
    output_file.close();

main('8-K', '20000101')
#main('10-KSB', '20000101')

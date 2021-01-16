import json
import csv
import sys
import os
import datetime
import xlrd

def excel_read(name):
    file = xlrd.open_workbook(name)
    sheet = file.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    all_content = []
    for i in range(rows):
        all_content.append(sheet.row_values(i))
    return all_content

def csv_read(name):
    file = csv.reader(open(name,'r'))
    rows = []
    for a in file:
        rows.append(a)
    return rows

__s_date = datetime.date(1899, 12, 31).toordinal() - 1
def getdate(date):
    if isinstance(date, float):
        date = int(date)
    d = datetime.date.fromordinal(__s_date + date)
    return d

def rrr_xlsx_csv():
    b = excel_read('rrr.xlsx')
    c = []
    for i in range(len(b)):
        if i > 0:
            a = b[i]
            t = []
            t.append(getdate(a[0]).strftime("%Y-%m-%d"))
            t.append(getdate(a[1]).strftime("%Y-%m-%d"))
            t.append(a[2])
            t.append(a[3])
            t.append(a[4])
            t.append(a[5])
            t.append(a[6])
            t.append(a[7])
            c.append(t)
    c.sort(key=lambda entry: entry[0], reverse=False)
    d = []
    for i in range(len(c)):
        d.append(','.join(a if isinstance(a, str) else str(a) for a in c[i]))
    with open('rrr.csv', 'w') as f:
        f.write('\n'.join(d))

def rrr_csv_json():
    c = csv_read('rrr.csv')
    d = []
    for i in range(len(c)):
        a = c[i]
        t = [
            '"公布时间":"{}"'.format(a[0]),
            '"生效时间":"{}"'.format(a[1]),
            '"大型金融机构":{}'.format(a[3]),
            '"中小金融机构":{}'.format(a[6]),
        ]
        d.append('   {' + ','.join(t) + '}')
    with open('rrr.json', 'w') as f:
        f.write('[\n' + ',\n'.join(d) + '\n]')


def mmm_xlsx_csv():
    b = excel_read('mmm.xlsx')
    c = []
    for i in range(len(b)):
        if i > 1:
            a = b[i]
            t = []
            t.append(datetime.datetime.strptime(a[0].replace("年","-").replace("月份",""), '%Y-%m').strftime("%Y-%m"))
            t.append(int(a[1]))
            t.append(a[2])
            t.append(a[3])
            t.append(int(a[4]))
            t.append(a[5])
            t.append(a[6])
            t.append(int(a[7]))
            t.append(a[8])
            t.append(a[9])
            c.append(t)
    c.sort(key=lambda entry: entry[0], reverse=False)
    d = []
    for i in range(len(c)):
        d.append(','.join(a if isinstance(a, str) else str(a) for a in c[i]))
    with open('mmm.csv', 'w') as f:
        f.write('\n'.join(d))

def mmm_csv_json():
    c = csv_read('mmm.csv')
    d = []
    for i in range(len(c)):
        a = c[i]
        t = [
            '"月份":"{}"'.format(a[0]),
            '"M0亿元":{}'.format(a[1]),
            '"M0同比增长":{}'.format(a[2]),
            '"M0环比增长":{}'.format(a[3]),
            '"M1亿元":{}'.format(a[4]),
            '"M1同比增长":{}'.format(a[5]),
            '"M1环比增长":{}'.format(a[6]),
            '"M2亿元":{}'.format(a[7]),
            '"M2同比增长":{}'.format(a[8]),
            '"M2环比增长":{}'.format(a[9]),
        ]
        d.append('   {' + ','.join(t) + '}')
    with open('mmm.json', 'w') as f:
        f.write('[\n' + ',\n'.join(d) + '\n]')

def rrr():
    rrr_xlsx_csv()
    rrr_csv_json()

def mmm():
    mmm_xlsx_csv()
    mmm_csv_json()

rrr()
mmm()

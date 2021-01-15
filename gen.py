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

def rrr_excel(rows):
    z = []
    for i in range(len(rows)):
        if i > 0:
            a = rows[i]
            b = []
            b.append(getdate(a[0]).strftime("%Y-%m-%d"))
            b.append(getdate(a[1]).strftime("%Y-%m-%d"))
            b.append(a[2])
            b.append(a[3])
            b.append(a[4])
            b.append(a[5])
            b.append(a[6])
            b.append(a[7])
            z.append(b)
    return z

def rrr_csv(rows):
    z = []
    for i in range(len(rows)):
        if i > 0:
            a = rows[i]
            b = []
            b.append(datetime.datetime.strptime(a[0].replace("年","-").replace("月","-").replace("日",""), '%Y-%m-%d').strftime("%Y-%m-%d"))
            b.append(datetime.datetime.strptime(a[1].replace("年","-").replace("月","-").replace("日",""), '%Y-%m-%d').strftime("%Y-%m-%d"))
            b.append(float(a[2].replace("%",""))/100)
            b.append(float(a[3].replace("%",""))/100)
            b.append(float(a[4].replace("%",""))/100)
            b.append(float(a[5].replace("%",""))/100)
            b.append(float(a[6].replace("%",""))/100)
            b.append(float(a[7].replace("%",""))/100)
            z.append(b)
    return z

def rrr():
    # z = rrr_csv(csv_read('rrr.csv'))
    z = rrr_excel(excel_read('rrr.xlsx'))
    z.sort(key=lambda entry: entry[0], reverse=False)
    with open('rrr.json', 'w') as f:
        f.write('[\n')
        for j in range(len(z)):
            a = z[j]
            f.write('   {')
            f.write('"公布时间":"{}",'.format(a[0]))
            f.write('"生效时间":"{}",'.format(a[1]))
            f.write('"大型金融机构":{:.3f},'.format(a[3]))
            f.write('"中小金融机构":{:.3f}'.format(a[6]))
            if j != len(z) - 1:
                f.write('},\n')
            else:
                f.write('}\n')
        f.write(']')

def mmm():
    s = csv_read('mmm.csv')
    z = []
    for i in range(len(s)):
        if i > 0:
            a = s[i]
            b = []
            b.append(datetime.datetime.strptime(a[0].replace("年","-").replace("月份",""), '%Y-%m').strftime("%Y-%m"))
            b.append(int(a[1]))
            b.append(float(a[2].replace("%",""))/100)
            b.append(float(a[3].replace("%",""))/100)
            b.append(int(a[4]))
            b.append(float(a[5].replace("%",""))/100)
            b.append(float(a[6].replace("%",""))/100)
            b.append(int(a[7]))
            b.append(float(a[8].replace("%",""))/100)
            b.append(float(a[9].replace("%",""))/100)
            z.append(b)
    z.sort(key=lambda entry: entry[0], reverse=False)
    with open('mmm.json', 'w') as f:
        f.write('[\n')
        for j in range(len(z)):
            a = z[j]
            f.write('   {')
            f.write('"月份":"{}",'.format(a[0]))
            f.write('"M0亿元":{},'.format(a[1]))
            f.write('"M0同比增长":{:.4f},'.format(a[2]))
            f.write('"M0环比增长":{:.4f},'.format(a[3]))
            f.write('"M1亿元":{},'.format(a[4]))
            f.write('"M1同比增长":{:.4f},'.format(a[5]))
            f.write('"M1环比增长":{:.4f},'.format(a[6]))
            f.write('"M2亿元":{},'.format(a[7]))
            f.write('"M2同比增长":{:.4f},'.format(a[8]))
            f.write('"M2环比增长":{:.4f}'.format(a[9]))
            if j != len(z) - 1:
                f.write('},\n')
            else:
                f.write('}\n')
        f.write(']')


rrr()
mmm()

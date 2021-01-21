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
    rows = []
    try:
        with open(name, 'r') as f:
            h = csv.reader(f)
            for a in h:
                rows.append(a)
    except:
        pass
    return rows

def csv_write(name, rows):
    with open(name, 'w') as f:
        h = csv.writer(f)
        for i in rows:
            h.writerow(i)

def json_read(name):
    rows = []
    try:
        with open(name, 'r') as f:
            rows = json.load(f)
    except:
        pass
    return rows

def json_write(name, rows):
    with open(name, 'w') as f:
        t1 = []
        for a in rows:
            t2 = []
            for b in a:
                t2.append('"' + b + '":' + ('"' + a[b] + '"' if isinstance(a[b], str) else str(int(a[b]))))
            t1.append('  {' + ','.join(t2) + '}')
        f.write('[\n' + ',\n'.join(t1) + '\n]')

__s_date = datetime.date(1899, 12, 31).toordinal() - 1
def getdate(date):
    if isinstance(date, float):
        date = int(date)
    d = datetime.date.fromordinal(__s_date + date)
    return d

def fetch_safe(d, k, i):
    if k not in d:
        return 0
    return 0 if isinstance(d[k][i], str) else float(d[k][i])


def rrr_xlsx_csv():
    b = excel_read('rrr.xlsx')
    c = []
    for i in range(len(b)):
        if i > 1:
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
    c.sort(key=lambda entry: entry[0] + entry[1], reverse=False)
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

def rrr():
    rrr_xlsx_csv()
    rrr_csv_json()


def to_json(d, e, json_file_name):
    c = json_read(json_file_name)
    year = int(d["Item"][0])
    for i in range(12):
        date = str(year) + '-' + '{:02}'.format(i + 1)
        if isinstance(d[e][i], str):
            break
        t = {}
        t["月份"] = date
        for a in d:
            if a != "Item":
                t[a] = 0 if isinstance(d[a][i], str) else float(d[a][i])
        for j in range(len(c)):
            if c[j]["月份"] == date:
                c[j] = t
                break 
        else:
            c.append(t)
    c.sort(key=lambda entry: entry["月份"], reverse=False)
    json_write(json_file_name, c)

def to_csv(d, e, cols, csv_file_name):
    c = csv_read(csv_file_name)
    year = int(d["Item"][0])
    for i in range(12):
        date = str(year) + '-' + '{:02}'.format(i + 1)
        if isinstance(d[e][i], str):
            break
        t = [ date ]
        for a in cols:
            t.append(int(fetch_safe(d, a, i)))
        for j in range(len(c)):
            if c[j][0] == date:
                c[j] = t
                break 
        else:
            c.append(t)
    c.sort(key=lambda entry: entry[0], reverse=False)
    csv_write(csv_file_name, c)

def mmm_xlsx(filename):
    b = excel_read(filename)
    d = {"Item": [], "M0": [], "M1": [], "M2": []}
    for i, a in enumerate(b):
        if '项目 Item' in a[0]:
            d["Item"] = a[3:]
        elif '流通中货币（M0）' in a[2]:
            d["M0"] = a[3:]
        elif '货币（M1）' in a[1]:
            d["M1"] = a[3:]
        elif '货币和准货币（M2）' in a[0]:
            d["M2"] = a[3:]
    return d

def mmm(filename):
    d = mmm_xlsx(filename)
    to_csv(d, 'M2', ['M0', 'M1', 'M2'], 'mmm.csv')
    to_json(d, 'M2', 'mmm.json')


def has_it(d, s):
    dd = d.upper().replace(' ', ' ').replace('\u3000', ' ')
    ss = s.upper().replace(' ', ' ').replace('\u3000', ' ')
    d1 = dd.split(' ')
    s1 = ss.split(' ')
    for a in s1:
        if a not in d1:
            return False
    d2 = dd.replace(' ', '')
    s2 = ss.replace(' ', '')
    if s2 not in d2:
        return False
    return True


def balance1_xlsx(filename):
    b = excel_read(filename)
    d = {}
    for i, a in enumerate(b):
        if has_it(a[0], '项目'):
            d["Item"] = a[1:]
        elif has_it(a[0], '国外资产 Foreign Assets'):
            d["国外资产"] = a[1:]
        elif has_it(a[0], '外汇'):
            d["外汇"] = a[1:]
        elif has_it(a[0], '货币黄金'):
            d["货币黄金"] = a[1:]
        elif has_it(a[0], '其他国外资产 Other Foreign Assets'):
            d["其他国外资产"] = a[1:]
        elif has_it(a[0], '对政府债权'):
            d["对政府债权"] = a[1:]
        elif has_it(a[0], '其中：中央政府'):
            d["中央政府"] = a[1:]
        elif has_it(a[0], '对其他存款性公司债权'):
            d["对其他存款性公司债权"] = a[1:]
        elif has_it(a[0], '对其他金融性公司债权') or has_it(a[0], '对其他金融机构债权'):
            d["对其他金融性公司债权"] = a[1:]
        elif has_it(a[0], '对非金融性部门债权') or has_it(a[0], '对非金融性公司债权') or has_it(a[0], '非金融机构债权'):
            d["对非金融性部门债权"] = a[1:]
        elif has_it(a[0], '其他资产'):
            d["其他资产"] = a[1:]
        elif has_it(a[0], '总资产'):
            d["总资产"] = a[1:]
        elif has_it(a[0], '储备货币'):
            d["储备货币"] = a[1:]
        elif has_it(a[0], '货币发行'):
            d["货币发行"] = a[1:]
        elif has_it(a[0], '金融性公司存款 Deposits of Financial Corporations') or has_it(a[0], '金融机构存款 Deposits of Financial Corporations'):
            d["金融性公司存款"] = a[1:]
        elif has_it(a[0], '其他存款性公司存款'): # 包含于 金融性公司存款
            d["其他存款性公司存款"] = a[1:]
        elif has_it(a[0], '其他金融性公司存款') or has_it(a[0], '其他金融机构'): # 包含于 金融性公司存款
            d["其他金融性公司存款"] = a[1:]
        elif  has_it(a[0], '非金融机构存款') or has_it(a[0], '非金融性公司存款'):
            d["非金融机构存款"] = a[1:]
        elif has_it(a[0], '不计入储备货币的金融性公司存款'):
            d["不计入储备货币的金融性公司存款"] = a[1:]
        elif has_it(a[0], '发行债券'):
            d["发行债券"] = a[1:]
        elif has_it(a[0], '国外负债'):
            d["国外负债"] = a[1:]
        elif has_it(a[0], '政府存款'):
            d["政府存款"] = a[1:]
        elif has_it(a[0], '自有资金'):
            d["自有资金"] = a[1:]
        elif has_it(a[0], '其他负债'):
            d["其他负债"] = a[1:]
        elif has_it(a[0], '总负债'):
            d["总负债"] = a[1:]
        else:
            print(a[0])
    return d

def balance1(filename):
    print('货币当局资产负债表 ' + filename)
    d = balance1_xlsx(filename)
    if len(d) > 0:
        t = ["国外资产", "外汇", "货币黄金", "其他国外资产", "对政府债权", "中央政府", "对其他存款性公司债权", "对其他金融性公司债权", "对非金融性部门债权", "其他资产", "总资产", "储备货币", "货币发行", "金融性公司存款", "其他存款性公司存款", "其他金融性公司存款", "非金融机构存款", "不计入储备货币的金融性公司存款", "发行债券", "国外负债", "政府存款", "自有资金", "其他负债", "总负债"]
        to_csv(d, '总资产', t, 'balance1.csv')
        to_json(d, '总资产', 'balance1.json')

def balance2_xlsx(filename):
    b = excel_read(filename)
    d = {}
    for i, a in enumerate(b):
        if '项目' in a[0] and 'Item' in a[0]:
            d["Item"] = a[1:]
        elif has_it(a[0], '国外资产 Foreign Assets'):
            d["国外资产"] = a[1:]
        elif has_it(a[0], '储备资产 Reserve Assets'):
            d["储备资产"] = a[1:]
        elif has_it(a[0], '准备金存款 Deposits with Central Bank'):
            d["准备金存款"] = a[1:]
        elif has_it(a[0], '库存现金 Cash in Vault'):
            d["库存现金"] = a[1:]
        elif has_it(a[0], '对政府债权'):
            d["对政府债权"] = a[1:]
        elif has_it(a[0], '其中：中央政府'):
            d["对中央政府债权"] = a[1:]
        elif has_it(a[0], '对中央银行债权') or has_it(a[0], '央行债券'):
            d["对中央银行债权"] = a[1:]
        elif has_it(a[0], '对其他存款性公司债权'):
            d["对其他存款性公司债权"] = a[1:]
        elif has_it(a[0], '对其他金融机构债权') or has_it(a[0], '对其他金融性公司债权'):
            d["对其他金融机构债权"] = a[1:]
        elif has_it(a[0], '对非金融机构债权') or has_it(a[0], '对非金融性公司债权'):
            d["对非金融机构债权"] = a[1:]
        elif has_it(a[0], '对其他居民部门债权'):
            d["对其他居民部门债权"] = a[1:]
        elif has_it(a[0], '其他资产 Other Assets'):
            d["其他资产"] = a[1:]
        elif has_it(a[0], '总资产 Total Assets'):
            d["总资产"] = a[1:]
        elif has_it(a[0], '对非金融机构及住户负债'):
            d["对非金融机构及住户负债"] = a[1:]
        elif has_it(a[0], '纳入广义货币的存款 Deposits Included'):
            d["纳入广义货币的存款"] = a[1:]
        elif has_it(a[0], '单位活期存款') or has_it(a[0], '企业活期存款'):
            d["单位活期存款"] = a[1:]
        elif has_it(a[0], '单位定期存款') or has_it(a[0], '企业定期存款'):
            d["单位定期存款"] = a[1:]
        elif has_it(a[0], '个人存款 Personal Deposits') or has_it(a[0], '居民储蓄存款 Saving Deposits'):
            d["个人存款"] = a[1:]
        elif has_it(a[0], '不纳入广义货币的存款 Deposits Excluded'):
            d["不纳入广义货币的存款"] = a[1:]
        elif has_it(a[0], '可转让存款 Transferable Deposits'):
            d["可转让存款"] = a[1:]
        elif has_it(a[0], '其他存款 Other Deposits'):
            d["其他存款"] = a[1:]
        elif has_it(a[0], '其他负债存款'):
            d["其他负债存款"] = a[1:]
        elif has_it(a[0], '对中央银行负债'):
            d["对中央银行负债"] = a[1:]
        elif has_it(a[0], '对其他存款性公司负债'):
            d["对其他存款性公司负债"] = a[1:]
        elif has_it(a[0], '对其他金融性公司负债'):
            d["对其他金融性公司负债"] = a[1:]
        elif has_it(a[0], '其中：计入广义货币的存款'):
            d["计入广义货币的存款"] = a[1:]
        elif has_it(a[0], '国外负债 Foreign Liabilities'):
            d["国外负债"] = a[1:]
        elif has_it(a[0], '债券发行 Bond Issue'):
            d["债券发行"] = a[1:]
        elif has_it(a[0], '实收资本 Paid-in Capital'):
            d["实收资本"] = a[1:]
        elif has_it(a[0], '其他负债 Other Liabilities'):
            d["其他负债"] = a[1:]
        elif has_it(a[0], '总负债 Total Liabilities'):
            d["总负债"] = a[1:]
        else:
            print(a[0])
    return d

def balance2(filename):
    print('其他存款性公司资产负债表 ' + filename)
    d = balance2_xlsx(filename)
    if len(d) > 0:
        t = ["国外资产", "储备资产", "准备金存款", "库存现金", "对政府债权", "对中央政府债权", "对中央银行债权", "对其他存款性公司债权", "对其他金融机构债权", "对非金融机构债权", "对其他居民部门债权", "其他资产", "总资产", "对非金融机构及住户负债", "纳入广义货币的存款", "单位活期存款", "单位定期存款", "个人存款", "不纳入广义货币的存款", "可转让存款", "其他存款", "其他负债存款", "对中央银行负债", "对其他存款性公司负债", "对其他金融性公司负债", "计入广义货币的存款", "国外负债", "债券发行", "实收资本", "其他负债", "总负债"]
        to_csv(d, '总资产', t, 'balance2.csv')
        to_json(d, '总资产', 'balance2.json')

def detect(filename):
    file = xlrd.open_workbook(filename)
    sheet = file.sheet_by_index(0)
    a = sheet.cell_value(0, 0)
    if '货币供应量' == a:
        mmm(filename)
    if '货币当局资产负债表' == a:
        balance1(filename)
    if '其他存款性公司资产负债表' == a:
        balance2(filename)


def seek(path):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.xls') or file.endswith('.xlsx'):
            detect(os.path.join(path, file))

seek('./res')
rrr()


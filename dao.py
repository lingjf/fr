import json

with open('mmm.json', 'r') as f:
    mmm = json.load(f)
with open('balance1.json', 'r') as f:
    balance1 = json.load(f)
with open('balance2.json', 'r') as f:
    balance2 = json.load(f)
with open('balance3.json', 'r') as f:
    balance3 = json.load(f)

def get(begin='2006-00'):
    Mm = list(filter(lambda a: a["月份"] > begin, mmm))
    B1 = list(filter(lambda a: a["月份"] > begin, balance1))
    B2 = list(filter(lambda a: a["月份"] > begin, balance2))
    B3 = list(filter(lambda a: a["月份"] > begin, balance3))

    M = list(map(lambda a: a["月份"], Mm))
    D = {}
    for i in M:
        D[i] = {}
        for j in Mm:
            if j["月份"] == i:
                 D[i]["货币供应量"] = j
        for j in B1:
            if j["月份"] == i:
                 D[i]["货币当局资产负债表"] = j
        for j in B2:
            if j["月份"] == i:
                 D[i]["其他存款性公司资产负债表"] = j
        for j in B2:
            if j["月份"] == i:
                 D[i]["金融机构人民币信贷收支表"] = j

    Z = list(zip(Mm, B1, B2, B3))
    return M, Z, D

def subset2(Z, k):
    S = []
    for z in Z:
        s = {}
        for a in k:
            for b in z:
                if a in b:
                    s[a] = b[a]
        S.append(s)
    return S

def subset1(Z, k):
    S = []
    for z in Z:
        s = {}
        for a in k:
            for b in k[a]:
                c = 1 if b in z[0] else 0 + 1 if b in z[1] else 0 + 1 if b in z[2] else 0 + 1 if b in z[3] else 0
                if a == "货币供应量":
                    s[(("货币供应量" + ".") if c > 1 else "") + b] = z[0][b] if b in z[0] else 0
                if a == "货币当局资产负债表":
                    s[(("货币当局资产负债表" + ".") if c > 1 else "") + b] = z[1][b] if b in z[1] else 0
                if a == "其他存款性公司资产负债表":
                    s[(("其他存款性公司资产负债表" + ".") if c > 1 else "") + b] = z[2][b] if b in z[2] else 0
                if a == "金融机构人民币信贷收支表":
                    s[(("金融机构人民币信贷收支表" + ".") if c > 1 else "") + b] = z[3][b] if b in z[3] else 0
        S.append(s)
    return S

def subset(Z, k):
    if isinstance(k, list):
        return subset2(Z, k)
    else:
        return subset1(Z, k)

if __name__ == '__main__':
    M, Z, D = get('2006-00')
    # a = subset(Z, {"货币供应量":["M0", "M1"]})
    # print(a)
    # b = subset(Z, ["M0", "M1"])
    # print(b)
    # print(Z[0][0].keys())
    # print(Z[0][1].keys())
    # print(Z[-1][2].keys())
    # print(Z[-1][3].keys())
    # print('')
    # print(set(Z[0][1].keys()).intersection(set(Z[0][2].keys())))
    # print(set(Z[0][1].keys()).intersection(set(Z[0][3].keys())))
    # print(set(Z[0][2].keys()).intersection(set(Z[0][3].keys())))


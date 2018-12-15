import pdftotext
import re
f = open('./20181106-statements-0798-.pdf','rb')
pdf = pdftotext.PDF(f)
fullpdf = ""
for i in range(len(pdf)):
    fullpdf=fullpdf+str(pdf[i])
fullpdf=fullpdf.replace('\r','|')
fullpdf=fullpdf.replace('\n','|')

to_csv = '\s{2,}'
pg2 = re.compile(to_csv)
colDiv = '^'
fullpdf = pg2.sub(colDiv,fullpdf)

seg_select = '\\*start\\*.*?\\*end\\*'
pg = re.compile(seg_select)
res = pg.findall(fullpdf)

accounts = {}
cur_account = ''
for i in res:
    lines = i.split('|'+colDiv)
    seg_title = lines[0].split('*')[2]
    if seg_title == 'summary':
        cur_account = lines[1][:len(lines[1])]
        accounts[cur_account] = []
    if seg_title == 'transactiondetail':
        for j in range(3,len(lines)-1):
            if lines[j].count('^')<3 or lines[j][0]=='D':
                continue
            parts = lines[j].split('^')
            date = parts[0]
            balance = parts[-1]
            amount = parts[-2]
            des = ''
            for k in range(1,len(parts)-2):
                des += parts[k]
            accounts[cur_account].append((date,des,amount,balance))

f2 = open('11.txt','w+')
for i in accounts:
    f2.write(i+'\n')
    for l in accounts[i]:
        for e in l:
            f2.write(e+'^')
        f2.write('\n')
f2.close()


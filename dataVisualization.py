#!/usr/bin/env python
# coding: utf-8

# In[76]:


import pyecharts
import pandas
f = open('11.txt','r')
accounts = {}
cur_acc_name = ''
for i in f:
    if i.find('^') == -1:
        cur_acc_name = i[:len(i)-1]
        accounts[cur_acc_name] = {'date':[],'description':[],'amount':[],'balance':[]}
        continue
    p = i.split('^')
    if p[2][0]!='-':
        continue
    accounts[cur_acc_name]['date'].append(p[0])
    accounts[cur_acc_name]['description'].append(p[1])
    accounts[cur_acc_name]['amount'].append(float(p[2].replace(',','')))
    accounts[cur_acc_name]['balance'].append(float(p[3].replace(',','')))
f.close()


# In[77]:


lineChart = pyecharts.Line()
lineChart.add('test',x_axis=list(range(len(accounts['CHECKING SUMMARY']['amount']))),y_axis=accounts['CHECKING SUMMARY']['balance'])


# In[78]:


import json
f = open('rec_cat.json')
raws = f.read()
raws = raws.replace('\n','')
raws = raws.replace('\t','')
f.close()
dic = json.loads(raws)
dic.append({'name':'other','keys':[]})


# In[79]:


l = len(accounts['CHECKING SUMMARY']['date'])


cat_sum=dict()
for i in dic:
    cat_sum[i['name']] = 0
for i in range(l):
    cated = False
    for j in dic:
        flg = False
        for k in j['keys']:
            if accounts['CHECKING SUMMARY']['description'][i].lower().find(k) != -1:
                cat_sum[j['name']] += accounts['CHECKING SUMMARY']['amount'][i]
                flg = True
                cated = True
                break
    if flg is True:
        break
    if cated is False:
        print(accounts['CHECKING SUMMARY']['description'][i])
        cat_sum['other'] += accounts['CHECKING SUMMARY']['amount'][i]
cat_sum


# In[81]:


pie = pyecharts.Pie()
attr = []
v = []
for i in cat_sum:
    attr.append(i)
    v.append(round(cat_sum[i]*-1,2))
pie.add('test',attr,v,is_legend_show=False, is_label_show=True)


# In[ ]:





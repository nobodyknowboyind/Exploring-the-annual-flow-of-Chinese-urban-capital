# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 23:47:52 2019

@author: 安东
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
% matplotlib inline

import warnings
warnings.filterwarnings('ignore') 
# 不发出警告

from bokeh.io import output_notebook
output_notebook()
# 导入notebook绘图模块

from bokeh.plotting import figure,show
from bokeh.models import ColumnDataSource,HoverTool
# 导入图表绘制、图标展示模块
# 导入ColumnDataSource模块
# 数据读取，筛选出“同城投资”、“跨城投资”数据

df = pd.read_excel('C:/Users/安东/Desktop/项目12中国城市资本流动问题探索/data.xlsx')
# 数据读取

df = df.groupby(['投资方所在城市','融资方所在城市','年份']).sum().reset_index()
# 汇总数据

data_tc = df[df['投资方所在城市'] == df['融资方所在城市']]
data_tc = data_tc.sort_values(by = '投资企业对数',ascending = False).reset_index()
del data_tc['index']
# 筛选出“同城投资”数据

data_kc = df[df['投资方所在城市'] != df['融资方所在城市']]
data_kc = data_kc.sort_values(by = '投资企业对数',ascending = False).reset_index()
del data_kc['index']
# 筛选出“跨城投资”数据
# 比较一下“同城投资”、“跨城投资”TOP20的数据分布
# 按照2013-2017年的汇总数据来计算，比较

tc_sum = data_tc.groupby(['投资方所在城市','融资方所在城市']).sum().sort_values(by = '投资企业对数',ascending = False)
del tc_sum['年份']
# 汇总“同城投资”数据

kc_sum = data_kc.groupby(['投资方所在城市','融资方所在城市']).sum().sort_values(by = '投资企业对数',ascending = False)
del kc_sum['年份']
# 汇总“跨城投资”数据
# 查看“同城投资”
tc_sum.iloc[:20]
# 查看“跨城投资”
kc_sum.iloc[:20]
tc_sum.iloc[:20].plot(kind = 'bar',grid = True, figsize = (10,4),color = 'blue',alpha = 0.7)
kc_sum.iloc[:20].plot(kind = 'bar',grid = True, figsize = (10,4),color = 'green',alpha = 0.7)
# 结论1
# ① 从2013-2016的汇总数据来看，投资比数“同城投资”>“跨城投资”
# ② “同城投资”中领头的城市为北上广深及部分二线强城市，其中 深圳>北京>上海>>其他城市
# ③ “跨城投资”中领头的城市仍为北上广深（相互投资），或者北上广深向周边城市投资（城市群）
# 比较一下“同城投资”、“跨城投资”TOP20的数据分布
# 分开比较2013-2016四个年度的数据

def f1(year):
    tc_year = data_tc[data_tc['年份'] == year].sort_values(by = '投资企业对数',ascending = False)
    kc_year = data_kc[data_kc['年份'] == year].sort_values(by = '投资企业对数',ascending = False)
    tc_year.index = tc_year['投资方所在城市']
    kc_year.index = kc_year['投资方所在城市'] + '-' + kc_year['融资方所在城市']
    # 筛选该年的“同城投资”、“跨城投资”
    #print('%i年同城投资TOP20:' % year)
    #print(tc_year.iloc[:20])
    #print('-----')
    #print('%i年跨城投资TOP20:' % year)
    #print(kc_year.iloc[:20])
    #print('-----')
    return(tc_year.iloc[:20],kc_year.iloc[:20])
    # 输出该年“同城投资”、“跨城投资”TOP20 
# 创建函数
    # 绘制图表

fig,axes = plt.subplots(4,2,figsize=(12,15))
plt.subplots_adjust(wspace = 0.1,hspace=0.5)
f1(2013)[0]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'blue',alpha = 0.7,ax = axes[0,0],title = '同城投资 - 2013年',ylim = [0,40000])
f1(2013)[1]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'green',alpha = 0.7,ax = axes[0,1],title = '跨城投资 - 2013年',ylim = [0,3000])
# 2013年
f1(2014)[0]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'blue',alpha = 0.7,ax = axes[1,0],title = '同城投资 - 2014年',ylim = [0,40000])
f1(2014)[1]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'green',alpha = 0.7,ax = axes[1,1],title = '跨城投资 - 2014年',ylim = [0,3000])
# 2014年
f1(2015)[0]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'blue',alpha = 0.7,ax = axes[2,0],title = '同城投资 - 2015年',ylim = [0,40000])
f1(2015)[1]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'green',alpha = 0.7,ax = axes[2,1],title = '跨城投资 - 2015年',ylim = [0,3000])
# 2015年
f1(2016)[0]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'blue',alpha = 0.7,ax = axes[3,0],title = '同城投资 - 2016年',ylim = [0,40000])
f1(2016)[1]['投资企业对数'].plot(kind = 'bar',grid = True, color = 'green',alpha = 0.7,ax = axes[3,1],title = '跨城投资 - 2016年',ylim = [0,3000])
# 2016年
# 结论2
# ① 分开2013-2016年来看，每年“同城投资”、“跨城投资”均呈上升趋势
# ② “同城投资”中，头部城市仍为北上深（没有广州），且随着时间推移，越来越拉开和其他城市的“同城投资”差距（注意这个结论）
# ③ “跨城投资”中，投资关系较强的城市为“北京-上海” > “北京-深圳” > “上海-深圳” → 一线城市之间投资力度较大
# ** 接下来详细挖掘一下“全国跨城市资本流动情况”
# 读取“中国城市代码对照表.xlsx”数据及重新设置kc_sum数据的index

city = pd.read_excel('C:/Users/安东/Desktop/项目12中国城市资本流动问题探索/中国城市代码对照表.xlsx')
kc_sum.reset_index(inplace = True) 
# 结合“中国行政代码对照表.xlsx”数据，给2013-2016年“跨城投资”的汇总数据添加城市的经纬度

kc_data = pd.merge(kc_sum,city[['城市名称','经度','纬度']],left_on ='投资方所在城市',right_on = '城市名称')
kc_data = pd.merge(kc_data,city[['城市名称','经度','纬度']],left_on ='融资方所在城市',right_on = '城市名称')
kc_data = kc_data[['投资方所在城市','融资方所在城市','投资企业对数','经度_x','纬度_x','经度_y','纬度_y']] 
kc_data.columns = ['投资方所在城市','融资方所在城市','投资企业对数','lng_tz','lat_tz','lng_rz','lat_rz']
kc_data.head()
# 导出gephi制图数据

gephi_edge = kc_data[['投资方所在城市','融资方所在城市','投资企业对数']]
gephi_edge.columns = ['source','target','weight']
gephi_edge['weight'] = (gephi_edge['weight'] - gephi_edge['weight'].min())/(gephi_edge['weight'].max() - gephi_edge['weight'].min())
gephi_edge.to_csv('C:/Users/安东/Desktop/gephi_edge.csv',index = False)
# 导出边数据

citys = list(set(gephi_edge['source'].tolist()+gephi_edge['target'].tolist()))
gephi_nodes = pd.DataFrame({'Id':citys})  
# 筛选出所有的城市节点，并生成dataframe
top_node = gephi_edge.sort_values(by = 'weight',ascending = False)
top_node20 = top_node['source'].drop_duplicates().iloc[:20]
top_node20_df = pd.DataFrame({'Id':top_node20, 'Label':top_node20})
# 筛选出投资对数较大，且不重复的前20个城市，并生成dataframe
gephi_nodes = pd.merge(gephi_nodes,top_node20_df,on = 'Id',how = 'left')
# 合并，给点数据增加label字段
gephi_nodes.to_csv('C:/Users/安东/Desktop/gephi_nodes.csv',index = False)
# 导出点数据

print('finished!')
# 导出qgis制图数据

kc_data.to_csv('C:/Users/安东/Desktop/qgisdata.csv',index = False)
print('finished!')
# 结论3
# ① 通过“全国跨城市资本流动OD图”可以明显看到
# ** 三个亮点密集的区域：长三角城市群、珠三角城市群、北京-天津城市群
# ** 这三个城市群与成都-重庆西部城市群构成了一个钻石形状
# ** 在钻石之外，仅有星星点点的东北和西部的几个亮点游离；
# ** 而这颗大钻石内的资本流动，占据了全国资本流动的90%以上！！
# ② 通过“城市关系图”可以发现：
# ** 城际投资的全国城市拓扑关系 → 以“北上深”为中心的城市网络
# 近四年对外控股型投资笔数最多的10个城市是哪些？

result1 = kc_sum[['投资方所在城市','投资企业对数']].groupby('投资方所在城市').sum().sort_values(by = '投资企业对数',ascending = False).iloc[:10]
# 近四年吸引对外控股型投资笔数最多的10个城市又是哪些？
result2 = kc_sum[['融资方所在城市','投资企业对数']].groupby('融资方所在城市').sum().sort_values(by = '投资企业对数',ascending = False).iloc[:10]
result1.plot(kind = 'bar',grid = True, figsize = (10,4),color = 'red',alpha = 0.7, rot = 0)
result2.plot(kind = 'bar',grid = True, figsize = (10,4),color = 'black',alpha = 0.7, rot = 0)
# 结论4
# ① 通过“对外控股型投资笔数-城市排名TOP10”可以看出
# ** 北京、上海、深圳毫无悬念地包揽了前三名，且在量级上远远超过了其他城市 → 北上深在一定程度上控制着全国的资金流向和经济命脉
# ** 杭州 → 第四名，表现最为亮眼的省会城市，崛起的新一线城市
# ** 广州 → 第五名，江湖人称“北上广”三兄弟的广州，在对外投资的控制力上已经与另两位兄弟渐行渐远了
# ** 前10名中有5名都是长三角区域的城市，可以看到长三角地区资本的活跃程度
# ② 通过“吸引对外控股型投资笔数-城市排名TOP10”可以看出
# ** 吸引外来控股型投资笔数最多的前三名的仍然是北上深
# ** 在外来资本流入城市的榜单中，嘉兴挤掉了南京,进入前十名 → 相比资本对外输出，嘉兴是一个更受资本青睐的城市
# 从2013年到2016年，资本流动两大阵营的变化趋势：“北上深阵营”、“本地化阵营”
# ** “北上深阵营”：最大的外来投资方为北上深之一的城市
# ** “本地化阵营”：这里简化计算，将非“北上深阵营”都划入“本地化阵营”

def f2(year):
    kc_datai = data_kc[data_kc['年份']==year]
    x = kc_datai[['融资方所在城市','投资企业对数']].groupby('融资方所在城市').max().reset_index()
    city_tz_max = pd.merge(kc_datai,x,on = ['融资方所在城市','投资企业对数'],how = 'right')
    # 数据整理 → 得到融资城市的最大外来投资对应的“投资方城市”
    city_tz_max['阵营'] = 0
    city_tz_max['阵营'][(city_tz_max['投资方所在城市'] == '北京') |
                        (city_tz_max['投资方所在城市'] == '上海') | 
                        (city_tz_max['投资方所在城市'] == '深圳') ] = 1
    # 划分“北上深阵营”、“本地化阵营”
    city_tz_max = pd.merge(city_tz_max,city[['城市名称','经度','纬度']],left_on ='融资方所在城市',right_on = '城市名称')
    city_tz_max = city_tz_max[['投资方所在城市','融资方所在城市','投资企业对数','阵营','经度','纬度']] 
    # 添加融资方所在城市经纬度
    dici = {}
    dici['北上深阵营城市数据量'] = city_tz_max['阵营'].value_counts().iloc[1]
    dici['本地化阵营城市数据量'] = city_tz_max['阵营'].value_counts().iloc[0]
    # 计算“北上深阵营”、“本地化阵营”的城市数量，并放入一个字典
    return(city_tz_max,dici)
# 创建函数

zy_year = pd.DataFrame([f2(2013)[1],f2(2014)[1],f2(2015)[1],f2(2016)[1]],index = ['2013年','2014年','2015年','2016年'])
zy_year['北上深阵营占比'] = zy_year['北上深阵营城市数据量']/(zy_year['北上深阵营城市数据量'] + zy_year['本地化阵营城市数据量'])
zy_year[['北上深阵营城市数据量','本地化阵营城市数据量']].plot(kind='bar',grid = True,colormap='Blues_r',rot = 0,
                                                              stacked=True,figsize = (10,4),ylim = [0,400])
# 绘制堆叠图查看占比变化趋势
zy_year
# 数据导出csv，qgis绘图

f2(2013)[0].to_csv('C:/Users/安东/Desktop/year2013.csv',index = False)
f2(2014)[0].to_csv('C:/Users/安东/Desktop/year2014.csv',index = False)
f2(2015)[0].to_csv('C:/Users/安东/Desktop/year2015.csv',index = False)
f2(2016)[0].to_csv('C:/Users/安东/Desktop/year2016.csv',index = False)
print('finished!')
# 结论5
# “北上深阵营”高歌猛进，“本地化阵营”节节败退
# ① 2013年，“北上深阵营”的地盘仅仅局限于国内少数相对发达地区，以及各省省会城市
# ② 随着时间的推移，“北上深阵营”的势力范围逐步扩大，东北和内蒙的大部分地区纳入了“北上深阵营”
# ③ 越来越多的中小型城市也逐渐成为“北上深阵营”的一员
# ④ 2014年，90%的控股型城际投资去向了99个城市，而到了2017年，90%的城际投资只去向了60个城市
# → “北上深”越来越强大的资本力量，正在逐步地穿透中国经济的底层——三四线城市

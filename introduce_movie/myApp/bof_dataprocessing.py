#基于项目的协同过滤
#基于项目
#导入第三方模块pandas和numpy
import pandas as pd
import numpy as np
from pandas import DataFrame
import pymysql

# 调用movlens中的ratings数据集切割后转化为二维矩阵进行展示
#数据库movielens中电影记录条数：3883
#数据库movielens中用户记录条数：6040
#数据库movielens中电影记录条数：1000209
#rating_data为矩阵类型
# rating_name = ['user_id','movie_id','rating','timestamp']
# rating_data = pd.read_table('D:/graduate project/MovieLens_data/ml-1m/ratings.dat',sep='::',header=None,names=rating_name)
#conn = MySQLdb.connect(host="47.95.198.185",user="root",passwd="111111",db='movielens',port = 3306,charset="utf8")
conn = pymysql.connect(host="localhost",user="root",db='movielens',port = 3306,charset="utf8")
sql = "select * from ratings"
rating_data= pd.read_sql(sql,conn)
#调用movlens中的movies数据集切割后转化为二维矩阵进行展示
#删除二维矩阵中时间戳对应的列
del rating_data['timestamp']
del rating_data['rating_id']
array_data_rate = rating_data.values
#把数据转换成字典的形式,形式如：{用户ID：{电影ID：评分，电影ID：评分}}
data_dict_rate={}
# array_data_rate[:1000,:]表示前1000个电影评分信息
for row in array_data_rate[:1000,:]:
    data_dict_rate.setdefault(row[0],{})
    data_dict_rate[row[0]][row[1]]=float(row[2])
# 读入数据，形成用户-电影评分矩阵， 每一列代表一个电影的评分，矩阵中的数据为用户（横坐标）对特定电影（纵坐标）的评分数据
#DataFrame提供的是一个类似表的结构，由多个Series组成，而Series在DataFrame中叫columns
datarate = DataFrame(data_dict_rate)
# 清理和转换数据
#0:代表未被评分
datarate = datarate.fillna(0)
# mdata：用户电影评分矩阵
# mcor：电影相关系数矩阵
# movie_id：电影ID
# user_id：用户ID
#转置矩阵ndarray，矩阵中的数据为用户（纵坐标）对特定电影（横坐标）的评分数据
mdatas = datarate.T
#madatas是一个44*1728矩阵
#madatas是一个44*500矩阵
# 计算不同电影相似，数据归一化到[0,1]
#不省略中间部分，可以通过set_printoptions来强制NumPy打印所有数据。设置precision来控制小数点后面最多显示的位数
np.set_printoptions(3)
#mcors:电影的相关系数矩阵
#使用numpy库，可以实现相关系数的计算,使用np.corrcoef(a)可计算行与行之间的相关系数，np.corrcoef(a,rowvar=0)用于计算各列之间的相关系数，输出为相关系数矩阵。
mcors = np.corrcoef(mdatas,rowvar=False)
#应用公式0.5*value+0.5可以将相关系数矩阵的值域由[-1,1]映射为[0,1]。
mcors = 0.5 + mcors * 0.5
mcors = pd.DataFrame(mcors, columns=mdatas.columns, index=mdatas.columns)
# 计算每个用户的每一项的评分，预测未评分电影的评分
#根据电影-电影相关度矩阵，以及用户已有的评分，通过加权平均计算用户未评分电影的预估评分。例如用户对A电影评3分、
# B电影评4分、C电影未评分，而C电影与A电影、B电影的相关度分别为0.5和0.7，则C电影的预估评分为(0.5*3+0.7*4)/(0.5+0.7)。
def cal_score(mdatas, mcors, movie_id, users_id,user_id):
    sum_score = 0
    sum_sims = 0
    #如果用户未评分则预计估分
    #python pandas判断缺失值一般采用 isnull()，然而生成的却是所有数据的true／false矩阵
    if pd.isnull(mdatas[movie_id][user_id]) or mdatas[movie_id][user_id] == 0:
       if users_id == user_id:
            for mitem in mdatas.columns:
                if mdatas[mitem][user_id] == 0:
                    continue
                else:
                    sum_score += mdatas[mitem][user_id] * mcors[movie_id][mitem]
                    sum_sims += mcors[movie_id][mitem]
            score = sum_score / sum_sims
       else:
           score = mdatas[movie_id][user_id]
    else:
        score = mdatas[movie_id][user_id]
    return score
# 计算评分矩阵
# mdatas：用户电影矩阵
# mcors：电影相关系数矩阵
# score_matrix：为不同的用户电影评分矩阵,包括用户未评分的电影的预测值
def cal_matscore(mdatas, mcors,user_id):
    #把评分矩阵的所有值清零,生成一个N长度的一维全零ndarray
    score_matrix = np.zeros(mdatas.shape)
    #index：行索引；columns：列索引
    score_matrix = pd.DataFrame(score_matrix, columns=mdatas.columns, index=mdatas.index)
    for mitem in score_matrix.columns:
        for muser in score_matrix.index:
            score_matrix[mitem][muser] = cal_score(mdatas, mcors, mitem, muser,user_id)
    return score_matrix
# 给出建议：取决于得分矩阵
# mdatas：用户电影矩阵
# score_matrix：针对不同用户的电影评分矩阵
#user_id ：用户ID
# n：建议数量
def recommend(mdatas, score_matrix, user, n):
    #选取某个用户的电影评分
    #ix :通过行标签或者行号索引行数据, user_ratings得到电影的ID和评分值
    user_ratings = mdatas.ix[user]
    #print(user_ratings)
    #选取未进行评分的电影即评分值为0的电影
    not_rated_score = user_ratings[user_ratings == 0]
    #print(not_rated_score)
    #获取未评分电影的预测评分值，并以字典形式：{电影id:电影评分预测值}存放
    recom_score = {}
    for movie in not_rated_score.index:
        recom_score[movie] = score_matrix[movie][user]
    #Series可以运用ndarray或字典的几乎所有索引操作和函数，融合了字典和ndarray的优点
    recom_score = pd.Series(recom_score)
    #对于每一位用户，提取其未评分的电影并按预估评分值倒序排列，提取前n位的电影作为推荐电影。
    recom_score= recom_score.sort_values(ascending=False)
    #返回推荐的电影
    #输出电影的id号
    #print(recom_score.index[0])
    #输出电影的评分值
    #print(recom_score.values[0])
    return recom_score[:n]
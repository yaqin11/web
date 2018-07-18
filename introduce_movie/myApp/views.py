from django.shortcuts import render
from myApp.models import IntroInf,Movies,Ratings,Users
from myApp.bof_dataprocessing import cal_matscore,mdatas,mcors,recommend
from myApp.bou_dataprocessing import user_cal_matscore,ucors,user_recommend


# Create your views here.
def index(request):
    user_id = request.session.get('user_id', default="未登录")
    # 生成不同的用户电影评分矩阵, 包括用户未评分的电影的预测值
    return render(request,'myApp/index.html',{"user_id":user_id})

#首页
def main(request):
    user_id = request.session.get("user_id", default="未登录")
    return render(request, 'myApp/main.html', {"user_id": user_id})
#详情
def detail(request):
    user_id = request.session.get("user_id", default="未登录")
    if user_id != "未登录":
        user = Users.objects.filter(user_id = user_id).first()
        return render(request, 'myApp/detail.html', {"user": user})
    else:
        return render(request, 'myApp/login.html')
#登录
def login(request):
    if request.method == "GET":
        return render(request,'myApp/login.html')
    else:
        user_id = request.POST.get('user_id')
        #将user_id使用session存储
        # request.session['user_id'] = user_id
        # score_matrix：针对不同用户的电影评分矩阵
        score_matrix = cal_matscore(mdatas, mcors, int(user_id))
        # array_data_movie为[movie_id,title]二维数组
        recommend_result = recommend(mdatas, score_matrix, int(user_id), 6)
        # 将基于项目的电影推荐结果存入数据库中
        # introinf = IntroInf.objects.create(1,int(recommend_result.index[0]),recommend_result.values[0])
        introinf = IntroInf()
        introinf.introinf_id = 1
        introinf.movie_id = int(recommend_result.index[0])
        introinf.prediction_score = recommend_result.values[0]
        introinf.save()
        # introinf = IntroInf.objects.create(2, int(recommend_result.index[1]), recommend_result.values[1])
        introinf.introinf_id = 2
        introinf.movie_id = int(recommend_result.index[1])
        introinf.prediction_score = recommend_result.values[1]
        introinf.save()
        # introinf = IntroInf.objects.create(3, int(recommend_result.index[2]), recommend_result.values[2])
        introinf.introinf_id = 3
        introinf.movie_id = int(recommend_result.index[2])
        introinf.prediction_score = recommend_result.values[2]
        introinf.save()
        # introinf = IntroInf.objects.create(4, int(recommend_result.index[3]), recommend_result.values[3])
        introinf.introinf_id = 4
        introinf.movie_id = int(recommend_result.index[3])
        introinf.prediction_score = recommend_result.values[3]
        introinf.save()
        # introinf = IntroInf.objects.create(5, int(recommend_result.index[4]), recommend_result.values[4])
        introinf.introinf_id = 5
        introinf.movie_id = int(recommend_result.index[4])
        introinf.prediction_score = recommend_result.values[4]
        introinf.save()
        # introinf = IntroInf.objects.create(6, int(recommend_result.index[5]), recommend_result.values[5])
        introinf.introinf_id = 6
        introinf.movie_id = int(recommend_result.index[5])
        introinf.prediction_score = recommend_result.values[5]
        introinf.save()
        # score_matrix：针对不同用户的电影评分矩阵
        score_matrix = user_cal_matscore(mdatas, ucors,)
        # array_data_movie为[movie_id,title]二维数组
        user_recommend_result = user_recommend(mdatas, score_matrix, int(user_id), 6)
        # 将基于用户的电影推荐结果存入数据库中
        introinf = IntroInf()
        introinf.introinf_id = 7
        introinf.movie_id = int(user_recommend_result.index[0])
        introinf.prediction_score = user_recommend_result.values[0]
        introinf.save()
        introinf.introinf_id = 8
        introinf.movie_id = int(user_recommend_result.index[1])
        introinf.prediction_score = user_recommend_result.values[1]
        introinf.save()
        introinf.introinf_id = 9
        introinf.movie_id = int(user_recommend_result.index[2])
        introinf.prediction_score = user_recommend_result.values[2]
        introinf.save()
        introinf.introinf_id = 10
        introinf.movie_id = int(user_recommend_result.index[3])
        introinf.prediction_score = user_recommend_result.values[3]
        introinf.save()
        passwd  = request.POST.get("passwd")
        if Users.objects.get(pk = user_id).user_id:
            #登录验证成功
            # 将user_id使用session存储
            request.session["user_id"] = user_id
            return render(request, 'myApp/main.html', {"user_id": user_id})
        else:
            return render(request,'myApp/login.html')

#猜您喜欢
def bopintroduce(request):
    #得到用户的id号
    user_id = request.session.get('user_id', default="未登录")
    if user_id == "未登录":
        return render(request,'myApp/index.html',{"user_id": user_id})
    else:
        # 电影的推荐信息包括电影id，电影名，电影类型，预测电影评分
        intro_inf1 = Movies.objects.filter(movie_id = IntroInf.objects.get(pk=1).movie_id).first()
        intro_inf2 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=2).movie_id).first()
        intro_inf3 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=3).movie_id).first()
        intro_inf4 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=4).movie_id).first()
        intro_inf5 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=5).movie_id).first()
        intro_inf6 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=6).movie_id).first()

           # 6040名用户中对某个推荐电影进行了评分的人数
           # 统计对推荐电影评分数据条数
        ratecount1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=1).movie_id).count()
        ratecount2 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=2).movie_id).count()
        ratecount3 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=3).movie_id).count()
        ratecount4 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=4).movie_id).count()
        ratecount5 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=5).movie_id).count()
        ratecount6 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=6).movie_id).count()

       # 统计用户对电影的评分在4分以上的用户数量
        ratecount1_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=1).movie_id,rating__gte = 4).count()
        ratecount2_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=2).movie_id, rating__gte=4).count()
        ratecount3_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=3).movie_id, rating__gte=4).count()
        ratecount4_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=4).movie_id, rating__gte=4).count()
        ratecount5_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=5).movie_id, rating__gte=4).count()
        ratecount6_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=6).movie_id, rating__gte=4).count()

        # 喜欢某推荐电影的用户还观看了评分在4分以上的四部电影（具有随机性）
        import random
        #定义随机挑选的用户信息列表
        user_inf1 = []
        #喜欢第一部推荐电影的用户喜欢的电影
        #选择所有给第一部推荐电影评过分，并且评分值大于等于4（五分制）的评分信息
        rinfs = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk =1).movie_id,rating__gte=4)
        #随机挑选出两个喜欢该推荐电影的用户
        for rinf in rinfs:
               user_inf1.append(rinf.user_id)
        user_id1 = user_inf1[random.randint(0,len(user_inf1)-1)]
        user_id2 = user_inf1[random.randint(0, len(user_inf1)-1)]
        #选择这2个用户分别喜欢的一部电影
        user_movie01 = Ratings.objects.filter(user_id = user_id1).first()
        user_movie02 = Ratings.objects.filter(user_id=user_id2).last()
        #得到每个电影的详细信息
        umovie01_1 = Movies.objects.filter(movie_id = user_movie01.movie_id).first()
        umovie02_1 = Movies.objects.filter(movie_id=user_movie02.movie_id).first()

        # 喜欢第二部推荐电影的用户喜欢的电影
        # 定义随机挑选的用户信息列表
        user_inf2 = []
        # 选择所有给第二部推荐电影评过分，并且评分值大于等于4（五分制）的评分信息
        rinfs = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=2).movie_id, rating__gte=4)
        # 随机挑选出2个喜欢该推荐电影的用户
        for rinf in rinfs:
            user_inf2.append(rinf.user_id)
        user_id1 = user_inf2[random.randint(0, len(user_inf2)-1)]
        user_id2 = user_inf2[random.randint(0, len(user_inf2)-1)]
        # 选择这2个用户分别喜欢的一部电影
        user_movie01 = Ratings.objects.filter(user_id=user_id1).first()
        user_movie02 = Ratings.objects.filter(user_id=user_id2).last()
        # 得到每个电影的详细信息
        umovie01_2 = Movies.objects.filter(movie_id=user_movie01.movie_id).first()
        umovie02_2 = Movies.objects.filter(movie_id=user_movie02.movie_id).first()

        # 喜欢第三部推荐电影的用户喜欢的电影
        # 定义随机挑选的用户信息列表
        user_inf3 = []
        # 选择所有给第三部推荐电影评过分，并且评分值大于等于4（五分制）的评分信息
        rinfs = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=3).movie_id, rating__gte=4)
        # 随机挑选出2个喜欢该推荐电影的用户
        for rinf in rinfs:
            user_inf3.append(rinf.user_id)
        user_id1 = user_inf3[random.randint(0, len(user_inf3)-1)]
        user_id2 = user_inf3[random.randint(0, len(user_inf3) - 1)]
        # 选择这2个用户分别喜欢的一部电影
        user_movie01 = Ratings.objects.filter(user_id=user_id1).first()
        user_movie02 = Ratings.objects.filter(user_id=user_id2).last()
        # 得到每个电影的详细信息
        umovie01_3 = Movies.objects.filter(movie_id=user_movie01.movie_id).first()
        umovie02_3 = Movies.objects.filter(movie_id=user_movie02.movie_id).first()

        # 喜欢第四部推荐电影的用户喜欢的电影
        # 定义随机挑选的用户信息列表
        user_inf4 = []
        # 选择所有给第2部推荐电影评过分，并且评分值大于等于4（五分制）的评分信息
        rinfs = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=4).movie_id, rating__gte=4)
        # 随机挑选出2个喜欢该推荐电影的用户
        for rinf in rinfs:
            user_inf4.append(rinf.user_id)
        user_id1 = user_inf4[random.randint(0, len(user_inf4)-1)]
        user_id2 = user_inf4[random.randint(0, len(user_inf4)-1)]
        # 选择这2个用户分别喜欢的一部电影
        user_movie01 = Ratings.objects.filter(user_id=user_id1).first()
        user_movie02 = Ratings.objects.filter(user_id=user_id2).last()
        # 得到每个电影的详细信息
        umovie01_4 = Movies.objects.filter(movie_id=user_movie01.movie_id).first()
        umovie02_4 = Movies.objects.filter(movie_id=user_movie02.movie_id).first()
        # 喜欢第五部推荐电影的用户喜欢的电影
        # 定义随机挑选的用户信息列表
        user_inf5 = []
        # 选择所有给第五部推荐电影评过分，并且评分值大于等于4（五分制）的评分信息
        rinfs = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=5).movie_id, rating__gte=4)
        # 随机挑选出2个喜欢该推荐电影的用户
        for rinf in rinfs:
            user_inf5.append(rinf.user_id)
        user_id1 = user_inf5[random.randint(0, len(user_inf5)-1)]
        user_id2 = user_inf5[random.randint(0, len(user_inf5)-1)]
        # 选择这2个用户分别喜欢的一部电影
        user_movie01 = Ratings.objects.filter(user_id=user_id1).first()
        user_movie02 = Ratings.objects.filter(user_id=user_id2).last()
        # 得到每个电影的详细信息
        umovie01_5 = Movies.objects.filter(movie_id=user_movie01.movie_id).first()
        umovie02_5 = Movies.objects.filter(movie_id=user_movie02.movie_id).first()

        # 喜欢第六部推荐电影的用户喜欢的电影
        # 定义随机挑选的用户信息列表
        user_inf6 = []
        # 选择所有给第六部推荐电影评过分，并且评分值大于等于4（五分制）的评分信息
        rinfs = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=6).movie_id, rating__gte=4)
        # 随机挑选出2个喜欢该推荐电影的用户
        for rinf in rinfs:
            user_inf6.append(rinf.user_id)
        user_id1 = user_inf6[random.randint(0, len(user_inf6)-1)]
        user_id2 = user_inf6[random.randint(0, len(user_inf6)-1)]
        # 选择这2个用户分别喜欢的一部电影
        user_movie01 = Ratings.objects.filter(user_id=user_id1).first()
        user_movie02 = Ratings.objects.filter(user_id=user_id2).last()
        # 得到每个电影的详细信息
        umovie01_6 = Movies.objects.filter(movie_id=user_movie01.movie_id).first()
        umovie02_6 = Movies.objects.filter(movie_id=user_movie02.movie_id).first()
        return render(request,'myApp/bop.html',{"prediction_score1":IntroInf.objects.get(pk = 1).prediction_score,"intro_inf1":intro_inf1,"ratecount1":ratecount1,"ratecount1_1":ratecount1_1,
                                               "prediction_score2": IntroInf.objects.get(pk = 2).prediction_score,"intro_inf2": intro_inf2, "ratecount2": ratecount2,"ratecount2_1": ratecount2_1,
                                               "prediction_score3": IntroInf.objects.get(pk = 3).prediction_score,
                                               "intro_inf3": intro_inf3, "ratecount3": ratecount3,
                                               "ratecount3_1": ratecount3_1,
                                               "prediction_score4": IntroInf.objects.get(pk = 4).prediction_score,
                                               "intro_inf4": intro_inf4, "ratecount4": ratecount4,
                                               "ratecount4_1": ratecount4_1,
                                               "prediction_score5": IntroInf.objects.get(pk = 5).prediction_score,
                                               "intro_inf5": intro_inf5, "ratecount5": ratecount5,
                                               "ratecount5_1": ratecount5_1,
                                               "prediction_score6": IntroInf.objects.get(pk = 6).prediction_score,
                                               "intro_inf6": intro_inf6, "ratecount6": ratecount6,
                                               "ratecount6_1": ratecount6_1,
                                                "umovie01_1":umovie01_1, "umovie02_1":umovie02_1,
                                                "umovie01_2": umovie01_2, "umovie02_2": umovie02_2,

                                                "umovie01_3": umovie01_3, "umovie02_3": umovie02_3,

                                                "umovie01_4": umovie01_4, "umovie02_4": umovie02_4,

                                                "umovie01_5": umovie01_5, "umovie02_5": umovie02_5,

                                                "umovie01_6": umovie01_6, "umovie02_6": umovie02_6,"user_id":user_id})
#其他人也喜欢
def bouintroduce(request):
        # 得到用户的id号
        user_id = request.session.get('user_id', default="未登录")
        if user_id == "未登录":
            return render(request, 'myApp/index.html', {"user_id": user_id})
        else:
            # 电影的推荐信息包括电影id，电影名，电影类型，预测电影评分
            intro_inf1 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=7).movie_id).first()
            intro_inf2 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=8).movie_id).first()
            intro_inf3 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=9).movie_id).first()
            intro_inf4 = Movies.objects.filter(movie_id=IntroInf.objects.get(pk=10).movie_id).first()

            # 6040名用户中对某个推荐电影进行了评分的人数
            # 统计对推荐电影评分数据条数
            ratecount1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=7).movie_id).count()
            ratecount2 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=8).movie_id).count()
            ratecount3 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=9).movie_id).count()
            ratecount4 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=10).movie_id).count()
            # 统计用户对电影的评分在4分以上的用户数量
            ratecount1_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=7).movie_id, rating__gte=4).count()
            ratecount2_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=8).movie_id, rating__gte=4).count()
            ratecount3_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=9).movie_id, rating__gte=4).count()
            ratecount4_1 = Ratings.objects.filter(movie_id=IntroInf.objects.get(pk=10).movie_id, rating__gte=4).count()

            #喜欢某推荐电影的用户还观看了评分在4分以上电影名称

            return render(request, 'myApp/uop.html',
                          {"prediction_score1":IntroInf.objects.get(pk = 7).prediction_score, "intro_inf1": intro_inf1,
                           "ratecount1": ratecount1, "ratecount1_1": ratecount1_1,
                           "prediction_score2": IntroInf.objects.get(pk = 8).prediction_score, "intro_inf2": intro_inf2,
                           "ratecount2": ratecount2, "ratecount2_1": ratecount2_1,
                           "prediction_score3":IntroInf.objects.get(pk = 9).prediction_score,
                           "intro_inf3": intro_inf3, "ratecount3": ratecount3,
                           "ratecount3_1": ratecount3_1,
                           "prediction_score4": IntroInf.objects.get(pk = 10).prediction_score,
                           "intro_inf4": intro_inf4, "ratecount4": ratecount4,
                           "ratecount4_1": ratecount4_1,
                           "prediction_score5": IntroInf.objects.get(pk = 1).prediction_score,
                           "user_id":user_id
                           })


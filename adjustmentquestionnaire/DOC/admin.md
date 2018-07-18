#管理员接口

## 查看问卷

method：GET

api:`/api/v1/admin_questionnaire`

body:
- page:第几页
- limit：每页数量
- state：状态
- id:问卷id，获取单个问卷时使用
- with_detail:是否返回详细信息

response

```json
{
  "page":100,//总页数
  "count":8888,//问卷总数
  "objs":[//问卷列表
  {
    "id":1,//问卷id,
    "title":"测试问卷",//问卷标题
    "free_quantity":100,//问卷数量
    "expire_date":"2018-12-10",//问卷截止日期
    "create_date":"2018-3-10",//问卷创建时间
    "status":0,//问卷状态：0-草稿，1-待审核，2-审核失败，3-审核通过，4-已发布
    "customer":{
        "id":1,//客户id
        "name":"小明"//客户名称
    },
      //加入with_detail参数为true，那么包含以下信息
    "question":[
        {
          "id":1,//问题id
          "title":"问题1", //问题标题
          "category":"radio",//问题类型，radio单选，CheckBox双选
          "item":[
            {
              "id":1,//选项id
              "content":"选项1"//选项内容
            }
          ]
        }
    ],
      "comments":[
          {//批注信息
              "id":1,//批注id
              "create_date":"2018-7-5",//批注日期
              "content":"测试批注不通过"//批注内容
           }
       ]
    }
  ]
}
```

##审核问卷
method：PUT

api:`/api/v1/questionnaire_comment`

body:
- **questionnaire_id**:问卷id
- **is_agree**:是否同意
- comment：批注信息

response：
```json
{
"msg":"提交成功"
}
```


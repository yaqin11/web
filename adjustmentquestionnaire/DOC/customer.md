#客户接口
##问卷接口

##创建问卷
    method：PUT
    
api: `/api/v1/customer_questionnaire`

body:
- **title**:问卷标题
- **deadline**:截止时间，格式是：YYY-MM-DD，例如2010-10-20
- **quantity**:数量
response:
```json
{
"id":"1" //新建的问卷
}
```

## 更新问卷

method：POST
api:`/api/v1/customer_questionnaire`

body:
- **id**:问卷id
- **title**:问卷标题
- **expire**:截止时间，格式是：YYY-MM-DD，例如2010-10-20
- **quantity**:数量
response:
```
json
{
"msg":"更新成功"
}
```

##删除问卷
method：DELETE
api: `/api/v1/customer_questionnaire`

body:

- **ids**:删除的问卷id列表，例如：{"ids":{1,2,3,4}}

response:
```json
{
    "deleted_ids":"[2,4]"//被删除的问卷id列表
}
```
##获取问卷

method:GET

api: `/api/v1/customer_questionnaire`

param:
- page:第几页数据，默认1
- limit：每页数据，默认10
- status：状态，默认草稿
- with_detail:是否需要详情，默认False
- id:问卷id，默认空
response:
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
##问题接口
###创建问题

method：PUT

api:`/api/v1/customer_question`

body:
- question_id:问卷id
- title:问题
- category：radio或者Checkbox
- items:问题选项，例如：['选项1','选项2','选项3'..]

例如：
```json
{
 "id":1 //新建的问题id
}
```

###更新问题

method：POST

api:`/api/v1/customer_question`

body:
- **id**:问卷id
- **title**：问题
- **category**:radio或者checkbox
- **items**:问题选项，例如：['选项','选项2'..]

response:
```json
{
  "msg":"更新成功"
}
```

###删除问题

method：DELETE

api:`/api/v1/customer_question`



## 问卷状态

### 修改问卷状态

method: POST

api: `/api/v1/questionnaire_state`

body:
- **id**: 问卷id
- **state**: 问卷状态

>  本接口用于:
> - 问卷提交审核:将问卷状态改为1,
> - 问卷发布:将问卷状态改为4

response:
```json
{
    "msg":"修改成功"
}
```
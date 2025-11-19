  * user
    * get心跳
    * get获取当前 Token 的用户详情
  * search
    * get通用搜索
  * group
    * get获取用户的团队
    * get获取团队的成员
    * put变更成员
    * del删除成员
  * doc
    * get获取知识库的文档列表
    * post创建文档
    * get获取文档详情
    * put更新文档
    * del删除文档
    * get获取知识库的文档列表
    * post创建文档
    * get获取文档详情
    * put更新文档
    * del删除文档
    * get获取文档历史版本列表
    * get获取文档历史版本详情
    * get获取目录
    * put更新目录
    * get获取目录
    * put更新目录
  * repo
    * get获取知识库列表
    * post创建知识库
    * get获取知识库列表
    * post创建知识库
    * get获取知识库详情
    * put更新知识库
    * del删除知识库
    * get获取知识库详情
    * put更新知识库
    * del删除知识库
  * statistic
    * get团队.汇总统计数据
    * get团队.成员统计数据
    * get团队.知识库统计数据
    * get团队.文档统计数据



[API docs by Redocly](https://redocly.com/redoc/)

# 语雀 OpenAPI (2.0.1)

Download OpenAPI specification:Download

License: Apache-2.0

## user

user

## 心跳

心跳 GET /api/v2/hello

##### Authorizations:

_authToken_

### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/hello

线上访问地址

https://www.yuque.com/api/v2/hello

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "message": "string"

}


}`

## 获取当前 Token 的用户详情

获取当前 Token 的用户详情 GET /api/v2/user

##### Authorizations:

_authToken_

### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/user

线上访问地址

https://www.yuque.com/api/v2/user

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "login": "string",

    * "name": "string",

    * "avatar_url": "string",

    * "books_count": 0,

    * "public_books_count": 0,

    * "followers_count": 0,

    * "following_count": 0,

    * "public": 0,

    * "description": "string",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z"

}


}`

## search

search

## 通用搜索

通用搜索 GET /api/v2/search

  * 支持分页, PageSize 固定为 20



##### Authorizations:

_authToken_

##### query Parameters

qrequired| string <= 200 characters 搜索关键词  
---|---  
typerequired| string Enum: "doc" "repo" 搜索类型 (doc:文档, repo:知识库)  
scope| string <= 400 characters 搜索范围, 不填默认为搜索当前用户/团队 [例子]
    
    
    - 假设:
      - 团队 URL = https://yuque_domain/group_a
      - 知识库 URL = https://yuque_domain/group_a/book_x
    - 则:
      - 搜索团队里的文档: { type: 'doc', scope: 'group_a' }
      - 搜索团队里的知识库: { type: 'repo', scope: 'group_a' }
      - 搜索知识库里的文档: { type: 'doc', scope: 'group_a/book_x' }
      
  
page| integer [ 1 .. 100 ] 页码 [分页参数]  
offset| integer [ 1 .. 100 ] Deprecated 页码, 非偏移量 [分页参数]  
creatorId| integer Deprecated 仅搜索指定作者 ID [筛选条件]  
creator| string 仅搜索指定作者 login [筛选条件]  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/search

线上访问地址

https://www.yuque.com/api/v2/search

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "meta": {
    * "total": 0,

    * "pageNo": 0,

    * "pageSize": 0

},

  * "data": [
    * {
      * "id": 0,

      * "type": "doc",

      * "title": "string",

      * "summary": "string",

      * "url": "string",

      * "info": "string",

      * "target": {
        * "id": 0,

        * "type": "Doc",

        * "slug": "string",

        * "title": "string",

        * "description": "string",

        * "cover": "string",

        * "user_id": 0,

        * "book_id": 0,

        * "last_editor_id": 0,

        * "public": 0,

        * "status": "string",

        * "likes_count": 0,

        * "read_count": 0,

        * "hits": 0,

        * "comments_count": 0,

        * "word_count": 0,

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z",

        * "content_updated_at": "2019-08-24T14:15:22Z",

        * "published_at": "2019-08-24T14:15:22Z",

        * "first_published_at": "2019-08-24T14:15:22Z",

        * "book": {
          * "id": 0,

          * "type": "string",

          * "slug": "string",

          * "name": "string",

          * "user_id": 0,

          * "description": "string",

          * "creator_id": 0,

          * "public": 0,

          * "items_count": 0,

          * "likes_count": 0,

          * "watches_count": 0,

          * "content_updated_at": "2019-08-24T14:15:22Z",

          * "created_at": "2019-08-24T14:15:22Z",

          * "updated_at": "2019-08-24T14:15:22Z",

          * "user": {
            * "id": 0,

            * "type": "string",

            * "login": "string",

            * "name": "string",

            * "avatar_url": "string",

            * "books_count": 0,

            * "public_books_count": 0,

            * "followers_count": 0,

            * "following_count": 0,

            * "public": 0,

            * "description": "string",

            * "created_at": "2019-08-24T14:15:22Z",

            * "updated_at": "2019-08-24T14:15:22Z"

},

          * "namespace": "string"

},

        * "user": {
          * "id": 0,

          * "type": "string",

          * "login": "string",

          * "name": "string",

          * "avatar_url": "string",

          * "books_count": 0,

          * "public_books_count": 0,

          * "followers_count": 0,

          * "following_count": 0,

          * "public": 0,

          * "description": "string",

          * "created_at": "2019-08-24T14:15:22Z",

          * "updated_at": "2019-08-24T14:15:22Z"

},

        * "last_editor": {
          * "id": 0,

          * "type": "string",

          * "login": "string",

          * "name": "string",

          * "avatar_url": "string",

          * "books_count": 0,

          * "public_books_count": 0,

          * "followers_count": 0,

          * "following_count": 0,

          * "public": 0,

          * "description": "string",

          * "created_at": "2019-08-24T14:15:22Z",

          * "updated_at": "2019-08-24T14:15:22Z"

},

        * "latest_version_id": 0,

        * "tags": {
          * "id": 0,

          * "title": "string",

          * "doc_id": 0,

          * "book_id": 0,

          * "user_id": 0,

          * "created_at": "2019-08-24T14:15:22Z",

          * "updated_at": "2019-08-24T14:15:22Z"

}

}

}

]


}`

## group

group

## 获取用户的团队

获取用户的团队 GET /api/v2/users/:id/groups

  * 支持分页, PageSize 固定为 100



##### Authorizations:

_authToken_

##### path Parameters

idrequired| string 用户 login 或 ID  
---|---  
  
##### query Parameters

role| integer Enum: 0 1 角色 [过滤条件] (0:管理员, 1:成员)  
---|---  
offset| integer Default: 0 偏移量 [分页条件]  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/users/{id}/groups

线上访问地址

https://www.yuque.com/api/v2/users/{id}/groups

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "login": "string",

    * "name": "string",

    * "avatar_url": "string",

    * "books_count": 0,

    * "public_books_count": 0,

    * "members_count": 0,

    * "public": 0,

    * "description": "string",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z"

}


}`

## 获取团队的成员

获取团队的成员 GET /api/v2/groups/:login/users

  * 支持分页, PageSize 固定为 100



##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队 Login or ID  
---|---  
  
##### query Parameters

role| integer Enum: 0 1 2 角色 [筛选条件] (0:管理员, 1:成员, 2:只读成员)  
---|---  
offset| integer Default: 0 偏移量 [分页条件]  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/groups/{login}/users

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/users

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "id": 0,

      * "group_id": 0,

      * "user_id": 0,

      * "role": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "group": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "members_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

}

}

]


}`

## 变更成员

变更成员 PUT /api/v2/groups/:login/users/:id

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队 Login or ID  
---|---  
idrequired| string 用户 Login or ID  
  
##### Request Body schema: application/json

role| integer Default: 1 Enum: 0 1 2 角色 (0:管理员, 1:成员, 2:只读成员)  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/groups/{login}/users/{id}

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/users/{id}

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "role": 0


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "group_id": 0,

    * "user_id": 0,

    * "role": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "group": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "members_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

}

}


}`

## 删除成员

删除成员 DELETE /api/v2/groups/:login/users/:id

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队 Login or ID  
---|---  
idrequired| string 用户 Login or ID  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

delete/api/v2/groups/{login}/users/{id}

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/users/{id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "user_id": "string"

}


}`

## doc

doc

## 获取知识库的文档列表

获取知识库的文档列表 GET /api/v2/repos/:book_id/docs GET /api/v2/repos/:group_login/:book_slug/docs

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
##### query Parameters

offset| integer Default: 0 偏移量 [分页参数]  
---|---  
limit| integer <= 100 Default: 100 每页数量 [分页参数]  
optional_properties| string Default: "" 获取的额外字段, 多个字段以逗号分隔

  * 注意: 每页数量超过 100 本字段会失效
  * 支持的字段有:
    * hits: 文档阅读数
    * tags: 标签
    * latest_version_id: 最新已发版本 ID

  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{book_id}/docs

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/docs

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "meta": {
    * "total": 0

},

  * "data": [
    * {
      * "id": 0,

      * "type": "Doc",

      * "slug": "string",

      * "title": "string",

      * "description": "string",

      * "cover": "string",

      * "user_id": 0,

      * "book_id": 0,

      * "last_editor_id": 0,

      * "public": 0,

      * "status": "string",

      * "likes_count": 0,

      * "read_count": 0,

      * "hits": 0,

      * "comments_count": 0,

      * "word_count": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "published_at": "2019-08-24T14:15:22Z",

      * "first_published_at": "2019-08-24T14:15:22Z",

      * "book": {
        * "id": 0,

        * "type": "string",

        * "slug": "string",

        * "name": "string",

        * "user_id": 0,

        * "description": "string",

        * "creator_id": 0,

        * "public": 0,

        * "items_count": 0,

        * "likes_count": 0,

        * "watches_count": 0,

        * "content_updated_at": "2019-08-24T14:15:22Z",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z",

        * "user": {
          * "id": 0,

          * "type": "string",

          * "login": "string",

          * "name": "string",

          * "avatar_url": "string",

          * "books_count": 0,

          * "public_books_count": 0,

          * "followers_count": 0,

          * "following_count": 0,

          * "public": 0,

          * "description": "string",

          * "created_at": "2019-08-24T14:15:22Z",

          * "updated_at": "2019-08-24T14:15:22Z"

},

        * "namespace": "string"

},

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "last_editor": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "latest_version_id": 0,

      * "tags": {
        * "id": 0,

        * "title": "string",

        * "doc_id": 0,

        * "book_id": 0,

        * "user_id": 0,

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

}

}

]


}`

## 创建文档

创建文档 POST /api/v2/repos/:book_id/docs POST /api/v2/repos/:group_login/:book_slug/docs

  * 注意: 创建文档后不会自动添加到目录，需要调用"知识库目录更新接口"更新到目录中



##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
##### Request Body schema: application/json

slug| string 路径  
---|---  
title| string Default: "无标题" 标题  
public| integer Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)

  * 不填则继承知识库的公开性

  
format| string Default: "markdown" Enum: "markdown" "html" "lake" 内容格式 (markdown:Markdown 格式, html:HTML 标准格式, lake:语雀 Lake 格式)  
bodyrequired| string 正文内容  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

post/api/v2/repos/{book_id}/docs

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/docs

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "slug": "string",

  * "title": "无标题",

  * "public": 0,

  * "format": "markdown",

  * "body": "string"


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 获取文档详情

获取文档详情 GET /api/v2/repos/:book_id/docs/:id GET /api/v2/repos/:group_login/:book_slug/docs/:id

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
idrequired| string 文档 ID or 路径  
  
##### query Parameters

page_size| integer [ 1 .. 200 ] Default: 100 数据表使用，分页大小  
---|---  
page| integer >= 1 Default: 1 数据表使用，页码  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{book_id}/docs/{id}

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/docs/{id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 更新文档

更新文档 PUT /api/v2/repos/:book_id/docs/:id PUT /api/v2/repos/:group_login/:book_slug/docs/:id

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
idrequired| string 文档 ID or 路径  
  
##### Request Body schema: application/json

slug| string 路径  
---|---  
title| string 标题  
public| integer Default: 0 Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)  
format| string Default: "markdown" Enum: "markdown" "html" "lake" 内容格式 (markdown:Markdown 格式, html:HTML 标准格式, lake:语雀 Lake 格式)  
body| string 正文内容  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/repos/{book_id}/docs/{id}

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/docs/{id}

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "slug": "string",

  * "title": "string",

  * "public": 0,

  * "format": "markdown",

  * "body": "string"


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 删除文档

删除文档 DELETE /api/v2/repos/:book_id/docs/:id DELETE /api/v2/repos/:group_login/:book_slug/docs/:id

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
idrequired| string 文档 ID or 路径  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

delete/api/v2/repos/{book_id}/docs/{id}

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/docs/{id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 获取知识库的文档列表

获取知识库的文档列表 GET /api/v2/repos/:book_id/docs GET /api/v2/repos/:group_login/:book_slug/docs

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
##### query Parameters

offset| integer Default: 0 偏移量 [分页参数]  
---|---  
limit| integer <= 100 Default: 100 每页数量 [分页参数]  
optional_properties| string Default: "" 获取的额外字段, 多个字段以逗号分隔

  * 注意: 每页数量超过 100 本字段会失效
  * 支持的字段有:
    * hits: 文档阅读数
    * tags: 标签
    * latest_version_id: 最新已发版本 ID

  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{group_login}/{book_slug}/docs

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "meta": {
    * "total": 0

},

  * "data": [
    * {
      * "id": 0,

      * "type": "Doc",

      * "slug": "string",

      * "title": "string",

      * "description": "string",

      * "cover": "string",

      * "user_id": 0,

      * "book_id": 0,

      * "last_editor_id": 0,

      * "public": 0,

      * "status": "string",

      * "likes_count": 0,

      * "read_count": 0,

      * "hits": 0,

      * "comments_count": 0,

      * "word_count": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "published_at": "2019-08-24T14:15:22Z",

      * "first_published_at": "2019-08-24T14:15:22Z",

      * "book": {
        * "id": 0,

        * "type": "string",

        * "slug": "string",

        * "name": "string",

        * "user_id": 0,

        * "description": "string",

        * "creator_id": 0,

        * "public": 0,

        * "items_count": 0,

        * "likes_count": 0,

        * "watches_count": 0,

        * "content_updated_at": "2019-08-24T14:15:22Z",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z",

        * "user": {
          * "id": 0,

          * "type": "string",

          * "login": "string",

          * "name": "string",

          * "avatar_url": "string",

          * "books_count": 0,

          * "public_books_count": 0,

          * "followers_count": 0,

          * "following_count": 0,

          * "public": 0,

          * "description": "string",

          * "created_at": "2019-08-24T14:15:22Z",

          * "updated_at": "2019-08-24T14:15:22Z"

},

        * "namespace": "string"

},

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "last_editor": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "latest_version_id": 0,

      * "tags": {
        * "id": 0,

        * "title": "string",

        * "doc_id": 0,

        * "book_id": 0,

        * "user_id": 0,

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

}

}

]


}`

## 创建文档

创建文档 POST /api/v2/repos/:book_id/docs POST /api/v2/repos/:group_login/:book_slug/docs

  * 注意: 创建文档后不会自动添加到目录，需要调用"知识库目录更新接口"更新到目录中



##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
##### Request Body schema: application/json

slug| string 路径  
---|---  
title| string Default: "无标题" 标题  
public| integer Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)

  * 不填则继承知识库的公开性

  
format| string Default: "markdown" Enum: "markdown" "html" "lake" 内容格式 (markdown:Markdown 格式, html:HTML 标准格式, lake:语雀 Lake 格式)  
bodyrequired| string 正文内容  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

post/api/v2/repos/{group_login}/{book_slug}/docs

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "slug": "string",

  * "title": "无标题",

  * "public": 0,

  * "format": "markdown",

  * "body": "string"


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 获取文档详情

获取文档详情 GET /api/v2/repos/:book_id/docs/:id GET /api/v2/repos/:group_login/:book_slug/docs/:id

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
idrequired| string 文档 ID or 路径  
  
##### query Parameters

page_size| integer [ 1 .. 200 ] Default: 100 数据表使用，分页大小  
---|---  
page| integer >= 1 Default: 1 数据表使用，页码  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{group_login}/{book_slug}/docs/{id}

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs/{id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 更新文档

更新文档 PUT /api/v2/repos/:book_id/docs/:id PUT /api/v2/repos/:group_login/:book_slug/docs/:id

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
idrequired| string 文档 ID or 路径  
  
##### Request Body schema: application/json

slug| string 路径  
---|---  
title| string 标题  
public| integer Default: 0 Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)  
format| string Default: "markdown" Enum: "markdown" "html" "lake" 内容格式 (markdown:Markdown 格式, html:HTML 标准格式, lake:语雀 Lake 格式)  
body| string 正文内容  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/repos/{group_login}/{book_slug}/docs/{id}

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs/{id}

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "slug": "string",

  * "title": "string",

  * "public": 0,

  * "format": "markdown",

  * "body": "string"


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 删除文档

删除文档 DELETE /api/v2/repos/:book_id/docs/:id DELETE /api/v2/repos/:group_login/:book_slug/docs/:id

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
idrequired| string 文档 ID or 路径  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

delete/api/v2/repos/{group_login}/{book_slug}/docs/{id}

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs/{id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "Doc",

    * "slug": "string",

    * "title": "string",

    * "description": "string",

    * "cover": "string",

    * "user_id": 0,

    * "book_id": 0,

    * "last_editor_id": 0,

    * "format": "markdown",

    * "body_draft": "string",

    * "body": "string",

    * "body_sheet": "string",

    * "body_table": "string",

    * "body_html": "string",

    * "body_lake": "string",

    * "public": 0,

    * "status": "string",

    * "likes_count": 0,

    * "read_count": 0,

    * "hits": 0,

    * "comments_count": 0,

    * "word_count": 0,

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "published_at": "2019-08-24T14:15:22Z",

    * "first_published_at": "2019-08-24T14:15:22Z",

    * "book": {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

},

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "creator": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "tags": {
      * "id": 0,

      * "title": "string",

      * "doc_id": 0,

      * "book_id": 0,

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "latest_version_id": 0

}


}`

## 获取文档历史版本列表

获取文档历史版本列表 GET /api/v2/doc_versions

  * 按时间倒序返回最近 100 个已发布版本



##### Authorizations:

_authToken_

##### query Parameters

doc_idrequired| integer 文档 ID  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/doc_versions

线上访问地址

https://www.yuque.com/api/v2/doc_versions

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "id": 0,

      * "doc_id": 0,

      * "slug": "string",

      * "title": "string",

      * "user_id": 0,

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

}

}

]


}`

## 获取文档历史版本详情

获取文档历史版本详情 GET /api/v2/doc_versions/:id

##### Authorizations:

_authToken_

##### path Parameters

idrequired| integer 版本 ID  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/doc_versions/{id}

线上访问地址

https://www.yuque.com/api/v2/doc_versions/{id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "doc_id": 0,

    * "slug": "string",

    * "title": "string",

    * "user_id": 0,

    * "format": "markdown",

    * "body": "string",

    * "body_html": "string",

    * "body_asl": "string",

    * "diff": "string",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

}

}


}`

## 获取目录

获取目录 GET /api/v2/repos/:book_id/toc GET /api/v2/repos/:group_login/:book_slug/toc

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{book_id}/toc

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/toc

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "uuid": "string",

      * "type": "DOC",

      * "title": "string",

      * "url": "string",

      * "slug": "string",

      * "id": 0,

      * "doc_id": 0,

      * "level": 0,

      * "depth": 0,

      * "open_window": 0,

      * "visible": 0,

      * "prev_uuid": "string",

      * "sibling_uuid": "string",

      * "child_uuid": "string",

      * "parent_uuid": "string"

}

]


}`

## 更新目录

更新目录 PUT /api/v2/repos/:book_id/toc PUT /api/v2/repos/:group_login/:book_slug/toc

字段说明:

  * 所有场景
    * 必填字段
      * action
      * action_mode
    * 选填字段
      * target_uuid
      * visible
  * 创建场景
    * 必填字段
      * 创建文档节点
        * type
        * doc_ids
      * 创建分组节点
        * type
        * title
      * 创建外链节点
        * type
        * title
        * url
        * open_window
  * 移动场景
    * 必填字段
      * target_uuid
      * node_uuid
  * 编辑场景
    * 必填字段
      * node_uuid
    * 选填字段
      * type
      * title
      * url
      * open_window
  * 删除场景
    * 必填字段
      * node_uuid



##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
##### Request Body schema: application/json

actionrequired| string Enum: "appendNode" "prependNode" "editNode" "removeNode" 操作 (appendNode:尾插, prependNode:头插, editNode:编辑节点, removeNode:删除节点)

  * action_mode 必填
  * 创建场景下不支持同级头插 prependNode
  * 删除节点不会删除关联文档
  * 删除节点时: action_mode=sibling (删除当前节点), action_mode=child (删除当前节点及子节点)

  
---|---  
action_mode| string Enum: "sibling" "child" 操作模式 (sibling:同级, child:子级)  
target_uuid| string 目标节点 UUID, 不填默认为根节点

  * 获取方式: 调用"获取知识库目录"接口获取

  
node_uuid| string 操作节点 UUID [移动/更新/删除必填]

  * 获取方式: 调用"获取知识库目录"接口获取

  
doc_id| integer Deprecated 文档 ID [创建文档必填]  
doc_ids| Array of integers 文档 ID 数组 [创建文档必填]  
type| string Default: "DOC" Enum: "DOC" "LINK" "TITLE" 节点类型 [创建必填] (DOC:文档, LINK:外链, TITLE:分组)  
title| string 节点名称 [创建分组/外链必填]  
url| string 节点 URL [创建外链必填]  
open_window| integer Default: 0 Enum: 0 1 是否新窗口打开 [外链选填] (0:当前页打开, 1:新窗口打开)  
visible| integer Default: 1 Enum: 0 1 是否可见 (0:不可见, 1:可见)  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/repos/{book_id}/toc

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}/toc

###  Request samples

  * Payload



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "action": "appendNode",

  * "action_mode": "sibling",

  * "target_uuid": "string",

  * "node_uuid": "string",

  * "doc_id": 0,

  * "doc_ids": [
    * 0

],

  * "type": "DOC",

  * "title": "string",

  * "url": "string",

  * "open_window": 0,

  * "visible": 0


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "uuid": "string",

      * "type": "DOC",

      * "title": "string",

      * "url": "string",

      * "slug": "string",

      * "id": 0,

      * "doc_id": 0,

      * "level": 0,

      * "depth": 0,

      * "open_window": 0,

      * "visible": 0,

      * "prev_uuid": "string",

      * "sibling_uuid": "string",

      * "child_uuid": "string",

      * "parent_uuid": "string"

}

]


}`

## 获取目录

获取目录 GET /api/v2/repos/:book_id/toc GET /api/v2/repos/:group_login/:book_slug/toc

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{group_login}/{book_slug}/toc

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/toc

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "uuid": "string",

      * "type": "DOC",

      * "title": "string",

      * "url": "string",

      * "slug": "string",

      * "id": 0,

      * "doc_id": 0,

      * "level": 0,

      * "depth": 0,

      * "open_window": 0,

      * "visible": 0,

      * "prev_uuid": "string",

      * "sibling_uuid": "string",

      * "child_uuid": "string",

      * "parent_uuid": "string"

}

]


}`

## 更新目录

更新目录 PUT /api/v2/repos/:book_id/toc PUT /api/v2/repos/:group_login/:book_slug/toc

字段说明:

  * 所有场景
    * 必填字段
      * action
      * action_mode
    * 选填字段
      * target_uuid
      * visible
  * 创建场景
    * 必填字段
      * 创建文档节点
        * type
        * doc_ids
      * 创建分组节点
        * type
        * title
      * 创建外链节点
        * type
        * title
        * url
        * open_window
  * 移动场景
    * 必填字段
      * target_uuid
      * node_uuid
  * 编辑场景
    * 必填字段
      * node_uuid
    * 选填字段
      * type
      * title
      * url
      * open_window
  * 删除场景
    * 必填字段
      * node_uuid



##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
##### Request Body schema: application/json

actionrequired| string Enum: "appendNode" "prependNode" "editNode" "removeNode" 操作 (appendNode:尾插, prependNode:头插, editNode:编辑节点, removeNode:删除节点)

  * action_mode 必填
  * 创建场景下不支持同级头插 prependNode
  * 删除节点不会删除关联文档
  * 删除节点时: action_mode=sibling (删除当前节点), action_mode=child (删除当前节点及子节点)

  
---|---  
action_mode| string Enum: "sibling" "child" 操作模式 (sibling:同级, child:子级)  
target_uuid| string 目标节点 UUID, 不填默认为根节点

  * 获取方式: 调用"获取知识库目录"接口获取

  
node_uuid| string 操作节点 UUID [移动/更新/删除必填]

  * 获取方式: 调用"获取知识库目录"接口获取

  
doc_id| integer Deprecated 文档 ID [创建文档必填]  
doc_ids| Array of integers 文档 ID 数组 [创建文档必填]  
type| string Default: "DOC" Enum: "DOC" "LINK" "TITLE" 节点类型 [创建必填] (DOC:文档, LINK:外链, TITLE:分组)  
title| string 节点名称 [创建分组/外链必填]  
url| string 节点 URL [创建外链必填]  
open_window| integer Default: 0 Enum: 0 1 是否新窗口打开 [外链选填] (0:当前页打开, 1:新窗口打开)  
visible| integer Default: 1 Enum: 0 1 是否可见 (0:不可见, 1:可见)  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/repos/{group_login}/{book_slug}/toc

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}/toc

###  Request samples

  * Payload



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "action": "appendNode",

  * "action_mode": "sibling",

  * "target_uuid": "string",

  * "node_uuid": "string",

  * "doc_id": 0,

  * "doc_ids": [
    * 0

],

  * "type": "DOC",

  * "title": "string",

  * "url": "string",

  * "open_window": 0,

  * "visible": 0


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "uuid": "string",

      * "type": "DOC",

      * "title": "string",

      * "url": "string",

      * "slug": "string",

      * "id": 0,

      * "doc_id": 0,

      * "level": 0,

      * "depth": 0,

      * "open_window": 0,

      * "visible": 0,

      * "prev_uuid": "string",

      * "sibling_uuid": "string",

      * "child_uuid": "string",

      * "parent_uuid": "string"

}

]


}`

## repo

repo

## 获取知识库列表

获取知识库列表 GET /api/v2/groups/:id/repos GET /api/v2/groups/:login/repos

GET /api/v2/users/:id/repos GET /api/v2/users/:login/repos

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 用户/团队的 Login 或 ID  
---|---  
  
##### query Parameters

offset| integer Default: 0 偏移量 [分页参数]  
---|---  
limit| integer <= 100 Default: 100 每页数量 [分页参数]  
type| string Enum: "Book" "Design" 类型 [筛选条件] (Book:文档型知识库, Design: 画板型知识库)  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/groups/{login}/repos

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/repos

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

}

]


}`

## 创建知识库

创建知识库 POST /api/v2/groups/:id/repos POST /api/v2/groups/:login/repos

POST /api/v2/users/:id/repos POST /api/v2/users/:login/repos

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 用户/团队的 Login 或 ID  
---|---  
  
##### Request Body schema: application/json

namerequired| string 名称  
---|---  
slugrequired| string 路径  
description| string 简介  
public| integer Default: 0 Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)  
enhancedPrivacy| boolean 增强私密性

  * 将除团队管理员之外的团队成员、团队只读成员也设置为无权限

  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

post/api/v2/groups/{login}/repos

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/repos

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "name": "string",

  * "slug": "string",

  * "description": "string",

  * "public": 0,

  * "enhancedPrivacy": true


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 获取知识库列表

获取知识库列表 GET /api/v2/groups/:id/repos GET /api/v2/groups/:login/repos

GET /api/v2/users/:id/repos GET /api/v2/users/:login/repos

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 用户/团队的 Login 或 ID  
---|---  
  
##### query Parameters

offset| integer Default: 0 偏移量 [分页参数]  
---|---  
limit| integer <= 100 Default: 100 每页数量 [分页参数]  
type| string Enum: "Book" "Design" 类型 [筛选条件] (Book:文档型知识库, Design: 画板型知识库)  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/users/{login}/repos

线上访问地址

https://www.yuque.com/api/v2/users/{login}/repos

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": [
    * {
      * "id": 0,

      * "type": "string",

      * "slug": "string",

      * "name": "string",

      * "user_id": 0,

      * "description": "string",

      * "creator_id": 0,

      * "public": 0,

      * "items_count": 0,

      * "likes_count": 0,

      * "watches_count": 0,

      * "content_updated_at": "2019-08-24T14:15:22Z",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z",

      * "user": {
        * "id": 0,

        * "type": "string",

        * "login": "string",

        * "name": "string",

        * "avatar_url": "string",

        * "books_count": 0,

        * "public_books_count": 0,

        * "followers_count": 0,

        * "following_count": 0,

        * "public": 0,

        * "description": "string",

        * "created_at": "2019-08-24T14:15:22Z",

        * "updated_at": "2019-08-24T14:15:22Z"

},

      * "namespace": "string"

}

]


}`

## 创建知识库

创建知识库 POST /api/v2/groups/:id/repos POST /api/v2/groups/:login/repos

POST /api/v2/users/:id/repos POST /api/v2/users/:login/repos

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 用户/团队的 Login 或 ID  
---|---  
  
##### Request Body schema: application/json

namerequired| string 名称  
---|---  
slugrequired| string 路径  
description| string 简介  
public| integer Default: 0 Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)  
enhancedPrivacy| boolean 增强私密性

  * 将除团队管理员之外的团队成员、团队只读成员也设置为无权限

  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

post/api/v2/users/{login}/repos

线上访问地址

https://www.yuque.com/api/v2/users/{login}/repos

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "name": "string",

  * "slug": "string",

  * "description": "string",

  * "public": 0,

  * "enhancedPrivacy": true


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 获取知识库详情

获取知识库详情 GET /api/v2/repos/:book_id GET /api/v2/repos/:group_login/:book_slug

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{book_id}

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "toc_yml": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 更新知识库

更新知识库 PUT /api/v2/repos/:book_id PUT /api/v2/repos/:group_login/:book_slug

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
##### Request Body schema: application/json

name| string 名称  
---|---  
slug| string 路径  
description| string 简介  
public| integer Default: 0 Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)  
toc| string 目录

  * 可利用此字段批量更新知识库的目录
  * 必须是 Markdown 格式, `[名称](文档路径)` 示例:


    
    
    - [新手指引]()
      - [语雀是什么](about)
      - [常见问题](faq)
    - [基础功能]()
      - [工作台](dashboard)
      - [如何设置自定义路径](nkt888)
      - [外链](http://www.alipay.com)
      
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/repos/{book_id}

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "name": "string",

  * "slug": "string",

  * "description": "string",

  * "public": 0,

  * "toc": "string"


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 删除知识库

删除知识库 DELETE /api/v2/repos/:book_id DELETE /api/v2/repos/:group_login/:book_slug

##### Authorizations:

_authToken_

##### path Parameters

book_idrequired| integer 知识库 ID  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

delete/api/v2/repos/{book_id}

线上访问地址

https://www.yuque.com/api/v2/repos/{book_id}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 获取知识库详情

获取知识库详情 GET /api/v2/repos/:book_id GET /api/v2/repos/:group_login/:book_slug

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/repos/{group_login}/{book_slug}

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "toc_yml": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 更新知识库

更新知识库 PUT /api/v2/repos/:book_id PUT /api/v2/repos/:group_login/:book_slug

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
##### Request Body schema: application/json

name| string 名称  
---|---  
slug| string 路径  
description| string 简介  
public| integer Default: 0 Enum: 0 1 2 公开性 (0:私密, 1:公开, 2:企业内公开)  
toc| string 目录

  * 可利用此字段批量更新知识库的目录
  * 必须是 Markdown 格式, `[名称](文档路径)` 示例:


    
    
    - [新手指引]()
      - [语雀是什么](about)
      - [常见问题](faq)
    - [基础功能]()
      - [工作台](dashboard)
      - [如何设置自定义路径](nkt888)
      - [外链](http://www.alipay.com)
      
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

put/api/v2/repos/{group_login}/{book_slug}

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}

###  Request samples

  * Payload



Content type

application/json

Copy

`{

  * "name": "string",

  * "slug": "string",

  * "description": "string",

  * "public": 0,

  * "toc": "string"


}`

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## 删除知识库

删除知识库 DELETE /api/v2/repos/:book_id DELETE /api/v2/repos/:group_login/:book_slug

##### Authorizations:

_authToken_

##### path Parameters

group_loginrequired| string 团队 Login  
---|---  
book_slugrequired| string 知识库路径  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

delete/api/v2/repos/{group_login}/{book_slug}

线上访问地址

https://www.yuque.com/api/v2/repos/{group_login}/{book_slug}

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "id": 0,

    * "type": "string",

    * "slug": "string",

    * "name": "string",

    * "user_id": 0,

    * "description": "string",

    * "creator_id": 0,

    * "public": 0,

    * "items_count": 0,

    * "likes_count": 0,

    * "watches_count": 0,

    * "content_updated_at": "2019-08-24T14:15:22Z",

    * "created_at": "2019-08-24T14:15:22Z",

    * "updated_at": "2019-08-24T14:15:22Z",

    * "user": {
      * "id": 0,

      * "type": "string",

      * "login": "string",

      * "name": "string",

      * "avatar_url": "string",

      * "books_count": 0,

      * "public_books_count": 0,

      * "followers_count": 0,

      * "following_count": 0,

      * "public": 0,

      * "description": "string",

      * "created_at": "2019-08-24T14:15:22Z",

      * "updated_at": "2019-08-24T14:15:22Z"

},

    * "namespace": "string"

}


}`

## statistic

statistic

## 团队.汇总统计数据

团队.汇总统计数据 GET /api/v2/groups/:login/statistics

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队的 Login 或 ID  
---|---  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/groups/{login}/statistics

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/statistics

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "bizdate": "string",

    * "user_id": "string",

    * "organization_id": "string",

    * "member_count": "string",

    * "collaborator_count": "string",

    * "day_read_count": "string",

    * "day_write_count": "string",

    * "write_count": "string",

    * "read_count": "string",

    * "read_count_30": "string",

    * "read_count_365": "string",

    * "comment_count": "string",

    * "comment_count_30": "string",

    * "comment_count_365": "string",

    * "like_count": "string",

    * "like_count_30": "string",

    * "like_count_365": "string",

    * "follow_count": "string",

    * "collect_count": "string",

    * "doc_count": "string",

    * "sheet_count": "string",

    * "board_count": "string",

    * "show_count": "string",

    * "resource_count": "string",

    * "artboard_count": "string",

    * "attachment_count": "string",

    * "book_count": "string",

    * "public_book_count": "string",

    * "private_book_count": "string",

    * "book_book_count": "string",

    * "book_resource_count": "string",

    * "book_design_count": "string",

    * "book_thread_count": "string",

    * "data_usage": "string",

    * "grains_count": "string",

    * "grains_count_sum": "string",

    * "grains_count_consume": "string",

    * "interaction_people_count": "string",

    * "content_count": "string",

    * "collaboration_count": "string",

    * "working_hours": "string",

    * "baike": "string",

    * "table_count": "string"

}


}`

## 团队.成员统计数据

团队.成员统计数据 GET /api/v2/groups/:login/statistics/members

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队的 Login 或 ID  
---|---  
  
##### query Parameters

name| string 成员名 [过滤条件]  
---|---  
range| integer Default: 0 Enum: 0 30 365 时间范围 [过滤条件] (0:全部, 30:近 30 天, 365:近一年)  
page| integer Default: 1 页码  
limit| integer <= 20 Default: 10 分页数量  
sortField| string Enum: "write_doc_count" "write_count" "read_count" "like_count" 排序字段  
sortOrder| string Default: "desc" Enum: "desc" "asc" 排序方向  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/groups/{login}/statistics/members

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/statistics/members

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "members": {
      * "bizdate": "string",

      * "user_id": "string",

      * "group_id": "string",

      * "organization_id": "string",

      * "write_count": "string",

      * "write_count_30": "string",

      * "write_count_365": "string",

      * "write_doc_count": "string",

      * "write_doc_count_30": "string",

      * "write_doc_count_365": "string",

      * "read_count": "string",

      * "read_count_30": "string",

      * "read_count_365": "string",

      * "like_count": "string",

      * "like_count_30": "string",

      * "like_count_365": "string",

      * "user": "string"

},

    * "total": 0

}


}`

## 团队.知识库统计数据

团队.知识库统计数据 GET /api/v2/groups/:login/statistics/books

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队的 Login 或 ID  
---|---  
  
##### query Parameters

name| string 知识库名 [过滤条件]  
---|---  
range| integer Default: 0 Enum: 0 30 365 时间范围 [过滤条件] (0:全部, 30:近 30 天, 365:近一年)  
page| integer Default: 1 页码  
limit| integer <= 20 Default: 10 分页数量  
sortField| string Enum: "content_updated_at_ms" "word_count" "post_count" "read_count" "like_count" "watch_count" "comment_count" 排序字段  
sortOrder| string Default: "desc" Enum: "desc" "asc" 排序方向  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/groups/{login}/statistics/books

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/statistics/books

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "books": {
      * "bizdate": "string",

      * "book_id": "string",

      * "slug": "string",

      * "name": "string",

      * "type": "string",

      * "is_public": "string",

      * "content_updated_at_ms": "string",

      * "user_id": "string",

      * "organization_id": "string",

      * "day_read_count": "string",

      * "day_write_count": "string",

      * "day_like_count": "string",

      * "post_count": "string",

      * "word_count": "string",

      * "write_count": "string",

      * "write_count_30": "string",

      * "read_count": "string",

      * "read_count_30": "string",

      * "read_count_365": "string",

      * "like_count": "string",

      * "like_count_7": "string",

      * "like_count_30": "string",

      * "like_count_365": "string",

      * "watch_count": "string",

      * "watch_count_7": "string",

      * "watch_count_30": "string",

      * "watch_count_365": "string",

      * "comment_count": "string",

      * "comment_count_30": "string",

      * "comment_count_365": "string",

      * "like_rank_rate": "string",

      * "popularity_30": "string",

      * "doc_count": "string",

      * "sheet_count": "string",

      * "board_count": "string",

      * "show_count": "string",

      * "resource_count": "string",

      * "artboard_count": "string",

      * "attachment_count": "string",

      * "interaction_people_count": "string",

      * "content_count": "string",

      * "collaboration_count": "string",

      * "working_hours": "string",

      * "baike": "string",

      * "table_count": "string"

},

    * "total": 0

}


}`

## 团队.文档统计数据

团队.文档统计数据 GET /api/v2/groups/:login/statistics/docs

##### Authorizations:

_authToken_

##### path Parameters

loginrequired| string 团队的 Login 或 ID  
---|---  
  
##### query Parameters

bookId| integer 指定知识库 [过滤条件]  
---|---  
name| string 文档名 [过滤条件]  
range| integer Default: 0 Enum: 0 30 365 时间范围 [过滤条件] (0:全部, 30:近 30 天, 365:近一年)  
page| integer Default: 1 页码  
limit| integer <= 20 Default: 10 分页数量  
sortField| string Enum: "content_updated_at" "word_count" "read_count" "like_count" "comment_count" "created_at" 排序字段  
sortOrder| string Default: "desc" Enum: "desc" "asc" 排序方向  
  
### Responses

**200 **

OK

**400 **

请求参数非法

**401 **

Token/Scope 未通过鉴权

**403 **

无操作权限

**404 **

实体未找到

**422 **

请求参数校验失败

**429 **

访问频率超限

**500 **

内部错误

get/api/v2/groups/{login}/statistics/docs

线上访问地址

https://www.yuque.com/api/v2/groups/{login}/statistics/docs

###  Response samples

  * 200



Content type

application/json

Copy

Expand all  Collapse all 

`{

  * "data": {
    * "docs": {
      * "bizdate": "string",

      * "book_id": "string",

      * "doc_id": "string",

      * "slug": "string",

      * "title": "string",

      * "type": "string",

      * "is_public": "string",

      * "created_at": "string",

      * "content_updated_at": "string",

      * "user_id": "string",

      * "organization_id": "string",

      * "day_read_count": "string",

      * "day_write_count": "string",

      * "day_like_count": "string",

      * "word_count": "string",

      * "write_count": "string",

      * "read_count": "string",

      * "read_count_7": "string",

      * "read_count_30": "string",

      * "read_count_365": "string",

      * "like_count": "string",

      * "like_count_7": "string",

      * "like_count_30": "string",

      * "like_count_365": "string",

      * "comment_count": "string",

      * "comment_count_30": "string",

      * "comment_count_365": "string",

      * "popularity_30": "string",

      * "attachment_count": "string",

      * "user": "string"

},

    * "total": 0

}


}`

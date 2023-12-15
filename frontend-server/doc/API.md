# API



## /auth



### /

**作用**：快速验证身份

**前端参数示例**：

```javascript
携带Cookie: sid=26v29rbf5-1v51_w481e8vsdvsDV
```

**后端返回示例**：

```javascript
{
	"code": 1000,
	"message": ok
}
```

```javascript
{
	"code": 1001,
	"message": "登陆身份已过期，请重新登录"
}
```





### /login

**作用**：验证账号密码返回登陆SessionID

**前端参数示例**：

```javascript
{
    "mob": 18766554433,
    "pwd": "Aa123456"
}
```

**后端返回示例**：

```javascript
{
	"code": 1000,
	"message": ok
}
```

```javascript
{
	"code": 1001,
	"message": "用户名或密码错误"
}
```





### /register

**作用**：根据手机号验证码密码进行注册

**前端参数示例**：

```javascript
{
    "mob": 18766554433,
    "code": 854427,
    "pwd": "Aa123456"
}
```

**后端返回示例**：

```javascript
{
	"code": 1000,
	"message": ok
}
```

```javascript
{
	"code": 1001,
	"message": "该手机号已被注册"
}
```

```javascript
{
	"code": 1002,
	"message": "无效的验证码"
}
```

```javascript
{
	"code": 1003,
	"message": "密码格式不正确"
}
```



### /send

**作用**：发送短信验证码

**前端参数示例**：

```javascript
{
    "mob": 18766554433,
}
```

**后端返回示例**：

```javascript
{
	"code": 1000,
	"Message": ok
}
```

```javascript
{
	"code": 1001,
	"message": "由于尝试次数过多，此ip已被禁止发送验证码"
}
```

```javascript
{
	"code": 2000,
	"message": "发生内部错误，错误代码：sms.invalid_phone_number"
}
```



### /logout

**作用**：登出，注销登陆缓存

**前端参数示例**：

```javascript
携带Cookie: sid=26v29rbf5-1v51_w481e8vsdvsDV
```

**后端返回示例**：

```javascript
{
	"code": 1000,
	"Message": ok
}
```

```javascript
{
	"code": 1001,
	"message": "发生未知错误，注销失败"
}
```


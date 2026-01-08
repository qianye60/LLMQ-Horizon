# nonebot.permission

- nonebot.permission


# nonebot.permission

本模块是Matcher.permission的类型定义。

每个事件响应器拥有一个Permission，其中是PermissionChecker的集合。
只要有一个PermissionChecker检查结果为True时就会继续运行。


## defUSER(*users, perm=None)​

- 说明匹配当前事件属于指定会话。如果perm中仅有User类型的权限检查函数，则会去除原有检查函数的会话 ID 限制。
- 参数*users(str)perm(Permission | None): 需要同时满足的权限user: 会话白名单
- 返回untyped

说明

匹配当前事件属于指定会话。

如果perm中仅有User类型的权限检查函数，则会去除原有检查函数的会话 ID 限制。

参数

- *users(str)
- perm(Permission | None): 需要同时满足的权限
- user: 会话白名单

*users(str)

perm(Permission | None): 需要同时满足的权限

user: 会话白名单

返回

- untyped


## classPermission(*checkers)​

- 说明权限类。当事件传递时，在Matcher运行前进行检查。
- 参数*checkers(T_PermissionChecker|Dependent[bool]): PermissionChecker
- 用法Permission(async_function)|sync_function# 等价于Permission(async_function,sync_function)

说明

权限类。

当事件传递时，在Matcher运行前进行检查。

参数

- *checkers(T_PermissionChecker|Dependent[bool]): PermissionChecker

用法


```python
Permission(async_function) | sync_function# 等价于Permission(async_function, sync_function)
```


### instance-varcheckers​

- 类型:set[Dependent[bool]]
- 说明:存储PermissionChecker

类型:set[Dependent[bool]]

说明:存储PermissionChecker


### async method__call__(bot, event, stack=None, dependency_cache=None)​

- 说明:检查是否满足某个权限。
- 参数bot(Bot): Bot 对象event(Event): Event 对象stack(AsyncExitStack | None): 异步上下文栈dependency_cache(T_DependencyCache| None): 依赖缓存
- 返回bool

说明:检查是否满足某个权限。

参数

- bot(Bot): Bot 对象
- event(Event): Event 对象
- stack(AsyncExitStack | None): 异步上下文栈
- dependency_cache(T_DependencyCache| None): 依赖缓存

bot(Bot): Bot 对象

event(Event): Event 对象

stack(AsyncExitStack | None): 异步上下文栈

dependency_cache(T_DependencyCache| None): 依赖缓存

返回

- bool


## classUser(users, perm=None)​

- 说明:检查当前事件是否属于指定会话。
- 参数users(tuple[str, ...]): 会话 ID 元组perm(Permission | None): 需同时满足的权限

说明:检查当前事件是否属于指定会话。

参数

- users(tuple[str, ...]): 会话 ID 元组
- perm(Permission | None): 需同时满足的权限

users(tuple[str, ...]): 会话 ID 元组

perm(Permission | None): 需同时满足的权限


### classmethodfrom_event(event, perm=None)​

- 说明从事件中获取会话 ID。如果perm中仅有User类型的权限检查函数，则会去除原有的会话 ID 限制。
- 参数event(Event): Event 对象perm(Permission | None): 需同时满足的权限
- 返回Self

说明

从事件中获取会话 ID。

如果perm中仅有User类型的权限检查函数，则会去除原有的会话 ID 限制。

参数

- event(Event): Event 对象
- perm(Permission | None): 需同时满足的权限

event(Event): Event 对象

perm(Permission | None): 需同时满足的权限

返回

- Self


### classmethodfrom_permission(*users, perm=None)​

- 说明指定会话与权限。如果perm中仅有User类型的权限检查函数，则会去除原有的会话 ID 限制。
- 参数*users(str): 会话白名单perm(Permission | None): 需同时满足的权限
- 返回Self

说明

指定会话与权限。

如果perm中仅有User类型的权限检查函数，则会去除原有的会话 ID 限制。

参数

- *users(str): 会话白名单
- perm(Permission | None): 需同时满足的权限

*users(str): 会话白名单

perm(Permission | None): 需同时满足的权限

返回

- Self


## classMessage(<auto>)​

- 说明:检查是否为消息事件
- 参数auto

说明:检查是否为消息事件

参数

auto


## classNotice(<auto>)​

- 说明:检查是否为通知事件
- 参数auto

说明:检查是否为通知事件

参数

auto


## classRequest(<auto>)​

- 说明:检查是否为请求事件
- 参数auto

说明:检查是否为请求事件

参数

auto


## classMetaEvent(<auto>)​

- 说明:检查是否为元事件
- 参数auto

说明:检查是否为元事件

参数

auto


## varMESSAGE​

- 类型:Permission
- 说明匹配任意message类型事件仅在需要同时捕获不同类型事件时使用，优先使用 message type 的 Matcher。

类型:Permission

说明

匹配任意message类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 message type 的 Matcher。


## varNOTICE​

- 类型:Permission
- 说明匹配任意notice类型事件仅在需要同时捕获不同类型事件时使用，优先使用 notice type 的 Matcher。

类型:Permission

说明

匹配任意notice类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 notice type 的 Matcher。


## varREQUEST​

- 类型:Permission
- 说明匹配任意request类型事件仅在需要同时捕获不同类型事件时使用，优先使用 request type 的 Matcher。

类型:Permission

说明

匹配任意request类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 request type 的 Matcher。


## varMETAEVENT​

- 类型:Permission
- 说明匹配任意meta_event类型事件仅在需要同时捕获不同类型事件时使用，优先使用 meta_event type 的 Matcher。

类型:Permission

说明

匹配任意meta_event类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 meta_event type 的 Matcher。


## classSuperUser(<auto>)​

- 说明:检查当前事件是否是消息事件且属于超级管理员
- 参数auto

说明:检查当前事件是否是消息事件且属于超级管理员

参数

auto


## varSUPERUSER​

- 类型:Permission
- 说明:匹配任意超级用户事件

类型:Permission

说明:匹配任意超级用户事件

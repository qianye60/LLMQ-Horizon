# nonebot.typing

- nonebot.typing


# nonebot.typing

本模块定义了 NoneBot 模块中共享的一些类型。

使用 Python 的 Type Hint 语法，
参考PEP 484,PEP 526和typing。


## defoverrides(InterfaceClass)​

- 说明:标记一个方法为父类 interface 的 implement
- 参数InterfaceClass(object)
- 返回untyped

说明:标记一个方法为父类 interface 的 implement

参数

- InterfaceClass(object)

返回

- untyped


## deftype_has_args(type_)​

- 参数type_(type[Any])
- 返回bool

参数

- type_(type[Any])

返回

- bool


## deforigin_is_union(origin)​

- 参数origin(type[Any] | None)
- 返回bool

参数

- origin(type[Any] | None)

返回

- bool


## deforigin_is_literal(origin)​

- 说明:判断是否是 Literal 类型
- 参数origin(type[Any] | None)
- 返回bool

说明:判断是否是 Literal 类型

参数

- origin(type[Any] | None)

返回

- bool


## defall_literal_values(type_)​

- 说明:获取 Literal 类型包含的所有值
- 参数type_(type[Any])
- 返回list[Any]

说明:获取 Literal 类型包含的所有值

参数

- type_(type[Any])

返回

- list[Any]


## deforigin_is_annotated(origin)​

- 说明:判断是否是 Annotated 类型
- 参数origin(type[Any] | None)
- 返回bool

说明:判断是否是 Annotated 类型

参数

- origin(type[Any] | None)

返回

- bool


## defis_none_type(type_)​

- 说明:判断是否是 None 类型
- 参数type_(type[Any])
- 返回bool

说明:判断是否是 None 类型

参数

- type_(type[Any])

返回

- bool


## defis_type_alias_type(type_)​

- 参数type_(type[Any])
- 返回bool

参数

- type_(type[Any])

返回

- bool


## defevaluate_forwardref(ref, globalns, localns)​

- 参数ref(ForwardRef)globalns(dict[str, Any])localns(dict[str, Any])
- 返回Any

参数

- ref(ForwardRef)
- globalns(dict[str, Any])
- localns(dict[str, Any])

ref(ForwardRef)

globalns(dict[str, Any])

localns(dict[str, Any])

返回

- Any


## classStateFlag(<auto>)​

- 参数auto

参数

auto


## varT_State​

- 类型:dict[Any, Any]
- 说明:事件处理状态 State 类型

类型:dict[Any, Any]

说明:事件处理状态 State 类型


## varT_BotConnectionHook​

- 类型:_DependentCallable[Any]
- 说明Bot 连接建立时钩子函数依赖参数:DependParam: 子依赖参数BotParam: Bot 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[Any]

说明

Bot 连接建立时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数


## varT_BotDisconnectionHook​

- 类型:_DependentCallable[Any]
- 说明Bot 连接断开时钩子函数依赖参数:DependParam: 子依赖参数BotParam: Bot 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[Any]

说明

Bot 连接断开时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数


## varT_CallingAPIHook​

- 类型:(Bot, str, dict[str, Any]) -> Awaitable[Any]
- 说明:bot.call_api钩子函数

类型:(Bot, str, dict[str, Any]) -> Awaitable[Any]

说明:bot.call_api钩子函数


## varT_CalledAPIHook​

- 类型:(Bot, Exception | None, str, dict[str, Any], Any) -> Awaitable[Any]
- 说明:bot.call_api后执行的函数，参数分别为 bot, exception, api, data, result

类型:(Bot, Exception | None, str, dict[str, Any], Any) -> Awaitable[Any]

说明:bot.call_api后执行的函数，参数分别为 bot, exception, api, data, result


## varT_EventPreProcessor​

- 类型:_DependentCallable[Any]
- 说明事件预处理函数 EventPreProcessor 类型依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[Any]

说明

事件预处理函数 EventPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数


## varT_EventPostProcessor​

- 类型:_DependentCallable[Any]
- 说明事件后处理函数 EventPostProcessor 类型依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[Any]

说明

事件后处理函数 EventPostProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数


## varT_RunPreProcessor​

- 类型:_DependentCallable[Any]
- 说明事件响应器运行前预处理函数 RunPreProcessor 类型依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象MatcherParam: Matcher 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[Any]

说明

事件响应器运行前预处理函数 RunPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数


## varT_RunPostProcessor​

- 类型:_DependentCallable[Any]
- 说明事件响应器运行后后处理函数 RunPostProcessor 类型依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象MatcherParam: Matcher 对象ExceptionParam: 异常对象（可能为 None）DefaultParam: 带有默认值的参数

类型:_DependentCallable[Any]

说明

事件响应器运行后后处理函数 RunPostProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- ExceptionParam: 异常对象（可能为 None）
- DefaultParam: 带有默认值的参数


## varT_RuleChecker​

- 类型:_DependentCallable[bool]
- 说明RuleChecker 即判断是否响应事件的处理函数。依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[bool]

说明

RuleChecker 即判断是否响应事件的处理函数。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数


## varT_PermissionChecker​

- 类型:_DependentCallable[bool]
- 说明PermissionChecker 即判断事件是否满足权限的处理函数。依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[bool]

说明

PermissionChecker 即判断事件是否满足权限的处理函数。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- DefaultParam: 带有默认值的参数


## varT_Handler​

- 类型:_DependentCallable[Any]
- 说明:Handler 处理函数。

类型:_DependentCallable[Any]

说明:Handler 处理函数。


## varT_TypeUpdater​

- 类型:_DependentCallable[str]
- 说明TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。 默认会更新为message。依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象MatcherParam: Matcher 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[str]

说明

TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。 默认会更新为message。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数


## varT_PermissionUpdater​

- 类型:_DependentCallable[Permission]
- 说明PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。 默认会更新为当前事件的触发对象。依赖参数:DependParam: 子依赖参数BotParam: Bot 对象EventParam: Event 对象StateParam: State 对象MatcherParam: Matcher 对象DefaultParam: 带有默认值的参数

类型:_DependentCallable[Permission]

说明

PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。 默认会更新为当前事件的触发对象。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数


## varT_DependencyCache​

- 类型:dict[_DependentCallable[Any], DependencyCache]
- 说明:依赖缓存, 用于存储依赖函数的返回值

类型:dict[_DependentCallable[Any], DependencyCache]

说明:依赖缓存, 用于存储依赖函数的返回值

# nonebot.matcher

- nonebot.matcher


# nonebot.matcher

本模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行对话。


## varDEFAULT_PROVIDER_CLASS​

- 类型:untyped
- 说明:默认存储器类型

类型:untyped

说明:默认存储器类型


## classMatcher()​

- 说明:事件响应器类
- 参数empty

说明:事件响应器类

参数

empty


### class-vartype​

- 类型:ClassVar[str]
- 说明:事件响应器类型

类型:ClassVar[str]

说明:事件响应器类型


### class-varrule​

- 类型:ClassVar[Rule]
- 说明:事件响应器匹配规则

类型:ClassVar[Rule]

说明:事件响应器匹配规则


### class-varpermission​

- 类型:ClassVar[Permission]
- 说明:事件响应器触发权限

类型:ClassVar[Permission]

说明:事件响应器触发权限


### class-varhandlers​

- 类型:ClassVar[list[Dependent[Any]]]
- 说明:事件响应器拥有的事件处理函数列表

类型:ClassVar[list[Dependent[Any]]]

说明:事件响应器拥有的事件处理函数列表


### class-varpriority​

- 类型:ClassVar[int]
- 说明:事件响应器优先级

类型:ClassVar[int]

说明:事件响应器优先级


### class-varblock​

- 类型:bool
- 说明:事件响应器是否阻止事件传播

类型:bool

说明:事件响应器是否阻止事件传播


### class-vartemp​

- 类型:ClassVar[bool]
- 说明:事件响应器是否为临时

类型:ClassVar[bool]

说明:事件响应器是否为临时


### class-varexpire_time​

- 类型:ClassVar[datetime | None]
- 说明:事件响应器过期时间点

类型:ClassVar[datetime | None]

说明:事件响应器过期时间点


### classmethodnew(type_="", rule=None, permission=None, handlers=None, temp=False, priority=1, block=False, *, plugin=None, module=None, source=None, expire_time=None, default_state=None, default_type_updater=None, default_permission_updater=None)​

- 说明:创建一个新的事件响应器，并存储至matchers <#matchers>_
- 参数type_(str): 事件响应器类型，与event.get_type()一致时触发，空字符串表示任意rule(Rule| None): 匹配规则permission(Permission| None): 权限handlers(list[T_Handler|Dependent[Any]] | None): 事件处理函数列表temp(bool): 是否为临时事件响应器，即触发一次后删除priority(int): 响应优先级block(bool): 是否阻止事件向更低优先级的响应器传播plugin(Plugin| None):Deprecated.事件响应器所在插件module(ModuleType | None):Deprecated.事件响应器所在模块source(MatcherSource | None): 事件响应器源代码上下文信息expire_time(datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除default_state(T_State| None): 默认状态statedefault_type_updater(T_TypeUpdater|Dependent[str] | None): 默认事件类型更新函数default_permission_updater(T_PermissionUpdater|Dependent[Permission] | None): 默认会话权限更新函数
- 返回type[Matcher]: 新的事件响应器类

说明:创建一个新的事件响应器，并存储至matchers <#matchers>_

参数

- type_(str): 事件响应器类型，与event.get_type()一致时触发，空字符串表示任意
- rule(Rule| None): 匹配规则
- permission(Permission| None): 权限
- handlers(list[T_Handler|Dependent[Any]] | None): 事件处理函数列表
- temp(bool): 是否为临时事件响应器，即触发一次后删除
- priority(int): 响应优先级
- block(bool): 是否阻止事件向更低优先级的响应器传播
- plugin(Plugin| None):Deprecated.事件响应器所在插件
- module(ModuleType | None):Deprecated.事件响应器所在模块
- source(MatcherSource | None): 事件响应器源代码上下文信息
- expire_time(datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除
- default_state(T_State| None): 默认状态state
- default_type_updater(T_TypeUpdater|Dependent[str] | None): 默认事件类型更新函数
- default_permission_updater(T_PermissionUpdater|Dependent[Permission] | None): 默认会话权限更新函数

type_(str): 事件响应器类型，与event.get_type()一致时触发，空字符串表示任意

rule(Rule| None): 匹配规则

permission(Permission| None): 权限

handlers(list[T_Handler|Dependent[Any]] | None): 事件处理函数列表

temp(bool): 是否为临时事件响应器，即触发一次后删除

priority(int): 响应优先级

block(bool): 是否阻止事件向更低优先级的响应器传播

plugin(Plugin| None):Deprecated.事件响应器所在插件

module(ModuleType | None):Deprecated.事件响应器所在模块

source(MatcherSource | None): 事件响应器源代码上下文信息

expire_time(datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

default_state(T_State| None): 默认状态state

default_type_updater(T_TypeUpdater|Dependent[str] | None): 默认事件类型更新函数

default_permission_updater(T_PermissionUpdater|Dependent[Permission] | None): 默认会话权限更新函数

返回

- type[Matcher]: 新的事件响应器类


### classmethoddestroy()​

- 说明:销毁当前的事件响应器
- 参数empty
- 返回None

说明:销毁当前的事件响应器

参数

empty

返回

- None


### classmethodcheck_perm(bot, event, stack=None, dependency_cache=None)​

- 说明:检查是否满足触发权限
- 参数bot(Bot): Bot 对象event(Event): 上报事件stack(AsyncExitStack | None): 异步上下文栈dependency_cache(T_DependencyCache| None): 依赖缓存
- 返回bool: 是否满足权限

说明:检查是否满足触发权限

参数

- bot(Bot): Bot 对象
- event(Event): 上报事件
- stack(AsyncExitStack | None): 异步上下文栈
- dependency_cache(T_DependencyCache| None): 依赖缓存

bot(Bot): Bot 对象

event(Event): 上报事件

stack(AsyncExitStack | None): 异步上下文栈

dependency_cache(T_DependencyCache| None): 依赖缓存

返回

- bool: 是否满足权限


### classmethodcheck_rule(bot, event, state, stack=None, dependency_cache=None)​

- 说明:检查是否满足匹配规则
- 参数bot(Bot): Bot 对象event(Event): 上报事件state(T_State): 当前状态stack(AsyncExitStack | None): 异步上下文栈dependency_cache(T_DependencyCache| None): 依赖缓存
- 返回bool: 是否满足匹配规则

说明:检查是否满足匹配规则

参数

- bot(Bot): Bot 对象
- event(Event): 上报事件
- state(T_State): 当前状态
- stack(AsyncExitStack | None): 异步上下文栈
- dependency_cache(T_DependencyCache| None): 依赖缓存

bot(Bot): Bot 对象

event(Event): 上报事件

state(T_State): 当前状态

stack(AsyncExitStack | None): 异步上下文栈

dependency_cache(T_DependencyCache| None): 依赖缓存

返回

- bool: 是否满足匹配规则


### classmethodtype_updater(func)​

- 说明:装饰一个函数来更改当前事件响应器的默认响应事件类型更新函数
- 参数func(T_TypeUpdater): 响应事件类型更新函数
- 返回T_TypeUpdater

说明:装饰一个函数来更改当前事件响应器的默认响应事件类型更新函数

参数

- func(T_TypeUpdater): 响应事件类型更新函数

返回

- T_TypeUpdater


### classmethodpermission_updater(func)​

- 说明:装饰一个函数来更改当前事件响应器的默认会话权限更新函数
- 参数func(T_PermissionUpdater): 会话权限更新函数
- 返回T_PermissionUpdater

说明:装饰一个函数来更改当前事件响应器的默认会话权限更新函数

参数

- func(T_PermissionUpdater): 会话权限更新函数

返回

- T_PermissionUpdater


### classmethodappend_handler(handler, parameterless=None)​

- 参数handler(T_Handler)parameterless(Iterable[Any] | None)
- 返回Dependent[Any]

参数

- handler(T_Handler)
- parameterless(Iterable[Any] | None)

handler(T_Handler)

parameterless(Iterable[Any] | None)

返回

- Dependent[Any]


### classmethodhandle(parameterless=None)​

- 说明:装饰一个函数来向事件响应器直接添加一个处理函数
- 参数parameterless(Iterable[Any] | None): 非参数类型依赖列表
- 返回(T_Handler) ->T_Handler

说明:装饰一个函数来向事件响应器直接添加一个处理函数

参数

- parameterless(Iterable[Any] | None): 非参数类型依赖列表

返回

- (T_Handler) ->T_Handler


### classmethodreceive(id="", parameterless=None)​

- 说明:装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数
- 参数id(str): 消息 IDparameterless(Iterable[Any] | None): 非参数类型依赖列表
- 返回(T_Handler) ->T_Handler

说明:装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数

参数

- id(str): 消息 ID
- parameterless(Iterable[Any] | None): 非参数类型依赖列表

id(str): 消息 ID

parameterless(Iterable[Any] | None): 非参数类型依赖列表

返回

- (T_Handler) ->T_Handler


### classmethodgot(key, prompt=None, parameterless=None)​

- 说明装饰一个函数来指示 NoneBot 获取一个参数key当要获取的key不存在时接收用户新的一条消息再运行该函数，
如果key已存在则直接继续运行
- 参数key(str): 参数名prompt(str |Message|MessageSegment|MessageTemplate| None): 在参数不存在时向用户发送的消息parameterless(Iterable[Any] | None): 非参数类型依赖列表
- 返回(T_Handler) ->T_Handler

说明

装饰一个函数来指示 NoneBot 获取一个参数key

当要获取的key不存在时接收用户新的一条消息再运行该函数，
如果key已存在则直接继续运行

参数

- key(str): 参数名
- prompt(str |Message|MessageSegment|MessageTemplate| None): 在参数不存在时向用户发送的消息
- parameterless(Iterable[Any] | None): 非参数类型依赖列表

key(str): 参数名

prompt(str |Message|MessageSegment|MessageTemplate| None): 在参数不存在时向用户发送的消息

parameterless(Iterable[Any] | None): 非参数类型依赖列表

返回

- (T_Handler) ->T_Handler


### classmethodsend(message, **kwargs)​

- 说明:发送一条消息给当前交互用户
- 参数message(str |Message|MessageSegment|MessageTemplate): 消息内容**kwargs(Any):Bot.send的参数， 请参考对应 adapter 的 bot 对象 api
- 返回Any

说明:发送一条消息给当前交互用户

参数

- message(str |Message|MessageSegment|MessageTemplate): 消息内容
- **kwargs(Any):Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

message(str |Message|MessageSegment|MessageTemplate): 消息内容

**kwargs(Any):Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

返回

- Any


### classmethodfinish(message=None, **kwargs)​

- 说明:发送一条消息给当前交互用户并结束当前事件响应器
- 参数message(str |Message|MessageSegment|MessageTemplate| None): 消息内容**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api
- 返回NoReturn

说明:发送一条消息给当前交互用户并结束当前事件响应器

参数

- message(str |Message|MessageSegment|MessageTemplate| None): 消息内容
- **kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

message(str |Message|MessageSegment|MessageTemplate| None): 消息内容

**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

返回

- NoReturn


### classmethodpause(prompt=None, **kwargs)​

- 说明:发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后继续下一个处理函数
- 参数prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api
- 返回NoReturn

说明:发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后继续下一个处理函数

参数

- prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容
- **kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容

**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

返回

- NoReturn


### classmethodreject(prompt=None, **kwargs)​

- 说明:最近使用got/receive接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数
- 参数prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api
- 返回NoReturn

说明:最近使用got/receive接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

参数

- prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容
- **kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容

**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

返回

- NoReturn


### classmethodreject_arg(key, prompt=None, **kwargs)​

- 说明:最近使用got接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一条消息后从头开始执行当前处理函数
- 参数key(str): 参数名prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api
- 返回NoReturn

说明:最近使用got接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一条消息后从头开始执行当前处理函数

参数

- key(str): 参数名
- prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容
- **kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

key(str): 参数名

prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容

**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

返回

- NoReturn


### classmethodreject_receive(id="", prompt=None, **kwargs)​

- 说明:最近使用receive接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数
- 参数id(str): 消息 idprompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api
- 返回NoReturn

说明:最近使用receive接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

参数

- id(str): 消息 id
- prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容
- **kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

id(str): 消息 id

prompt(str |Message|MessageSegment|MessageTemplate| None): 消息内容

**kwargs:Bot.send的参数， 请参考对应 adapter 的 bot 对象 api

返回

- NoReturn


### classmethodskip()​

- 说明跳过当前事件处理函数，继续下一个处理函数通常在事件处理函数的依赖中使用。
- 参数empty
- 返回NoReturn

说明

跳过当前事件处理函数，继续下一个处理函数

通常在事件处理函数的依赖中使用。

参数

empty

返回

- NoReturn


### methodget_receive(id, default=None)​

- 说明获取一个receive事件如果没有找到对应的事件，返回default值
- 重载1.(id) -> Event | None参数id(str)返回Event| None2.(id, default) -> Event | T参数id(str)default(T)返回Event| T

说明

获取一个receive事件

如果没有找到对应的事件，返回default值

重载

1.(id) -> Event | None

- 参数id(str)
- 返回Event| None

参数

- id(str)

返回

- Event| None

2.(id, default) -> Event | T

- 参数id(str)default(T)
- 返回Event| T

参数

- id(str)
- default(T)

id(str)

default(T)

返回

- Event| T


### methodset_receive(id, event)​

- 说明:设置一个receive事件
- 参数id(str)event(Event)
- 返回None

说明:设置一个receive事件

参数

- id(str)
- event(Event)

id(str)

event(Event)

返回

- None


### methodget_last_receive(default=None)​

- 说明获取最近一次receive事件如果没有事件，返回default值
- 重载1.() -> Event | None参数empty返回Event| None2.(default) -> Event | T参数default(T)返回Event| T

说明

获取最近一次receive事件

如果没有事件，返回default值

重载

1.() -> Event | None

- 参数empty
- 返回Event| None

参数

empty

返回

- Event| None

2.(default) -> Event | T

- 参数default(T)
- 返回Event| T

参数

- default(T)

返回

- Event| T


### methodget_arg(key, default=None)​

- 说明获取一个got消息如果没有找到对应的消息，返回default值
- 重载1.(key) -> Message | None参数key(str)返回Message| None2.(key, default) -> Message | T参数key(str)default(T)返回Message| T

说明

获取一个got消息

如果没有找到对应的消息，返回default值

重载

1.(key) -> Message | None

- 参数key(str)
- 返回Message| None

参数

- key(str)

返回

- Message| None

2.(key, default) -> Message | T

- 参数key(str)default(T)
- 返回Message| T

参数

- key(str)
- default(T)

key(str)

default(T)

返回

- Message| T


### methodset_arg(key, message)​

- 说明:设置一个got消息
- 参数key(str)message(Message)
- 返回None

说明:设置一个got消息

参数

- key(str)
- message(Message)

key(str)

message(Message)

返回

- None


### methodset_target(target, cache=True)​

- 参数target(str)cache(bool)
- 返回None

参数

- target(str)
- cache(bool)

target(str)

cache(bool)

返回

- None


### methodget_target(default=None)​

- 重载1.() -> str | None参数empty返回str | None2.(default) -> str | T参数default(T)返回str | T

重载

1.() -> str | None

- 参数empty
- 返回str | None

参数

empty

返回

- str | None

2.(default) -> str | T

- 参数default(T)
- 返回str | T

参数

- default(T)

返回

- str | T


### methodstop_propagation()​

- 说明:阻止事件传播
- 参数empty
- 返回untyped

说明:阻止事件传播

参数

empty

返回

- untyped


### async methodupdate_type(bot, event, stack=None, dependency_cache=None)​

- 参数bot(Bot)event(Event)stack(AsyncExitStack | None)dependency_cache(T_DependencyCache| None)
- 返回str

参数

- bot(Bot)
- event(Event)
- stack(AsyncExitStack | None)
- dependency_cache(T_DependencyCache| None)

bot(Bot)

event(Event)

stack(AsyncExitStack | None)

dependency_cache(T_DependencyCache| None)

返回

- str


### async methodupdate_permission(bot, event, stack=None, dependency_cache=None)​

- 参数bot(Bot)event(Event)stack(AsyncExitStack | None)dependency_cache(T_DependencyCache| None)
- 返回Permission

参数

- bot(Bot)
- event(Event)
- stack(AsyncExitStack | None)
- dependency_cache(T_DependencyCache| None)

bot(Bot)

event(Event)

stack(AsyncExitStack | None)

dependency_cache(T_DependencyCache| None)

返回

- Permission


### async methodresolve_reject()​

- 参数empty
- 返回untyped

参数

empty

返回

- untyped


### methodensure_context(bot, event)​

- 参数bot(Bot)event(Event)
- 返回untyped

参数

- bot(Bot)
- event(Event)

bot(Bot)

event(Event)

返回

- untyped


### async methodsimple_run(bot, event, state, stack=None, dependency_cache=None)​

- 参数bot(Bot)event(Event)state(T_State)stack(AsyncExitStack | None)dependency_cache(T_DependencyCache| None)
- 返回untyped

参数

- bot(Bot)
- event(Event)
- state(T_State)
- stack(AsyncExitStack | None)
- dependency_cache(T_DependencyCache| None)

bot(Bot)

event(Event)

state(T_State)

stack(AsyncExitStack | None)

dependency_cache(T_DependencyCache| None)

返回

- untyped


### async methodrun(bot, event, state, stack=None, dependency_cache=None)​

- 参数bot(Bot)event(Event)state(T_State)stack(AsyncExitStack | None)dependency_cache(T_DependencyCache| None)
- 返回untyped

参数

- bot(Bot)
- event(Event)
- state(T_State)
- stack(AsyncExitStack | None)
- dependency_cache(T_DependencyCache| None)

bot(Bot)

event(Event)

state(T_State)

stack(AsyncExitStack | None)

dependency_cache(T_DependencyCache| None)

返回

- untyped


## classMatcherManager()​

- 说明事件响应器管理器实现了常用字典操作，用于管理事件响应器。
- 参数empty

说明

事件响应器管理器

实现了常用字典操作，用于管理事件响应器。

参数

empty


### methodkeys()​

- 参数empty
- 返回KeysView[int]

参数

empty

返回

- KeysView[int]


### methodvalues()​

- 参数empty
- 返回ValuesView[list[type[Matcher]]]

参数

empty

返回

- ValuesView[list[type[Matcher]]]


### methoditems()​

- 参数empty
- 返回ItemsView[int, list[type[Matcher]]]

参数

empty

返回

- ItemsView[int, list[type[Matcher]]]


### methodget(key, default=None)​

- 重载1.(key) -> list[type[Matcher]] | None参数key(int)返回list[type[Matcher]] | None2.(key, default) -> list[type[Matcher]]参数key(int)default(list[type[Matcher]])返回list[type[Matcher]]3.(key, default) -> list[type[Matcher]] | T参数key(int)default(T)返回list[type[Matcher]] | T

重载

1.(key) -> list[type[Matcher]] | None

- 参数key(int)
- 返回list[type[Matcher]] | None

参数

- key(int)

返回

- list[type[Matcher]] | None

2.(key, default) -> list[type[Matcher]]

- 参数key(int)default(list[type[Matcher]])
- 返回list[type[Matcher]]

参数

- key(int)
- default(list[type[Matcher]])

key(int)

default(list[type[Matcher]])

返回

- list[type[Matcher]]

3.(key, default) -> list[type[Matcher]] | T

- 参数key(int)default(T)
- 返回list[type[Matcher]] | T

参数

- key(int)
- default(T)

key(int)

default(T)

返回

- list[type[Matcher]] | T


### methodpop(key)​

- 参数key(int)
- 返回list[type[Matcher]]

参数

- key(int)

返回

- list[type[Matcher]]


### methodpopitem()​

- 参数empty
- 返回tuple[int, list[type[Matcher]]]

参数

empty

返回

- tuple[int, list[type[Matcher]]]


### methodclear()​

- 参数empty
- 返回None

参数

empty

返回

- None


### methodupdate(m, /)​

- 参数m(MutableMapping[int, list[type[Matcher]]])
- 返回None

参数

- m(MutableMapping[int, list[type[Matcher]]])

返回

- None


### methodsetdefault(key, default)​

- 参数key(int)default(list[type[Matcher]])
- 返回list[type[Matcher]]

参数

- key(int)
- default(list[type[Matcher]])

key(int)

default(list[type[Matcher]])

返回

- list[type[Matcher]]


### methodset_provider(provider_class)​

- 说明:设置事件响应器存储器
- 参数provider_class(type[MatcherProvider]): 事件响应器存储器类
- 返回None

说明:设置事件响应器存储器

参数

- provider_class(type[MatcherProvider]): 事件响应器存储器类

返回

- None


## abstract classMatcherProvider(matchers)​

- 说明:事件响应器存储器基类
- 参数matchers(Mapping[int, list[type[Matcher]]]): 当前存储器中已有的事件响应器

说明:事件响应器存储器基类

参数

- matchers(Mapping[int, list[type[Matcher]]]): 当前存储器中已有的事件响应器


## varmatchers​

- 类型:untyped

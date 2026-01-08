# nonebot.adapters

- nonebot.adapters


# nonebot.adapters

本模块定义了协议适配基类，各协议请继承以下基类。

使用Driver.register_adapter注册适配器。


## abstract classAdapter(driver, **kwargs)​

- 说明协议适配器基类。通常，在 Adapter 中编写协议通信相关代码，如: 建立通信连接、处理接收与发送 data 等。
- 参数driver(Driver):Driver实例**kwargs(Any): 其他由Driver.register_adapter传入的额外参数

说明

协议适配器基类。

通常，在 Adapter 中编写协议通信相关代码，如: 建立通信连接、处理接收与发送 data 等。

参数

- driver(Driver):Driver实例
- **kwargs(Any): 其他由Driver.register_adapter传入的额外参数

driver(Driver):Driver实例

**kwargs(Any): 其他由Driver.register_adapter传入的额外参数


### instance-vardriver​

- 类型:Driver
- 说明:实例

类型:Driver

说明:实例


### instance-varbots​

- 类型:dict[str,Bot]
- 说明:本协议适配器已建立连接的Bot实例

类型:dict[str,Bot]

说明:本协议适配器已建立连接的Bot实例


### abstract classmethodget_name()​

- 说明:当前协议适配器的名称
- 参数empty
- 返回str

说明:当前协议适配器的名称

参数

empty

返回

- str


### propertyconfig​

- 类型:Config
- 说明:全局 NoneBot 配置

类型:Config

说明:全局 NoneBot 配置


### methodbot_connect(bot)​

- 说明告知 NoneBot 建立了一个新的Bot连接。当有新的Bot实例连接建立成功时调用。
- 参数bot(Bot):Bot实例
- 返回None

说明

告知 NoneBot 建立了一个新的Bot连接。

当有新的Bot实例连接建立成功时调用。

参数

- bot(Bot):Bot实例

返回

- None


### methodbot_disconnect(bot)​

- 说明告知 NoneBotBot连接已断开。当有Bot实例连接断开时调用。
- 参数bot(Bot):Bot实例
- 返回None

说明

告知 NoneBotBot连接已断开。

当有Bot实例连接断开时调用。

参数

- bot(Bot):Bot实例

返回

- None


### methodsetup_http_server(setup)​

- 说明:设置一个 HTTP 服务器路由配置
- 参数setup(HTTPServerSetup)
- 返回untyped

说明:设置一个 HTTP 服务器路由配置

参数

- setup(HTTPServerSetup)

返回

- untyped


### methodsetup_websocket_server(setup)​

- 说明:设置一个 WebSocket 服务器路由配置
- 参数setup(WebSocketServerSetup)
- 返回untyped

说明:设置一个 WebSocket 服务器路由配置

参数

- setup(WebSocketServerSetup)

返回

- untyped


### async methodrequest(setup)​

- 说明:进行一个 HTTP 客户端请求
- 参数setup(Request)
- 返回Response

说明:进行一个 HTTP 客户端请求

参数

- setup(Request)

返回

- Response


### methodwebsocket(setup)​

- 说明:建立一个 WebSocket 客户端连接请求
- 参数setup(Request)
- 返回AsyncGenerator[WebSocket, None]

说明:建立一个 WebSocket 客户端连接请求

参数

- setup(Request)

返回

- AsyncGenerator[WebSocket, None]


### methodon_ready(func)​

- 参数func(LIFESPAN_FUNC)
- 返回LIFESPAN_FUNC

参数

- func(LIFESPAN_FUNC)

返回

- LIFESPAN_FUNC


## abstract classBot(adapter, self_id)​

- 说明Bot 基类。用于处理上报消息，并提供 API 调用接口。
- 参数adapter(Adapter): 协议适配器实例self_id(str): 机器人 ID

说明

Bot 基类。

用于处理上报消息，并提供 API 调用接口。

参数

- adapter(Adapter): 协议适配器实例
- self_id(str): 机器人 ID

adapter(Adapter): 协议适配器实例

self_id(str): 机器人 ID


### instance-varadapter​

- 类型:Adapter
- 说明:协议适配器实例

类型:Adapter

说明:协议适配器实例


### instance-varself_id​

- 类型:str
- 说明:机器人 ID

类型:str

说明:机器人 ID


### propertytype​

- 类型:str
- 说明:协议适配器名称

类型:str

说明:协议适配器名称


### propertyconfig​

- 类型:Config
- 说明:全局 NoneBot 配置

类型:Config

说明:全局 NoneBot 配置


### async methodcall_api(api, **data)​

- 说明:调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用
- 参数api(str): API 名称**data(Any): API 数据
- 返回Any
- 用法awaitbot.call_api("send_msg",message="hello world")awaitbot.send_msg(message="hello world")

说明:调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用

参数

- api(str): API 名称
- **data(Any): API 数据

api(str): API 名称

**data(Any): API 数据

返回

- Any

用法


```python
await bot.call_api("send_msg", message="hello world")await bot.send_msg(message="hello world")
```


### abstract async methodsend(event, message, **kwargs)​

- 说明:调用机器人基础发送消息接口
- 参数event(Event): 上报事件message(str |Message|MessageSegment): 要发送的消息**kwargs(Any): 任意额外参数
- 返回Any

说明:调用机器人基础发送消息接口

参数

- event(Event): 上报事件
- message(str |Message|MessageSegment): 要发送的消息
- **kwargs(Any): 任意额外参数

event(Event): 上报事件

message(str |Message|MessageSegment): 要发送的消息

**kwargs(Any): 任意额外参数

返回

- Any


### classmethodon_calling_api(func)​

- 说明调用 api 预处理。钩子函数参数:bot: 当前 bot 对象api: 调用的 api 名称data: api 调用的参数字典
- 参数func(T_CallingAPIHook)
- 返回T_CallingAPIHook

说明

调用 api 预处理。

钩子函数参数:

- bot: 当前 bot 对象
- api: 调用的 api 名称
- data: api 调用的参数字典

参数

- func(T_CallingAPIHook)

返回

- T_CallingAPIHook


### classmethodon_called_api(func)​

- 说明调用 api 后处理。钩子函数参数:bot: 当前 bot 对象exception: 调用 api 时发生的错误api: 调用的 api 名称data: api 调用的参数字典result: api 调用的返回
- 参数func(T_CalledAPIHook)
- 返回T_CalledAPIHook

说明

调用 api 后处理。

钩子函数参数:

- bot: 当前 bot 对象
- exception: 调用 api 时发生的错误
- api: 调用的 api 名称
- data: api 调用的参数字典
- result: api 调用的返回

参数

- func(T_CalledAPIHook)

返回

- T_CalledAPIHook


## abstract classEvent(<auto>)​

- 说明:Event 基类。提供获取关键信息的方法，其余信息可直接获取。
- 参数auto

说明:Event 基类。提供获取关键信息的方法，其余信息可直接获取。

参数

auto


### abstract methodget_type()​

- 说明:获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。
- 参数empty
- 返回str

说明:获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。

参数

empty

返回

- str


### abstract methodget_event_name()​

- 说明:获取事件名称的方法。
- 参数empty
- 返回str

说明:获取事件名称的方法。

参数

empty

返回

- str


### abstract methodget_event_description()​

- 说明:获取事件描述的方法，通常为事件具体内容。
- 参数empty
- 返回str

说明:获取事件描述的方法，通常为事件具体内容。

参数

empty

返回

- str


### methodget_log_string()​

- 说明获取事件日志信息的方法。通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，
可以抛出NoLogException异常。
- 参数empty
- 返回str
- 异常NoLogException: 希望 NoneBot 隐藏该事件日志

说明

获取事件日志信息的方法。

通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，
可以抛出NoLogException异常。

参数

empty

返回

- str

异常

- NoLogException: 希望 NoneBot 隐藏该事件日志


### abstract methodget_user_id()​

- 说明:获取事件主体 id 的方法，通常是用户 id 。
- 参数empty
- 返回str

说明:获取事件主体 id 的方法，通常是用户 id 。

参数

empty

返回

- str


### abstract methodget_session_id()​

- 说明:获取会话 id 的方法，用于判断当前事件属于哪一个会话， 通常是用户 id、群组 id 组合。
- 参数empty
- 返回str

说明:获取会话 id 的方法，用于判断当前事件属于哪一个会话， 通常是用户 id、群组 id 组合。

参数

empty

返回

- str


### abstract methodget_message()​

- 说明:获取事件消息内容的方法。
- 参数empty
- 返回Message

说明:获取事件消息内容的方法。

参数

empty

返回

- Message


### methodget_plaintext()​

- 说明获取消息纯文本的方法。通常不需要修改，默认通过get_message().extract_plain_text获取。
- 参数empty
- 返回str

说明

获取消息纯文本的方法。

通常不需要修改，默认通过get_message().extract_plain_text获取。

参数

empty

返回

- str


### abstract methodis_tome()​

- 说明:获取事件是否与机器人有关的方法。
- 参数empty
- 返回bool

说明:获取事件是否与机器人有关的方法。

参数

empty

返回

- bool


## abstract classMessage(<auto>)​

- 说明:消息序列
- 参数message: 消息内容

说明:消息序列

参数

- message: 消息内容


### classmethodtemplate(format_string)​

- 说明创建消息模板。用法和str.format大致相同，支持以Message对象作为消息模板并输出消息对象。
并且提供了拓展的格式化控制符，
可以通过该消息类型的MessageSegment工厂方法创建消息。
- 参数format_string(str | TM): 格式化模板
- 返回MessageTemplate[Self]: 消息格式化器

说明

创建消息模板。

用法和str.format大致相同，支持以Message对象作为消息模板并输出消息对象。
并且提供了拓展的格式化控制符，
可以通过该消息类型的MessageSegment工厂方法创建消息。

参数

- format_string(str | TM): 格式化模板

返回

- MessageTemplate[Self]: 消息格式化器


### abstract classmethodget_segment_class()​

- 说明:获取消息段类型
- 参数empty
- 返回type[TMS]

说明:获取消息段类型

参数

empty

返回

- type[TMS]


### abstract staticmethod_construct(msg)​

- 说明:构造消息数组
- 参数msg(str)
- 返回Iterable[TMS]

说明:构造消息数组

参数

- msg(str)

返回

- Iterable[TMS]


### method__getitem__(args)​

- 重载1.(args) -> Self参数args(str): 消息段类型返回Self: 所有类型为args的消息段2.(args) -> TMS参数args(tuple[str, int]): 消息段类型和索引返回TMS: 类型为args[0]的消息段第args[1]个3.(args) -> Self参数args(tuple[str, slice]): 消息段类型和切片返回Self: 类型为args[0]的消息段切片args[1]4.(args) -> TMS参数args(int): 索引返回TMS: 第args个消息段5.(args) -> Self参数args(slice): 切片返回Self: 消息切片args

重载

1.(args) -> Self

- 参数args(str): 消息段类型
- 返回Self: 所有类型为args的消息段

参数

- args(str): 消息段类型

返回

- Self: 所有类型为args的消息段

2.(args) -> TMS

- 参数args(tuple[str, int]): 消息段类型和索引
- 返回TMS: 类型为args[0]的消息段第args[1]个

参数

- args(tuple[str, int]): 消息段类型和索引

返回

- TMS: 类型为args[0]的消息段第args[1]个

3.(args) -> Self

- 参数args(tuple[str, slice]): 消息段类型和切片
- 返回Self: 类型为args[0]的消息段切片args[1]

参数

- args(tuple[str, slice]): 消息段类型和切片

返回

- Self: 类型为args[0]的消息段切片args[1]

4.(args) -> TMS

- 参数args(int): 索引
- 返回TMS: 第args个消息段

参数

- args(int): 索引

返回

- TMS: 第args个消息段

5.(args) -> Self

- 参数args(slice): 切片
- 返回Self: 消息切片args

参数

- args(slice): 切片

返回

- Self: 消息切片args


### method__contains__(value)​

- 说明:检查消息段是否存在
- 参数value(TMS | str): 消息段或消息段类型
- 返回bool: 消息内是否存在给定消息段或给定类型的消息段

说明:检查消息段是否存在

参数

- value(TMS | str): 消息段或消息段类型

返回

- bool: 消息内是否存在给定消息段或给定类型的消息段


### methodhas(value)​

- 说明:与__contains__相同
- 参数value(TMS | str)
- 返回bool

说明:与__contains__相同

参数

- value(TMS | str)

返回

- bool


### methodindex(value, *args)​

- 说明:索引消息段
- 参数value(TMS | str): 消息段或者消息段类型*args(SupportsIndex)arg: start 与 end
- 返回int: 索引 index
- 异常ValueError: 消息段不存在

说明:索引消息段

参数

- value(TMS | str): 消息段或者消息段类型
- *args(SupportsIndex)
- arg: start 与 end

value(TMS | str): 消息段或者消息段类型

*args(SupportsIndex)

arg: start 与 end

返回

- int: 索引 index

异常

- ValueError: 消息段不存在


### methodget(type_, count=None)​

- 说明:获取指定类型的消息段
- 参数type_(str): 消息段类型count(int | None): 获取个数
- 返回Self: 构建的新消息

说明:获取指定类型的消息段

参数

- type_(str): 消息段类型
- count(int | None): 获取个数

type_(str): 消息段类型

count(int | None): 获取个数

返回

- Self: 构建的新消息


### methodcount(value)​

- 说明:计算指定消息段的个数
- 参数value(TMS | str): 消息段或消息段类型
- 返回int: 个数

说明:计算指定消息段的个数

参数

- value(TMS | str): 消息段或消息段类型

返回

- int: 个数


### methodonly(value)​

- 说明:检查消息中是否仅包含指定消息段
- 参数value(TMS | str): 指定消息段或消息段类型
- 返回bool: 是否仅包含指定消息段

说明:检查消息中是否仅包含指定消息段

参数

- value(TMS | str): 指定消息段或消息段类型

返回

- bool: 是否仅包含指定消息段


### methodappend(obj)​

- 说明:添加一个消息段到消息数组末尾。
- 参数obj(str | TMS): 要添加的消息段
- 返回Self

说明:添加一个消息段到消息数组末尾。

参数

- obj(str | TMS): 要添加的消息段

返回

- Self


### methodextend(obj)​

- 说明:拼接一个消息数组或多个消息段到消息数组末尾。
- 参数obj(Self | Iterable[TMS]): 要添加的消息数组
- 返回Self

说明:拼接一个消息数组或多个消息段到消息数组末尾。

参数

- obj(Self | Iterable[TMS]): 要添加的消息数组

返回

- Self


### methodjoin(iterable)​

- 说明:将多个消息连接并将自身作为分割
- 参数iterable(Iterable[TMS | Self]): 要连接的消息
- 返回Self: 连接后的消息

说明:将多个消息连接并将自身作为分割

参数

- iterable(Iterable[TMS | Self]): 要连接的消息

返回

- Self: 连接后的消息


### methodcopy()​

- 说明:深拷贝消息
- 参数empty
- 返回Self

说明:深拷贝消息

参数

empty

返回

- Self


### methodinclude(*types)​

- 说明:过滤消息
- 参数*types(str): 包含的消息段类型
- 返回Self: 新构造的消息

说明:过滤消息

参数

- *types(str): 包含的消息段类型

返回

- Self: 新构造的消息


### methodexclude(*types)​

- 说明:过滤消息
- 参数*types(str): 不包含的消息段类型
- 返回Self: 新构造的消息

说明:过滤消息

参数

- *types(str): 不包含的消息段类型

返回

- Self: 新构造的消息


### methodextract_plain_text()​

- 说明:提取消息内纯文本消息
- 参数empty
- 返回str

说明:提取消息内纯文本消息

参数

empty

返回

- str


## abstract classMessageSegment(<auto>)​

- 说明:消息段基类
- 参数auto

说明:消息段基类

参数

auto


### instance-vartype​

- 类型:str
- 说明:消息段类型

类型:str

说明:消息段类型


### class-vardata​

- 类型:dict[str, Any]
- 说明:消息段数据

类型:dict[str, Any]

说明:消息段数据


### abstract classmethodget_message_class()​

- 说明:获取消息数组类型
- 参数empty
- 返回type[TM]

说明:获取消息数组类型

参数

empty

返回

- type[TM]


### abstract method__str__()​

- 说明:该消息段所代表的 str，在命令匹配部分使用
- 参数empty
- 返回str

说明:该消息段所代表的 str，在命令匹配部分使用

参数

empty

返回

- str


### method__add__(other)​

- 参数other(str | Self | Iterable[Self])
- 返回TM

参数

- other(str | Self | Iterable[Self])

返回

- TM


### methodget(key, default=None)​

- 参数key(str)default(Any)
- 返回untyped

参数

- key(str)
- default(Any)

key(str)

default(Any)

返回

- untyped


### methodkeys()​

- 参数empty
- 返回untyped

参数

empty

返回

- untyped


### methodvalues()​

- 参数empty
- 返回untyped

参数

empty

返回

- untyped


### methoditems()​

- 参数empty
- 返回untyped

参数

empty

返回

- untyped


### methodjoin(iterable)​

- 参数iterable(Iterable[Self | TM])
- 返回TM

参数

- iterable(Iterable[Self | TM])

返回

- TM


### methodcopy()​

- 参数empty
- 返回Self

参数

empty

返回

- Self


### abstract methodis_text()​

- 说明:当前消息段是否为纯文本
- 参数empty
- 返回bool

说明:当前消息段是否为纯文本

参数

empty

返回

- bool


## classMessageTemplate(template, factory=str, private_getattr=False)​

- 说明:消息模板格式化实现类。
- 参数template(str | TM): 模板factory(type[str] | type[TM]): 消息类型工厂，默认为strprivate_getattr(bool): 是否允许在模板中访问私有属性，默认为False

说明:消息模板格式化实现类。

参数

- template(str | TM): 模板
- factory(type[str] | type[TM]): 消息类型工厂，默认为str
- private_getattr(bool): 是否允许在模板中访问私有属性，默认为False

template(str | TM): 模板

factory(type[str] | type[TM]): 消息类型工厂，默认为str

private_getattr(bool): 是否允许在模板中访问私有属性，默认为False


### methodadd_format_spec(spec, name=None)​

- 参数spec(FormatSpecFunc_T)name(str | None)
- 返回FormatSpecFunc_T

参数

- spec(FormatSpecFunc_T)
- name(str | None)

spec(FormatSpecFunc_T)

name(str | None)

返回

- FormatSpecFunc_T


### methodformat(*args, **kwargs)​

- 说明:根据传入参数和模板生成消息对象
- 参数*args**kwargs
- 返回TF

说明:根据传入参数和模板生成消息对象

参数

- *args
- **kwargs

*args

**kwargs

返回

- TF


### methodformat_map(mapping)​

- 说明:根据传入字典和模板生成消息对象, 在传入字段名不是有效标识符时有用
- 参数mapping(Mapping[str, Any])
- 返回TF

说明:根据传入字典和模板生成消息对象, 在传入字段名不是有效标识符时有用

参数

- mapping(Mapping[str, Any])

返回

- TF


### methodvformat(format_string, args, kwargs)​

- 参数format_string(str)args(Sequence[Any])kwargs(Mapping[str, Any])
- 返回TF

参数

- format_string(str)
- args(Sequence[Any])
- kwargs(Mapping[str, Any])

format_string(str)

args(Sequence[Any])

kwargs(Mapping[str, Any])

返回

- TF


### methodget_field(field_name, args, kwargs)​

- 参数field_name(str)args(Sequence[Any])kwargs(Mapping[str, Any])
- 返回tuple[Any, int | str]

参数

- field_name(str)
- args(Sequence[Any])
- kwargs(Mapping[str, Any])

field_name(str)

args(Sequence[Any])

kwargs(Mapping[str, Any])

返回

- tuple[Any, int | str]


### methodformat_field(value, format_spec)​

- 参数value(Any)format_spec(str)
- 返回Any

参数

- value(Any)
- format_spec(str)

value(Any)

format_spec(str)

返回

- Any

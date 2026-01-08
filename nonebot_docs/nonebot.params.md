# nonebot.params

- nonebot.params


# nonebot.params

本模块定义了依赖注入的各类参数。


## defArg(key=None)​

- 说明:Arg 参数消息
- 参数key(str | None)
- 返回Any

说明:Arg 参数消息

参数

- key(str | None)

返回

- Any


## classArgParam(*args, key, type, **kwargs)​

- 说明Arg 注入参数本注入解析事件响应器操作got所获取的参数。可以通过Arg、ArgStr、ArgPlainText等函数参数key指定获取的参数，
留空则会根据参数名称获取。
- 参数*argskey(str)type(Literal['message', 'str', 'plaintext', 'prompt'])**kwargs(Any)

说明

Arg 注入参数

本注入解析事件响应器操作got所获取的参数。

可以通过Arg、ArgStr、ArgPlainText等函数参数key指定获取的参数，
留空则会根据参数名称获取。

参数

- *args
- key(str)
- type(Literal['message', 'str', 'plaintext', 'prompt'])
- **kwargs(Any)

*args

key(str)

type(Literal['message', 'str', 'plaintext', 'prompt'])

**kwargs(Any)


## defArgPlainText(key=None)​

- 说明:Arg 参数消息纯文本
- 参数key(str | None)
- 返回str

说明:Arg 参数消息纯文本

参数

- key(str | None)

返回

- str


## defArgPromptResult(key=None)​

- 说明:argprompt 发送结果
- 参数key(str | None)
- 返回Any

说明:argprompt 发送结果

参数

- key(str | None)

返回

- Any


## defArgStr(key=None)​

- 说明:Arg 参数消息文本
- 参数key(str | None)
- 返回str

说明:Arg 参数消息文本

参数

- key(str | None)

返回

- str


## classBotParam(*args, checker=None, **kwargs)​

- 说明注入参数。本注入解析所有类型为且仅为Bot及其子类或None的参数。为保证兼容性，本注入还会解析名为bot且没有类型注解的参数。
- 参数*argschecker(ModelField| None)**kwargs(Any)

说明

注入参数。

本注入解析所有类型为且仅为Bot及其子类或None的参数。

为保证兼容性，本注入还会解析名为bot且没有类型注解的参数。

参数

- *args
- checker(ModelField| None)
- **kwargs(Any)

*args

checker(ModelField| None)

**kwargs(Any)


## classDefaultParam(*args, validate=False, **kwargs)​

- 说明默认值注入参数本注入解析所有剩余未能解析且具有默认值的参数。本注入参数应该具有最低优先级，因此应该在所有其他注入参数之后使用。
- 参数*argsvalidate(bool)**kwargs(Any)

说明

默认值注入参数

本注入解析所有剩余未能解析且具有默认值的参数。

本注入参数应该具有最低优先级，因此应该在所有其他注入参数之后使用。

参数

- *args
- validate(bool)
- **kwargs(Any)

*args

validate(bool)

**kwargs(Any)


## classDependParam(*args, dependent, use_cache, **kwargs)​

- 说明子依赖注入参数。本注入解析所有子依赖注入，然后将它们的返回值作为参数值传递给父依赖。本注入应该具有最高优先级，因此应该在其他参数之前检查。
- 参数*argsdependent(Dependent[Any])use_cache(bool)**kwargs(Any)

说明

子依赖注入参数。

本注入解析所有子依赖注入，然后将它们的返回值作为参数值传递给父依赖。

本注入应该具有最高优先级，因此应该在其他参数之前检查。

参数

- *args
- dependent(Dependent[Any])
- use_cache(bool)
- **kwargs(Any)

*args

dependent(Dependent[Any])

use_cache(bool)

**kwargs(Any)


## defDepends(dependency=None, *, use_cache=True, validate=False)​

- 说明:子依赖装饰器
- 参数dependency(T_Handler| None): 依赖函数。默认为参数的类型注释。use_cache(bool): 是否使用缓存。默认为True。validate(bool | PydanticFieldInfo): 是否使用 Pydantic 类型校验。默认为False。
- 返回Any
- 用法defdepend_func()->Any:return...defdepend_gen_func():try:yield...finally:...asyncdefhandler(param_name:Any=Depends(depend_func),gen:Any=Depends(depend_gen_func),):...

说明:子依赖装饰器

参数

- dependency(T_Handler| None): 依赖函数。默认为参数的类型注释。
- use_cache(bool): 是否使用缓存。默认为True。
- validate(bool | PydanticFieldInfo): 是否使用 Pydantic 类型校验。默认为False。

dependency(T_Handler| None): 依赖函数。默认为参数的类型注释。

use_cache(bool): 是否使用缓存。默认为True。

validate(bool | PydanticFieldInfo): 是否使用 Pydantic 类型校验。默认为False。

返回

- Any

用法


```python
def depend_func() -> Any:    return ...def depend_gen_func():    try:        yield ...    finally:        ...async def handler(    param_name: Any = Depends(depend_func),    gen: Any = Depends(depend_gen_func),):    ...
```


## classEventParam(*args, checker=None, **kwargs)​

- 说明注入参数本注入解析所有类型为且仅为Event及其子类或None的参数。为保证兼容性，本注入还会解析名为event且没有类型注解的参数。
- 参数*argschecker(ModelField| None)**kwargs(Any)

说明

注入参数

本注入解析所有类型为且仅为Event及其子类或None的参数。

为保证兼容性，本注入还会解析名为event且没有类型注解的参数。

参数

- *args
- checker(ModelField| None)
- **kwargs(Any)

*args

checker(ModelField| None)

**kwargs(Any)


## classExceptionParam(*args, validate=False, **kwargs)​

- 说明的异常注入参数本注入解析所有类型为Exception或None的参数。为保证兼容性，本注入还会解析名为exception且没有类型注解的参数。
- 参数*argsvalidate(bool)**kwargs(Any)

说明

的异常注入参数

本注入解析所有类型为Exception或None的参数。

为保证兼容性，本注入还会解析名为exception且没有类型注解的参数。

参数

- *args
- validate(bool)
- **kwargs(Any)

*args

validate(bool)

**kwargs(Any)


## classMatcherParam(*args, checker=None, **kwargs)​

- 说明事件响应器实例注入参数本注入解析所有类型为且仅为Matcher及其子类或None的参数。为保证兼容性，本注入还会解析名为matcher且没有类型注解的参数。
- 参数*argschecker(ModelField| None)**kwargs(Any)

说明

事件响应器实例注入参数

本注入解析所有类型为且仅为Matcher及其子类或None的参数。

为保证兼容性，本注入还会解析名为matcher且没有类型注解的参数。

参数

- *args
- checker(ModelField| None)
- **kwargs(Any)

*args

checker(ModelField| None)

**kwargs(Any)


## classStateParam(*args, validate=False, **kwargs)​

- 说明事件处理状态注入参数本注入解析所有类型为T_State的参数。为保证兼容性，本注入还会解析名为state且没有类型注解的参数。
- 参数*argsvalidate(bool)**kwargs(Any)

说明

事件处理状态注入参数

本注入解析所有类型为T_State的参数。

为保证兼容性，本注入还会解析名为state且没有类型注解的参数。

参数

- *args
- validate(bool)
- **kwargs(Any)

*args

validate(bool)

**kwargs(Any)


## defEventType()​

- 说明:类型参数
- 参数empty
- 返回str

说明:类型参数

参数

empty

返回

- str


## defEventMessage()​

- 说明:消息参数
- 参数empty
- 返回Any

说明:消息参数

参数

empty

返回

- Any


## defEventPlainText()​

- 说明:纯文本消息参数
- 参数empty
- 返回str

说明:纯文本消息参数

参数

empty

返回

- str


## defEventToMe()​

- 说明:to_me参数
- 参数empty
- 返回bool

说明:to_me参数

参数

empty

返回

- bool


## defCommand()​

- 说明:消息命令元组
- 参数empty
- 返回tuple[str, ...]

说明:消息命令元组

参数

empty

返回

- tuple[str, ...]


## defRawCommand()​

- 说明:消息命令文本
- 参数empty
- 返回str

说明:消息命令文本

参数

empty

返回

- str


## defCommandArg()​

- 说明:消息命令参数
- 参数empty
- 返回Any

说明:消息命令参数

参数

empty

返回

- Any


## defCommandStart()​

- 说明:消息命令开头
- 参数empty
- 返回str

说明:消息命令开头

参数

empty

返回

- str


## defCommandWhitespace()​

- 说明:消息命令与参数之间的空白
- 参数empty
- 返回str

说明:消息命令与参数之间的空白

参数

empty

返回

- str


## defShellCommandArgs()​

- 说明:shell 命令解析后的参数字典
- 参数empty
- 返回Any

说明:shell 命令解析后的参数字典

参数

empty

返回

- Any


## defShellCommandArgv()​

- 说明:shell 命令原始参数列表
- 参数empty
- 返回Any

说明:shell 命令原始参数列表

参数

empty

返回

- Any


## defRegexMatched()​

- 说明:正则匹配结果
- 参数empty
- 返回Match[str]

说明:正则匹配结果

参数

empty

返回

- Match[str]


## defRegexStr(*groups)​

- 说明:正则匹配结果文本
- 重载1.(group, /) -> str参数group(Literal[0])返回str2.(group, /) -> str | Any参数group(str | int)返回str | Any3.(group1, group2, /, *groups) -> tuple[str | Any, ...]参数group1(str | int)group2(str | int)*groups(str | int)返回tuple[str | Any, ...]

说明:正则匹配结果文本

重载

1.(group, /) -> str

- 参数group(Literal[0])
- 返回str

参数

- group(Literal[0])

返回

- str

2.(group, /) -> str | Any

- 参数group(str | int)
- 返回str | Any

参数

- group(str | int)

返回

- str | Any

3.(group1, group2, /, *groups) -> tuple[str | Any, ...]

- 参数group1(str | int)group2(str | int)*groups(str | int)
- 返回tuple[str | Any, ...]

参数

- group1(str | int)
- group2(str | int)
- *groups(str | int)

group1(str | int)

group2(str | int)

*groups(str | int)

返回

- tuple[str | Any, ...]


## defRegexGroup()​

- 说明:正则匹配结果 group 元组
- 参数empty
- 返回tuple[Any, ...]

说明:正则匹配结果 group 元组

参数

empty

返回

- tuple[Any, ...]


## defRegexDict()​

- 说明:正则匹配结果 group 字典
- 参数empty
- 返回dict[str, Any]

说明:正则匹配结果 group 字典

参数

empty

返回

- dict[str, Any]


## defStartswith()​

- 说明:响应触发前缀
- 参数empty
- 返回str

说明:响应触发前缀

参数

empty

返回

- str


## defEndswith()​

- 说明:响应触发后缀
- 参数empty
- 返回str

说明:响应触发后缀

参数

empty

返回

- str


## defFullmatch()​

- 说明:响应触发完整消息
- 参数empty
- 返回str

说明:响应触发完整消息

参数

empty

返回

- str


## defKeyword()​

- 说明:响应触发关键字
- 参数empty
- 返回str

说明:响应触发关键字

参数

empty

返回

- str


## defReceived(id=None, default=None)​

- 说明:receive事件参数
- 参数id(str | None)default(Any)
- 返回Any

说明:receive事件参数

参数

- id(str | None)
- default(Any)

id(str | None)

default(Any)

返回

- Any


## defLastReceived(default=None)​

- 说明:last_receive事件参数
- 参数default(Any)
- 返回Any

说明:last_receive事件参数

参数

- default(Any)

返回

- Any


## defReceivePromptResult(id=None)​

- 说明:receiveprompt 发送结果
- 参数id(str | None)
- 返回Any

说明:receiveprompt 发送结果

参数

- id(str | None)

返回

- Any


## defPausePromptResult()​

- 说明:pauseprompt 发送结果
- 参数empty
- 返回Any

说明:pauseprompt 发送结果

参数

empty

返回

- Any

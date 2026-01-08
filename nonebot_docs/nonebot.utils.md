# nonebot.utils

- nonebot.utils


# nonebot.utils

本模块包含了 NoneBot 的一些工具函数


## defescape_tag(s)​

- 说明用于记录带颜色日志时转义<tag>类型特殊标签参考:loguru color 标签
- 参数s(str): 需要转义的字符串
- 返回str

说明

用于记录带颜色日志时转义<tag>类型特殊标签

参考:loguru color 标签

参数

- s(str): 需要转义的字符串

返回

- str


## defdeep_update(mapping, *updating_mappings)​

- 说明:深度更新合并字典
- 参数mapping(dict[K, Any])*updating_mappings(dict[K, Any])
- 返回dict[K, Any]

说明:深度更新合并字典

参数

- mapping(dict[K, Any])
- *updating_mappings(dict[K, Any])

mapping(dict[K, Any])

*updating_mappings(dict[K, Any])

返回

- dict[K, Any]


## deflenient_issubclass(cls, class_or_tuple)​

- 说明:检查 cls 是否是 class_or_tuple 中的一个类型子类并忽略类型错误。
- 参数cls(Any)class_or_tuple(type[Any] | tuple[type[Any], ...])
- 返回bool

说明:检查 cls 是否是 class_or_tuple 中的一个类型子类并忽略类型错误。

参数

- cls(Any)
- class_or_tuple(type[Any] | tuple[type[Any], ...])

cls(Any)

class_or_tuple(type[Any] | tuple[type[Any], ...])

返回

- bool


## defgeneric_check_issubclass(cls, class_or_tuple)​

- 说明检查 cls 是否是 class_or_tuple 中的一个类型子类。特别的：如果 cls 是typing.TypeVar类型，
则会检查其__bound__或__constraints__是否是 class_or_tuple 中一个类型的子类或 None。如果 cls 是typing.Union或types.UnionType类型，
则会检查其中的所有类型是否是 class_or_tuple 中一个类型的子类或 None。如果 cls 是typing.Literal类型，
则会检查其中的所有值是否是 class_or_tuple 中一个类型的实例。如果 cls 是typing.List、typing.Dict等泛型类型，
则会检查其原始类型是否是 class_or_tuple 中一个类型的子类。
- 参数cls(Any)class_or_tuple(type[Any] | tuple[type[Any], ...])
- 返回bool

说明

检查 cls 是否是 class_or_tuple 中的一个类型子类。

特别的：

- 如果 cls 是typing.TypeVar类型，
则会检查其__bound__或__constraints__是否是 class_or_tuple 中一个类型的子类或 None。
- 如果 cls 是typing.Union或types.UnionType类型，
则会检查其中的所有类型是否是 class_or_tuple 中一个类型的子类或 None。
- 如果 cls 是typing.Literal类型，
则会检查其中的所有值是否是 class_or_tuple 中一个类型的实例。
- 如果 cls 是typing.List、typing.Dict等泛型类型，
则会检查其原始类型是否是 class_or_tuple 中一个类型的子类。

参数

- cls(Any)
- class_or_tuple(type[Any] | tuple[type[Any], ...])

cls(Any)

class_or_tuple(type[Any] | tuple[type[Any], ...])

返回

- bool


## deftype_is_complex(type_)​

- 说明:检查 type_ 是否是复杂类型
- 参数type_(type[Any])
- 返回bool

说明:检查 type_ 是否是复杂类型

参数

- type_(type[Any])

返回

- bool


## defis_coroutine_callable(call)​

- 说明:检查 call 是否是一个 callable 协程函数
- 参数call((...) -> Any)
- 返回bool

说明:检查 call 是否是一个 callable 协程函数

参数

- call((...) -> Any)

返回

- bool


## defis_gen_callable(call)​

- 说明:检查 call 是否是一个生成器函数
- 参数call((...) -> Any)
- 返回bool

说明:检查 call 是否是一个生成器函数

参数

- call((...) -> Any)

返回

- bool


## defis_async_gen_callable(call)​

- 说明:检查 call 是否是一个异步生成器函数
- 参数call((...) -> Any)
- 返回bool

说明:检查 call 是否是一个异步生成器函数

参数

- call((...) -> Any)

返回

- bool


## defrun_sync(call)​

- 说明:一个用于包装 sync function 为 async function 的装饰器
- 参数call((P) -> R): 被装饰的同步函数
- 返回(P) -> Coroutine[None, None, R]

说明:一个用于包装 sync function 为 async function 的装饰器

参数

- call((P) -> R): 被装饰的同步函数

返回

- (P) -> Coroutine[None, None, R]


## defrun_sync_ctx_manager(cm)​

- 说明:一个用于包装 sync context manager 为 async context manager 的执行函数
- 参数cm(AbstractContextManager[T])
- 返回AsyncGenerator[T, None]

说明:一个用于包装 sync context manager 为 async context manager 的执行函数

参数

- cm(AbstractContextManager[T])

返回

- AsyncGenerator[T, None]


## async defrun_coro_with_catch(coro, exc, return_on_err=None)​

- 说明:运行协程并当遇到指定异常时返回指定值。
- 重载1.(coro, exc, return_on_err=None) -> T | None参数coro(Coroutine[Any, Any, T])exc(tuple[type[Exception], ...])return_on_err(None)返回T | None2.(coro, exc, return_on_err) -> T | R参数coro(Coroutine[Any, Any, T])exc(tuple[type[Exception], ...])return_on_err(R)返回T | R
- 参数coro: 要运行的协程exc: 要捕获的异常return_on_err: 当发生异常时返回的值
- 返回协程的返回值或发生异常时的指定值

说明:运行协程并当遇到指定异常时返回指定值。

重载

1.(coro, exc, return_on_err=None) -> T | None

- 参数coro(Coroutine[Any, Any, T])exc(tuple[type[Exception], ...])return_on_err(None)
- 返回T | None

参数

- coro(Coroutine[Any, Any, T])
- exc(tuple[type[Exception], ...])
- return_on_err(None)

coro(Coroutine[Any, Any, T])

exc(tuple[type[Exception], ...])

return_on_err(None)

返回

- T | None

2.(coro, exc, return_on_err) -> T | R

- 参数coro(Coroutine[Any, Any, T])exc(tuple[type[Exception], ...])return_on_err(R)
- 返回T | R

参数

- coro(Coroutine[Any, Any, T])
- exc(tuple[type[Exception], ...])
- return_on_err(R)

coro(Coroutine[Any, Any, T])

exc(tuple[type[Exception], ...])

return_on_err(R)

返回

- T | R

参数

- coro: 要运行的协程
- exc: 要捕获的异常
- return_on_err: 当发生异常时返回的值

coro: 要运行的协程

exc: 要捕获的异常

return_on_err: 当发生异常时返回的值

返回

协程的返回值或发生异常时的指定值


## async defrun_coro_with_shield(coro)​

- 说明:运行协程并在取消时屏蔽取消异常。
- 参数coro(Coroutine[Any, Any, T]): 要运行的协程
- 返回T: 协程的返回值

说明:运行协程并在取消时屏蔽取消异常。

参数

- coro(Coroutine[Any, Any, T]): 要运行的协程

返回

- T: 协程的返回值


## defflatten_exception_group(exc_group)​

- 参数exc_group(BaseExceptionGroup[E])
- 返回Generator[E, None, None]

参数

- exc_group(BaseExceptionGroup[E])

返回

- Generator[E, None, None]


## defget_name(obj)​

- 说明:获取对象的名称
- 参数obj(Any)
- 返回str

说明:获取对象的名称

参数

- obj(Any)

返回

- str


## defpath_to_module_name(path)​

- 说明:转换路径为模块名
- 参数path(Path)
- 返回str

说明:转换路径为模块名

参数

- path(Path)

返回

- str


## defresolve_dot_notation(obj_str, default_attr, default_prefix=None)​

- 说明:解析并导入点分表示法的对象
- 参数obj_str(str)default_attr(str)default_prefix(str | None)
- 返回Any

说明:解析并导入点分表示法的对象

参数

- obj_str(str)
- default_attr(str)
- default_prefix(str | None)

obj_str(str)

default_attr(str)

default_prefix(str | None)

返回

- Any


## classclassproperty(func)​

- 说明:类属性装饰器
- 参数func((Any) -> T)

说明:类属性装饰器

参数

- func((Any) -> T)


## classDataclassEncoder(<auto>)​

- 说明:可以序列化Message(List[Dataclass]) 的JSONEncoder
- 参数auto

说明:可以序列化Message(List[Dataclass]) 的JSONEncoder

参数

auto


### methoddefault(o)​

- 参数o
- 返回untyped

参数

- o

返回

- untyped


## deflogger_wrapper(logger_name)​

- 说明:用于打印 adapter 的日志。
- 参数logger_name(str): adapter 的名称
- 返回untyped: 日志记录函数日志记录函数的参数:level: 日志等级message: 日志信息exception: 异常信息

说明:用于打印 adapter 的日志。

参数

- logger_name(str): adapter 的名称

返回

- untyped: 日志记录函数日志记录函数的参数:level: 日志等级message: 日志信息exception: 异常信息

untyped: 日志记录函数

日志记录函数的参数:

- level: 日志等级
- message: 日志信息
- exception: 异常信息

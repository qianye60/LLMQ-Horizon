# nonebot.dependencies

- nonebot.dependencies


# nonebot.dependencies

本模块模块实现了依赖注入的定义与处理。


## abstract classParam(*args, validate=False, **kwargs)​

- 说明依赖注入的基本单元 —— 参数。继承自pydantic.fields.FieldInfo，用于描述参数信息（不包括参数名）。
- 参数*argsvalidate(bool)**kwargs(Any)

说明

依赖注入的基本单元 —— 参数。

继承自pydantic.fields.FieldInfo，用于描述参数信息（不包括参数名）。

参数

- *args
- validate(bool)
- **kwargs(Any)

*args

validate(bool)

**kwargs(Any)


## classDependent(<auto>)​

- 说明:依赖注入容器
- 参数call: 依赖注入的可调用对象，可以是任何 Callable 对象pre_checkers: 依赖注入解析前的参数检查params: 具名参数列表parameterless: 匿名参数列表allow_types: 允许的参数类型

说明:依赖注入容器

参数

- call: 依赖注入的可调用对象，可以是任何 Callable 对象
- pre_checkers: 依赖注入解析前的参数检查
- params: 具名参数列表
- parameterless: 匿名参数列表
- allow_types: 允许的参数类型

call: 依赖注入的可调用对象，可以是任何 Callable 对象

pre_checkers: 依赖注入解析前的参数检查

params: 具名参数列表

parameterless: 匿名参数列表

allow_types: 允许的参数类型


### staticmethodparse_params(call, allow_types)​

- 参数call(_DependentCallable[R])allow_types(tuple[type[Param], ...])
- 返回tuple[ModelField, ...]

参数

- call(_DependentCallable[R])
- allow_types(tuple[type[Param], ...])

call(_DependentCallable[R])

allow_types(tuple[type[Param], ...])

返回

- tuple[ModelField, ...]


### staticmethodparse_parameterless(parameterless, allow_types)​

- 参数parameterless(tuple[Any, ...])allow_types(tuple[type[Param], ...])
- 返回tuple[Param, ...]

参数

- parameterless(tuple[Any, ...])
- allow_types(tuple[type[Param], ...])

parameterless(tuple[Any, ...])

allow_types(tuple[type[Param], ...])

返回

- tuple[Param, ...]


### classmethodparse(*, call, parameterless=None, allow_types)​

- 参数call(_DependentCallable[R])parameterless(Iterable[Any] | None)allow_types(Iterable[type[Param]])
- 返回Dependent[R]

参数

- call(_DependentCallable[R])
- parameterless(Iterable[Any] | None)
- allow_types(Iterable[type[Param]])

call(_DependentCallable[R])

parameterless(Iterable[Any] | None)

allow_types(Iterable[type[Param]])

返回

- Dependent[R]


### async methodcheck(**params)​

- 参数**params(Any)
- 返回None

参数

- **params(Any)

返回

- None


### async methodsolve(**params)​

- 参数**params(Any)
- 返回dict[str, Any]

参数

- **params(Any)

返回

- dict[str, Any]

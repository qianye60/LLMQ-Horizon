# nonebot

- nonebot


# nonebot

本模块主要定义了 NoneBot 启动所需函数，供 bot 入口文件调用。


## 快捷导入​

为方便使用，本模块从子模块导入了部分内容，以下内容可以直接通过本模块导入:

- on=>on
- on_metaevent=>on_metaevent
- on_message=>on_message
- on_notice=>on_notice
- on_request=>on_request
- on_startswith=>on_startswith
- on_endswith=>on_endswith
- on_fullmatch=>on_fullmatch
- on_keyword=>on_keyword
- on_command=>on_command
- on_shell_command=>on_shell_command
- on_regex=>on_regex
- on_type=>on_type
- CommandGroup=>CommandGroup
- Matchergroup=>MatcherGroup
- load_plugin=>load_plugin
- load_plugins=>load_plugins
- load_all_plugins=>load_all_plugins
- load_from_json=>load_from_json
- load_from_toml=>load_from_toml
- load_builtin_plugin=>load_builtin_plugin
- load_builtin_plugins=>load_builtin_plugins
- get_plugin=>get_plugin
- get_plugin_by_module_name=>get_plugin_by_module_name
- get_loaded_plugins=>get_loaded_plugins
- get_available_plugin_names=>get_available_plugin_names
- get_plugin_config=>get_plugin_config
- require=>require


## defget_driver()​

- 说明获取全局Driver实例。可用于在计划任务的回调等情形中获取当前Driver实例。
- 参数empty
- 返回Driver: 全局Driver对象
- 异常ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法driver=nonebot.get_driver()

说明

获取全局Driver实例。

可用于在计划任务的回调等情形中获取当前Driver实例。

参数

empty

返回

- Driver: 全局Driver对象

异常

- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
driver = nonebot.get_driver()
```


## defget_adapter(name)​

- 说明:获取已注册的Adapter实例。
- 重载1.(name) -> Adapter参数name(str): 适配器名称返回Adapter: 指定名称的Adapter对象2.(name) -> A参数name(type[A]): 适配器类型返回A: 指定类型的Adapter对象
- 异常ValueError: 指定的Adapter未注册ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法fromnonebot.adapters.consoleimportAdapteradapter=nonebot.get_adapter(Adapter)

说明:获取已注册的Adapter实例。

重载

1.(name) -> Adapter

- 参数name(str): 适配器名称
- 返回Adapter: 指定名称的Adapter对象

参数

- name(str): 适配器名称

返回

- Adapter: 指定名称的Adapter对象

2.(name) -> A

- 参数name(type[A]): 适配器类型
- 返回A: 指定类型的Adapter对象

参数

- name(type[A]): 适配器类型

返回

- A: 指定类型的Adapter对象

异常

- ValueError: 指定的Adapter未注册
- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

ValueError: 指定的Adapter未注册

ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
from nonebot.adapters.console import Adapteradapter = nonebot.get_adapter(Adapter)
```


## defget_adapters()​

- 说明:获取所有已注册的Adapter实例。
- 参数empty
- 返回dict[str,Adapter]: 所有Adapter实例字典
- 异常ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法adapters=nonebot.get_adapters()

说明:获取所有已注册的Adapter实例。

参数

empty

返回

- dict[str,Adapter]: 所有Adapter实例字典

异常

- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
adapters = nonebot.get_adapters()
```


## defget_app()​

- 说明:获取全局ASGIMixin对应的 Server App 对象。
- 参数empty
- 返回Any: Server App 对象
- 异常AssertionError: 全局 Driver 对象不是ASGIMixin类型ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法app=nonebot.get_app()

说明:获取全局ASGIMixin对应的 Server App 对象。

参数

empty

返回

- Any: Server App 对象

异常

- AssertionError: 全局 Driver 对象不是ASGIMixin类型
- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

AssertionError: 全局 Driver 对象不是ASGIMixin类型

ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
app = nonebot.get_app()
```


## defget_asgi()​

- 说明:获取全局ASGIMixin对应的ASGI对象。
- 参数empty
- 返回Any: ASGI 对象
- 异常AssertionError: 全局 Driver 对象不是ASGIMixin类型ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法asgi=nonebot.get_asgi()

说明:获取全局ASGIMixin对应的ASGI对象。

参数

empty

返回

- Any: ASGI 对象

异常

- AssertionError: 全局 Driver 对象不是ASGIMixin类型
- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

AssertionError: 全局 Driver 对象不是ASGIMixin类型

ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
asgi = nonebot.get_asgi()
```


## defget_bot(self_id=None)​

- 说明获取一个连接到 NoneBot 的Bot对象。当提供self_id时，此函数是get_bots()[self_id]的简写；
当不提供时，返回一个Bot。
- 参数self_id(str | None): 用来识别Bot的Bot.self_id属性
- 返回Bot:Bot对象
- 异常KeyError: 对应 self_id 的 Bot 不存在ValueError: 没有传入 self_id 且没有 Bot 可用ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法assertnonebot.get_bot("12345")==nonebot.get_bots()["12345"]another_unspecified_bot=nonebot.get_bot()

说明

获取一个连接到 NoneBot 的Bot对象。

当提供self_id时，此函数是get_bots()[self_id]的简写；
当不提供时，返回一个Bot。

参数

- self_id(str | None): 用来识别Bot的Bot.self_id属性

返回

- Bot:Bot对象

异常

- KeyError: 对应 self_id 的 Bot 不存在
- ValueError: 没有传入 self_id 且没有 Bot 可用
- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

KeyError: 对应 self_id 的 Bot 不存在

ValueError: 没有传入 self_id 且没有 Bot 可用

ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
assert nonebot.get_bot("12345") == nonebot.get_bots()["12345"]another_unspecified_bot = nonebot.get_bot()
```


## defget_bots()​

- 说明:获取所有连接到 NoneBot 的Bot对象。
- 参数empty
- 返回dict[str,Bot]: 一个以Bot.self_id为键Bot对象为值的字典
- 异常ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)
- 用法bots=nonebot.get_bots()

说明:获取所有连接到 NoneBot 的Bot对象。

参数

empty

返回

- dict[str,Bot]: 一个以Bot.self_id为键Bot对象为值的字典

dict[str,Bot]: 一个以Bot.self_id为键

Bot对象为值的字典

异常

- ValueError: 全局Driver对象尚未初始化 (nonebot.init尚未调用)

用法


```python
bots = nonebot.get_bots()
```


## definit(*, _env_file=None, **kwargs)​

- 说明初始化 NoneBot 以及 全局Driver对象。NoneBot 将会从 .env 文件中读取环境信息，并使用相应的 env 文件配置。也可以传入自定义的_env_file来指定 NoneBot 从该文件读取配置。
- 参数_env_file(DOTENV_TYPE | None): 配置文件名，默认从.env.{env_name}中读取配置**kwargs(Any): 任意变量，将会存储到Driver.config对象里
- 返回None
- 用法nonebot.init(database=Database(...))

说明

初始化 NoneBot 以及 全局Driver对象。

NoneBot 将会从 .env 文件中读取环境信息，并使用相应的 env 文件配置。

也可以传入自定义的_env_file来指定 NoneBot 从该文件读取配置。

参数

- _env_file(DOTENV_TYPE | None): 配置文件名，默认从.env.{env_name}中读取配置
- **kwargs(Any): 任意变量，将会存储到Driver.config对象里

_env_file(DOTENV_TYPE | None): 配置文件名，默认从.env.{env_name}中读取配置

**kwargs(Any): 任意变量，将会存储到Driver.config对象里

返回

- None

用法


```python
nonebot.init(database=Database(...))
```


## defrun(*args, **kwargs)​

- 说明:启动 NoneBot，即运行全局Driver对象。
- 参数*args(Any): 传入Driver.run的位置参数**kwargs(Any): 传入Driver.run的命名参数
- 返回None
- 用法nonebot.run(host="127.0.0.1",port=8080)

说明:启动 NoneBot，即运行全局Driver对象。

参数

- *args(Any): 传入Driver.run的位置参数
- **kwargs(Any): 传入Driver.run的命名参数

*args(Any): 传入Driver.run的位置参数

**kwargs(Any): 传入Driver.run的命名参数

返回

- None

用法


```python
nonebot.run(host="127.0.0.1", port=8080)
```

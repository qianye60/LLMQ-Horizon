# nonebot.config

- nonebot.config


# nonebot.config

本模块定义了 NoneBot 本身运行所需的配置项。

NoneBot 使用pydantic以及python-dotenv来读取配置。

配置项需符合特殊格式或 json 序列化格式
详情见pydantic Field Type文档。


## classEnv(_env_file=ENV_FILE_SENTINEL, _env_file_encoding=None, _env_nested_delimiter=None, **values)​

- 说明运行环境配置。大小写不敏感。将会从环境变量>dotenv 配置文件的优先级读取环境信息。
- 参数_env_file(DOTENV_TYPE | None)_env_file_encoding(str | None)_env_nested_delimiter(str | None)**values(Any)

说明

运行环境配置。大小写不敏感。

将会从环境变量>dotenv 配置文件的优先级读取环境信息。

参数

- _env_file(DOTENV_TYPE | None)
- _env_file_encoding(str | None)
- _env_nested_delimiter(str | None)
- **values(Any)

_env_file(DOTENV_TYPE | None)

_env_file_encoding(str | None)

_env_nested_delimiter(str | None)

**values(Any)


### class-varenvironment​

- 类型:str
- 说明当前环境名。NoneBot 将从.env.{environment}文件中加载配置。

类型:str

说明

当前环境名。

NoneBot 将从.env.{environment}文件中加载配置。


## classConfig(_env_file=ENV_FILE_SENTINEL, _env_file_encoding=None, _env_nested_delimiter=None, **values)​

- 说明NoneBot 主要配置。大小写不敏感。除了 NoneBot 的配置项外，还可以自行添加配置项到.env.{environment}文件中。
这些配置将会在 json 反序列化后一起带入Config类中。配置方法参考:配置
- 参数_env_file(DOTENV_TYPE | None)_env_file_encoding(str | None)_env_nested_delimiter(str | None)**values(Any)

说明

NoneBot 主要配置。大小写不敏感。

除了 NoneBot 的配置项外，还可以自行添加配置项到.env.{environment}文件中。
这些配置将会在 json 反序列化后一起带入Config类中。

配置方法参考:配置

参数

- _env_file(DOTENV_TYPE | None)
- _env_file_encoding(str | None)
- _env_nested_delimiter(str | None)
- **values(Any)

_env_file(DOTENV_TYPE | None)

_env_file_encoding(str | None)

_env_nested_delimiter(str | None)

**values(Any)


### class-vardriver​

- 类型:str
- 说明NoneBot 运行所使用的Driver。继承自Driver。配置格式为<module>[:<Driver>][+<module>[:<Mixin>]]*。~为nonebot.drivers.的缩写。配置方法参考:配置驱动器

类型:str

说明

NoneBot 运行所使用的Driver。继承自Driver。

配置格式为<module>[:<Driver>][+<module>[:<Mixin>]]*。

~为nonebot.drivers.的缩写。

配置方法参考:配置驱动器


### class-varhost​

- 类型:IPvAnyAddress
- 说明:NoneBotReverseDriver服务端监听的 IP/主机名。

类型:IPvAnyAddress

说明:NoneBotReverseDriver服务端监听的 IP/主机名。


### class-varport​

- 类型:int
- 说明:NoneBotReverseDriver服务端监听的端口。

类型:int

说明:NoneBotReverseDriver服务端监听的端口。


### class-varlog_level​

- 类型:int | str
- 说明NoneBot 日志输出等级，可以为int类型等级或等级名称。参考记录日志，loguru 日志等级。提示日志等级名称应为大写，如INFO。
- 用法LOG_LEVEL=25LOG_LEVEL=INFO

类型:int | str

说明

NoneBot 日志输出等级，可以为int类型等级或等级名称。

参考记录日志，loguru 日志等级。

日志等级名称应为大写，如INFO。

用法


```python
LOG_LEVEL=25LOG_LEVEL=INFO
```


### class-varapi_timeout​

- 类型:float | None
- 说明:API 请求超时时间，单位: 秒。

类型:float | None

说明:API 请求超时时间，单位: 秒。


### class-varsuperusers​

- 类型:set[str]
- 说明:机器人超级用户。
- 用法SUPERUSERS=["12345789"]

类型:set[str]

说明:机器人超级用户。

用法


```python
SUPERUSERS=["12345789"]
```


### class-varnickname​

- 类型:set[str]
- 说明:机器人昵称。

类型:set[str]

说明:机器人昵称。


### class-varcommand_start​

- 类型:set[str]
- 说明命令的起始标记，用于判断一条消息是不是命令。参考命令响应规则。
- 用法COMMAND_START=["/", ""]

类型:set[str]

说明

命令的起始标记，用于判断一条消息是不是命令。

参考命令响应规则。

用法


```python
COMMAND_START=["/", ""]
```


### class-varcommand_sep​

- 类型:set[str]
- 说明命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。参考命令响应规则。
- 用法COMMAND_SEP=["."]

类型:set[str]

说明

命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。

参考命令响应规则。

用法


```python
COMMAND_SEP=["."]
```


### class-varsession_expire_timeout​

- 类型:timedelta
- 说明:等待用户回复的超时时间。
- 用法SESSION_EXPIRE_TIMEOUT=[-][DD]D[,][HH:MM:]SS[.ffffff]SESSION_EXPIRE_TIMEOUT=[±]P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601

类型:timedelta

说明:等待用户回复的超时时间。

用法


```python
SESSION_EXPIRE_TIMEOUT=[-][DD]D[,][HH:MM:]SS[.ffffff]SESSION_EXPIRE_TIMEOUT=[±]P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601
```

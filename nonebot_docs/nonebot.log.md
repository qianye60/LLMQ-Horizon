# nonebot.log

- nonebot.log


# nonebot.log

本模块定义了 NoneBot 的日志记录 Logger。

NoneBot 使用loguru来记录日志信息。

自定义 logger 请参考自定义日志以及loguru文档。


## varlogger​

- 类型:Logger
- 说明NoneBot 日志记录器对象。默认信息:格式:[%(asctime)s %(name)s] %(levelname)s: %(message)s等级:INFO，根据config.log_level配置改变输出: 输出至 stdout
- 用法fromnonebot.logimportlogger

类型:Logger

说明

NoneBot 日志记录器对象。

默认信息:

- 格式:[%(asctime)s %(name)s] %(levelname)s: %(message)s
- 等级:INFO，根据config.log_level配置改变
- 输出: 输出至 stdout

用法


```python
from nonebot.log import logger
```


## classLoguruHandler(<auto>)​

- 说明:logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。
- 参数auto

说明:logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。

参数

auto


### methodemit(record)​

- 参数record(logging.LogRecord)
- 返回untyped

参数

- record(logging.LogRecord)

返回

- untyped


## defdefault_filter(record)​

- 说明:默认的日志过滤器，根据config.log_level配置改变日志等级。
- 参数record(Record)
- 返回untyped

说明:默认的日志过滤器，根据config.log_level配置改变日志等级。

参数

- record(Record)

返回

- untyped


## vardefault_format​

- 类型:str
- 说明:默认日志格式

类型:str

说明:默认日志格式

# nonebot.exception

- nonebot.exception


# nonebot.exception

本模块包含了所有 NoneBot 运行时可能会抛出的异常。

这些异常并非所有需要用户处理，在 NoneBot 内部运行时被捕获，并进行对应操作。


```python
NoneBotException├── ParserExit├── ProcessException|   ├── IgnoredException|   ├── SkippedException|   |   └── TypeMisMatch|   ├── MockApiException|   └── StopPropagation├── MatcherException|   ├── PausedException|   ├── RejectedException|   └── FinishedException├── AdapterException|   ├── NoLogException|   ├── ApiNotAvailable|   ├── NetworkError|   └── ActionFailed└── DriverException    └── WebSocketClosed
```


## classNoneBotException(<auto>)​

- 说明:所有 NoneBot 发生的异常基类。
- 参数auto

说明:所有 NoneBot 发生的异常基类。

参数

auto


## classParserExit(<auto>)​

- 说明:处理消息失败时返回的异常。
- 参数auto

说明:处理消息失败时返回的异常。

参数

auto


## classProcessException(<auto>)​

- 说明:事件处理过程中发生的异常基类。
- 参数auto

说明:事件处理过程中发生的异常基类。

参数

auto


## classIgnoredException(<auto>)​

- 说明:指示 NoneBot 应该忽略该事件。可由 PreProcessor 抛出。
- 参数reason: 忽略事件的原因

说明:指示 NoneBot 应该忽略该事件。可由 PreProcessor 抛出。

参数

- reason: 忽略事件的原因


## classSkippedException(<auto>)​

- 说明指示 NoneBot 立即结束当前Dependent的运行。例如，可以在Handler中通过Matcher.skip抛出。
- 参数auto
- 用法defalways_skip():Matcher.skip()@matcher.handle()asyncdefhandler(dependency=Depends(always_skip)):# never run

说明

指示 NoneBot 立即结束当前Dependent的运行。

例如，可以在Handler中通过Matcher.skip抛出。

参数

auto

用法


```python
def always_skip():    Matcher.skip()@matcher.handle()async def handler(dependency = Depends(always_skip)):    # never run
```


## classTypeMisMatch(<auto>)​

- 说明:当前Handler的参数类型不匹配。
- 参数auto

说明:当前Handler的参数类型不匹配。

参数

auto


## classMockApiException(<auto>)​

- 说明:指示 NoneBot 阻止本次 API 调用或修改本次调用返回值，并返回自定义内容。 可由 api hook 抛出。
- 参数result: 返回的内容

说明:指示 NoneBot 阻止本次 API 调用或修改本次调用返回值，并返回自定义内容。 可由 api hook 抛出。

参数

- result: 返回的内容


## classStopPropagation(<auto>)​

- 说明指示 NoneBot 终止事件向下层传播。在Matcher.block为True或使用Matcher.stop_propagation方法时抛出。
- 参数auto
- 用法matcher=on_notice(block=True)# 或者@matcher.handle()asyncdefhandler(matcher:Matcher):matcher.stop_propagation()

说明

指示 NoneBot 终止事件向下层传播。

在Matcher.block为True或使用Matcher.stop_propagation方法时抛出。

参数

auto

用法


```python
matcher = on_notice(block=True)# 或者@matcher.handle()async def handler(matcher: Matcher):    matcher.stop_propagation()
```


## classMatcherException(<auto>)​

- 说明:所有 Matcher 发生的异常基类。
- 参数auto

说明:所有 Matcher 发生的异常基类。

参数

auto


## classPausedException(<auto>)​

- 说明指示 NoneBot 结束当前Handler并等待下一条消息后继续下一个Handler。 可用于用户输入新信息。可以在Handler中通过Matcher.pause抛出。
- 参数auto
- 用法@matcher.handle()asyncdefhandler():awaitmatcher.pause("some message")

说明

指示 NoneBot 结束当前Handler并等待下一条消息后继续下一个Handler。 可用于用户输入新信息。

可以在Handler中通过Matcher.pause抛出。

参数

auto

用法


```python
@matcher.handle()async def handler():    await matcher.pause("some message")
```


## classRejectedException(<auto>)​

- 说明指示 NoneBot 结束当前Handler并等待下一条消息后重新运行当前Handler。 可用于用户重新输入。可以在Handler中通过Matcher.reject抛出。
- 参数auto
- 用法@matcher.handle()asyncdefhandler():awaitmatcher.reject("some message")

说明

指示 NoneBot 结束当前Handler并等待下一条消息后重新运行当前Handler。 可用于用户重新输入。

可以在Handler中通过Matcher.reject抛出。

参数

auto

用法


```python
@matcher.handle()async def handler():    await matcher.reject("some message")
```


## classFinishedException(<auto>)​

- 说明指示 NoneBot 结束当前Handler且后续Handler不再被运行。可用于结束用户会话。可以在Handler中通过Matcher.finish抛出。
- 参数auto
- 用法@matcher.handle()asyncdefhandler():awaitmatcher.finish("some message")

说明

指示 NoneBot 结束当前Handler且后续Handler不再被运行。可用于结束用户会话。

可以在Handler中通过Matcher.finish抛出。

参数

auto

用法


```python
@matcher.handle()async def handler():    await matcher.finish("some message")
```


## classAdapterException(<auto>)​

- 说明:代表Adapter抛出的异常，所有的Adapter都要在内部继承自这个Exception。
- 参数adapter_name: 标识 adapter

说明:代表Adapter抛出的异常，所有的Adapter都要在内部继承自这个Exception。

参数

- adapter_name: 标识 adapter


## classNoLogException(<auto>)​

- 说明指示 NoneBot 对当前Event进行处理但不显示 Log 信息。可在Event.get_log_string时抛出
- 参数auto

说明

指示 NoneBot 对当前Event进行处理但不显示 Log 信息。

可在Event.get_log_string时抛出

参数

auto


## classApiNotAvailable(<auto>)​

- 说明:在 API 连接不可用时抛出。
- 参数auto

说明:在 API 连接不可用时抛出。

参数

auto


## classNetworkError(<auto>)​

- 说明:在网络出现问题时抛出， 如: API 请求地址不正确, API 请求无返回或返回状态非正常等。
- 参数auto

说明:在网络出现问题时抛出， 如: API 请求地址不正确, API 请求无返回或返回状态非正常等。

参数

auto


## classActionFailed(<auto>)​

- 说明:API 请求成功返回数据，但 API 操作失败。
- 参数auto

说明:API 请求成功返回数据，但 API 操作失败。

参数

auto


## classDriverException(<auto>)​

- 说明:Driver抛出的异常基类。
- 参数auto

说明:Driver抛出的异常基类。

参数

auto


## classWebSocketClosed(<auto>)​

- 说明:WebSocket 连接已关闭。
- 参数auto

说明:WebSocket 连接已关闭。

参数

auto

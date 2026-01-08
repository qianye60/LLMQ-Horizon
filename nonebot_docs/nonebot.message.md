# nonebot.message

- nonebot.message


# nonebot.message

本模块定义了事件处理主要流程。

NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。


## defevent_preprocessor(func)​

- 说明事件预处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。
- 参数func(T_EventPreProcessor)
- 返回T_EventPreProcessor

说明

事件预处理。

装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。

参数

- func(T_EventPreProcessor)

返回

- T_EventPreProcessor


## defevent_postprocessor(func)​

- 说明事件后处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。
- 参数func(T_EventPostProcessor)
- 返回T_EventPostProcessor

说明

事件后处理。

装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。

参数

- func(T_EventPostProcessor)

返回

- T_EventPostProcessor


## defrun_preprocessor(func)​

- 说明运行预处理。装饰一个函数，使它在每次事件响应器运行前执行。
- 参数func(T_RunPreProcessor)
- 返回T_RunPreProcessor

说明

运行预处理。

装饰一个函数，使它在每次事件响应器运行前执行。

参数

- func(T_RunPreProcessor)

返回

- T_RunPreProcessor


## defrun_postprocessor(func)​

- 说明运行后处理。装饰一个函数，使它在每次事件响应器运行后执行。
- 参数func(T_RunPostProcessor)
- 返回T_RunPostProcessor

说明

运行后处理。

装饰一个函数，使它在每次事件响应器运行后执行。

参数

- func(T_RunPostProcessor)

返回

- T_RunPostProcessor


## async defcheck_and_run_matcher(Matcher, bot, event, state, stack=None, dependency_cache=None)​

- 说明:检查并运行事件响应器。
- 参数Matcher(type[Matcher]): 事件响应器bot(Bot): Bot 对象event(Event): Event 对象state(T_State): 会话状态stack(AsyncExitStack | None): 异步上下文栈dependency_cache(T_DependencyCache| None): 依赖缓存
- 返回None

说明:检查并运行事件响应器。

参数

- Matcher(type[Matcher]): 事件响应器
- bot(Bot): Bot 对象
- event(Event): Event 对象
- state(T_State): 会话状态
- stack(AsyncExitStack | None): 异步上下文栈
- dependency_cache(T_DependencyCache| None): 依赖缓存

Matcher(type[Matcher]): 事件响应器

bot(Bot): Bot 对象

event(Event): Event 对象

state(T_State): 会话状态

stack(AsyncExitStack | None): 异步上下文栈

dependency_cache(T_DependencyCache| None): 依赖缓存

返回

- None


## async defhandle_event(bot, event)​

- 说明:处理一个事件。调用该函数以实现分发事件。
- 参数bot(Bot): Bot 对象event(Event): Event 对象
- 返回None
- 用法driver.task_group.start_soon(handle_event,bot,event)

说明:处理一个事件。调用该函数以实现分发事件。

参数

- bot(Bot): Bot 对象
- event(Event): Event 对象

bot(Bot): Bot 对象

event(Event): Event 对象

返回

- None

用法


```python
driver.task_group.start_soon(handle_event, bot, event)
```

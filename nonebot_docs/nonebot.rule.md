# nonebot.rule

- nonebot.rule


# nonebot.rule

本模块是Matcher.rule的类型定义。

每个事件响应器拥有一个Rule，其中是RuleChecker的集合。
只有当所有RuleChecker检查结果为True时继续运行。


## classRule(*checkers)​

- 说明规则类。当事件传递时，在Matcher运行前进行检查。
- 参数*checkers(T_RuleChecker|Dependent[bool]): RuleChecker
- 用法Rule(async_function)&sync_function# 等价于Rule(async_function,sync_function)

说明

规则类。

当事件传递时，在Matcher运行前进行检查。

参数

- *checkers(T_RuleChecker|Dependent[bool]): RuleChecker

用法


```python
Rule(async_function) & sync_function# 等价于Rule(async_function, sync_function)
```


### instance-varcheckers​

- 类型:set[Dependent[bool]]
- 说明:存储RuleChecker

类型:set[Dependent[bool]]

说明:存储RuleChecker


### async method__call__(bot, event, state, stack=None, dependency_cache=None)​

- 说明:检查是否符合所有规则
- 参数bot(Bot): Bot 对象event(Event): Event 对象state(T_State): 当前 Statestack(AsyncExitStack | None): 异步上下文栈dependency_cache(T_DependencyCache| None): 依赖缓存
- 返回bool

说明:检查是否符合所有规则

参数

- bot(Bot): Bot 对象
- event(Event): Event 对象
- state(T_State): 当前 State
- stack(AsyncExitStack | None): 异步上下文栈
- dependency_cache(T_DependencyCache| None): 依赖缓存

bot(Bot): Bot 对象

event(Event): Event 对象

state(T_State): 当前 State

stack(AsyncExitStack | None): 异步上下文栈

dependency_cache(T_DependencyCache| None): 依赖缓存

返回

- bool


## classCMD_RESULT(<auto>)​

- 参数auto

参数

auto


## classTRIE_VALUE(<auto>)​

- 说明:TRIE_VALUE(command_start, command)
- 参数auto

说明:TRIE_VALUE(command_start, command)

参数

auto


## classStartswithRule(msg, ignorecase=False)​

- 说明:检查消息纯文本是否以指定字符串开头。
- 参数msg(tuple[str, ...]): 指定消息开头字符串元组ignorecase(bool): 是否忽略大小写

说明:检查消息纯文本是否以指定字符串开头。

参数

- msg(tuple[str, ...]): 指定消息开头字符串元组
- ignorecase(bool): 是否忽略大小写

msg(tuple[str, ...]): 指定消息开头字符串元组

ignorecase(bool): 是否忽略大小写


## defstartswith(msg, ignorecase=False)​

- 说明:匹配消息纯文本开头。
- 参数msg(str | tuple[str, ...]): 指定消息开头字符串元组ignorecase(bool): 是否忽略大小写
- 返回Rule

说明:匹配消息纯文本开头。

参数

- msg(str | tuple[str, ...]): 指定消息开头字符串元组
- ignorecase(bool): 是否忽略大小写

msg(str | tuple[str, ...]): 指定消息开头字符串元组

ignorecase(bool): 是否忽略大小写

返回

- Rule


## classEndswithRule(msg, ignorecase=False)​

- 说明:检查消息纯文本是否以指定字符串结尾。
- 参数msg(tuple[str, ...]): 指定消息结尾字符串元组ignorecase(bool): 是否忽略大小写

说明:检查消息纯文本是否以指定字符串结尾。

参数

- msg(tuple[str, ...]): 指定消息结尾字符串元组
- ignorecase(bool): 是否忽略大小写

msg(tuple[str, ...]): 指定消息结尾字符串元组

ignorecase(bool): 是否忽略大小写


## defendswith(msg, ignorecase=False)​

- 说明:匹配消息纯文本结尾。
- 参数msg(str | tuple[str, ...]): 指定消息开头字符串元组ignorecase(bool): 是否忽略大小写
- 返回Rule

说明:匹配消息纯文本结尾。

参数

- msg(str | tuple[str, ...]): 指定消息开头字符串元组
- ignorecase(bool): 是否忽略大小写

msg(str | tuple[str, ...]): 指定消息开头字符串元组

ignorecase(bool): 是否忽略大小写

返回

- Rule


## classFullmatchRule(msg, ignorecase=False)​

- 说明:检查消息纯文本是否与指定字符串全匹配。
- 参数msg(tuple[str, ...]): 指定消息全匹配字符串元组ignorecase(bool): 是否忽略大小写

说明:检查消息纯文本是否与指定字符串全匹配。

参数

- msg(tuple[str, ...]): 指定消息全匹配字符串元组
- ignorecase(bool): 是否忽略大小写

msg(tuple[str, ...]): 指定消息全匹配字符串元组

ignorecase(bool): 是否忽略大小写


## deffullmatch(msg, ignorecase=False)​

- 说明:完全匹配消息。
- 参数msg(str | tuple[str, ...]): 指定消息全匹配字符串元组ignorecase(bool): 是否忽略大小写
- 返回Rule

说明:完全匹配消息。

参数

- msg(str | tuple[str, ...]): 指定消息全匹配字符串元组
- ignorecase(bool): 是否忽略大小写

msg(str | tuple[str, ...]): 指定消息全匹配字符串元组

ignorecase(bool): 是否忽略大小写

返回

- Rule


## classKeywordsRule(*keywords)​

- 说明:检查消息纯文本是否包含指定关键字。
- 参数*keywords(str): 指定关键字元组

说明:检查消息纯文本是否包含指定关键字。

参数

- *keywords(str): 指定关键字元组


## defkeyword(*keywords)​

- 说明:匹配消息纯文本关键词。
- 参数*keywords(str): 指定关键字元组
- 返回Rule

说明:匹配消息纯文本关键词。

参数

- *keywords(str): 指定关键字元组

返回

- Rule


## classCommandRule(cmds, force_whitespace=None)​

- 说明:检查消息是否为指定命令。
- 参数cmds(list[tuple[str, ...]]): 指定命令元组列表force_whitespace(str | bool | None): 是否强制命令后必须有指定空白符

说明:检查消息是否为指定命令。

参数

- cmds(list[tuple[str, ...]]): 指定命令元组列表
- force_whitespace(str | bool | None): 是否强制命令后必须有指定空白符

cmds(list[tuple[str, ...]]): 指定命令元组列表

force_whitespace(str | bool | None): 是否强制命令后必须有指定空白符


## defcommand(*cmds, force_whitespace=None)​

- 说明匹配消息命令。根据配置里提供的command_start,command_sep判断消息是否为命令。可以通过Command获取匹配成功的命令（例:("test",)），
通过RawCommand获取匹配成功的原始命令文本（例:"/test"），
通过CommandArg获取匹配成功的命令参数。
- 参数*cmds(str | tuple[str, ...]): 命令文本或命令元组force_whitespace(str | bool | None): 是否强制命令后必须有指定空白符
- 返回Rule
- 用法使用默认command_start,command_sep配置情况下：命令("test",)可以匹配:/test开头的消息
命令("test", "sub")可以匹配:/test.sub开头的消息

说明

匹配消息命令。

根据配置里提供的command_start,command_sep判断消息是否为命令。

可以通过Command获取匹配成功的命令（例:("test",)），
通过RawCommand获取匹配成功的原始命令文本（例:"/test"），
通过CommandArg获取匹配成功的命令参数。

参数

- *cmds(str | tuple[str, ...]): 命令文本或命令元组
- force_whitespace(str | bool | None): 是否强制命令后必须有指定空白符

*cmds(str | tuple[str, ...]): 命令文本或命令元组

force_whitespace(str | bool | None): 是否强制命令后必须有指定空白符

返回

- Rule

用法

使用默认command_start,command_sep配置情况下：

命令("test",)可以匹配:/test开头的消息
命令("test", "sub")可以匹配:/test.sub开头的消息

命令内容与后续消息间无需空格!


## classArgumentParser(<auto>)​

- 说明shell_like命令参数解析器，解析出错时不会退出程序。支持Message富文本解析。
- 参数auto
- 用法用法与argparse.ArgumentParser相同，
参考文档:argparse

说明

shell_like命令参数解析器，解析出错时不会退出程序。

支持Message富文本解析。

参数

auto

用法

用法与argparse.ArgumentParser相同，
参考文档:argparse


### methodparse_known_args(args=None, namespace=None)​

- 重载1.(args=None, namespace=None) -> tuple[Namespace, list[str | MessageSegment]]参数args(Sequence[str |MessageSegment] | None)namespace(None)返回tuple[Namespace, list[str |MessageSegment]]2.(args, namespace) -> tuple[T, list[str | MessageSegment]]参数args(Sequence[str |MessageSegment] | None)namespace(T)返回tuple[T, list[str |MessageSegment]]3.(*, namespace) -> tuple[T, list[str | MessageSegment]]参数namespace(T)返回tuple[T, list[str |MessageSegment]]

重载

1.(args=None, namespace=None) -> tuple[Namespace, list[str | MessageSegment]]

- 参数args(Sequence[str |MessageSegment] | None)namespace(None)
- 返回tuple[Namespace, list[str |MessageSegment]]

参数

- args(Sequence[str |MessageSegment] | None)
- namespace(None)

args(Sequence[str |MessageSegment] | None)

namespace(None)

返回

- tuple[Namespace, list[str |MessageSegment]]

2.(args, namespace) -> tuple[T, list[str | MessageSegment]]

- 参数args(Sequence[str |MessageSegment] | None)namespace(T)
- 返回tuple[T, list[str |MessageSegment]]

参数

- args(Sequence[str |MessageSegment] | None)
- namespace(T)

args(Sequence[str |MessageSegment] | None)

namespace(T)

返回

- tuple[T, list[str |MessageSegment]]

3.(*, namespace) -> tuple[T, list[str | MessageSegment]]

- 参数namespace(T)
- 返回tuple[T, list[str |MessageSegment]]

参数

- namespace(T)

返回

- tuple[T, list[str |MessageSegment]]


## classShellCommandRule(cmds, parser)​

- 说明:检查消息是否为指定 shell 命令。
- 参数cmds(list[tuple[str, ...]]): 指定命令元组列表parser(ArgumentParser | None): 可选参数解析器

说明:检查消息是否为指定 shell 命令。

参数

- cmds(list[tuple[str, ...]]): 指定命令元组列表
- parser(ArgumentParser | None): 可选参数解析器

cmds(list[tuple[str, ...]]): 指定命令元组列表

parser(ArgumentParser | None): 可选参数解析器


## defshell_command(*cmds, parser=None)​

- 说明匹配shell_like形式的消息命令。根据配置里提供的command_start,command_sep判断消息是否为命令。可以通过Command获取匹配成功的命令
（例:("test",)），
通过RawCommand获取匹配成功的原始命令文本
（例:"/test"），
通过ShellCommandArgv获取解析前的参数列表
（例:["arg", "-h"]），
通过ShellCommandArgs获取解析后的参数字典
（例:{"arg": "arg", "h": True}）。警告如果参数解析失败，则通过ShellCommandArgs获取的将是ParserExit异常。
- 参数*cmds(str | tuple[str, ...]): 命令文本或命令元组parser(ArgumentParser | None):ArgumentParser对象
- 返回Rule
- 用法使用默认command_start,command_sep配置，更多示例参考argparse标准库文档。fromnonebot.ruleimportArgumentParserparser=ArgumentParser()parser.add_argument("-a",action="store_true")rule=shell_command("ls",parser=parser)

说明

匹配shell_like形式的消息命令。

根据配置里提供的command_start,command_sep判断消息是否为命令。

可以通过Command获取匹配成功的命令
（例:("test",)），
通过RawCommand获取匹配成功的原始命令文本
（例:"/test"），
通过ShellCommandArgv获取解析前的参数列表
（例:["arg", "-h"]），
通过ShellCommandArgs获取解析后的参数字典
（例:{"arg": "arg", "h": True}）。

如果参数解析失败，则通过ShellCommandArgs获取的将是ParserExit异常。

参数

- *cmds(str | tuple[str, ...]): 命令文本或命令元组
- parser(ArgumentParser | None):ArgumentParser对象

*cmds(str | tuple[str, ...]): 命令文本或命令元组

parser(ArgumentParser | None):ArgumentParser对象

返回

- Rule

用法

使用默认command_start,command_sep配置，更多示例参考argparse标准库文档。


```python
from nonebot.rule import ArgumentParserparser = ArgumentParser()parser.add_argument("-a", action="store_true")rule = shell_command("ls", parser=parser)
```

命令内容与后续消息间无需空格!


## classRegexRule(regex, flags=0)​

- 说明:检查消息字符串是否符合指定正则表达式。
- 参数regex(str): 正则表达式flags(int): 正则表达式标记

说明:检查消息字符串是否符合指定正则表达式。

参数

- regex(str): 正则表达式
- flags(int): 正则表达式标记

regex(str): 正则表达式

flags(int): 正则表达式标记


## defregex(regex, flags=0)​

- 说明匹配符合正则表达式的消息字符串。可以通过RegexStr获取匹配成功的字符串，
通过RegexGroup获取匹配成功的 group 元组，
通过RegexDict获取匹配成功的 group 字典。
- 参数regex(str): 正则表达式flags(int | re.RegexFlag): 正则表达式标记
- 返回Rule

说明

匹配符合正则表达式的消息字符串。

可以通过RegexStr获取匹配成功的字符串，
通过RegexGroup获取匹配成功的 group 元组，
通过RegexDict获取匹配成功的 group 字典。

参数

- regex(str): 正则表达式
- flags(int | re.RegexFlag): 正则表达式标记

regex(str): 正则表达式

flags(int | re.RegexFlag): 正则表达式标记

返回

- Rule

正则表达式匹配使用 search 而非 match，如需从头匹配请使用r"^xxx"来确保匹配开头

正则表达式匹配使用EventMessage的str字符串，
而非EventMessage的PlainText纯文本字符串


## classToMeRule(<auto>)​

- 说明:检查事件是否与机器人有关。
- 参数auto

说明:检查事件是否与机器人有关。

参数

auto


## defto_me()​

- 说明:匹配与机器人有关的事件。
- 参数empty
- 返回Rule

说明:匹配与机器人有关的事件。

参数

empty

返回

- Rule


## classIsTypeRule(*types)​

- 说明:检查事件类型是否为指定类型。
- 参数*types(type[Event])

说明:检查事件类型是否为指定类型。

参数

- *types(type[Event])


## defis_type(*types)​

- 说明:匹配事件类型。
- 参数*types(type[Event]): 事件类型
- 返回Rule

说明:匹配事件类型。

参数

- *types(type[Event]): 事件类型

返回

- Rule

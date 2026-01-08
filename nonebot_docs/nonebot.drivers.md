# nonebot.drivers

- nonebot.drivers


# nonebot.drivers

本模块定义了驱动适配器基类。

各驱动请继承以下基类。


## abstract classASGIMixin(<auto>)​

- 说明ASGI 服务端基类。将后端框架封装，以满足适配器使用。
- 参数auto

说明

ASGI 服务端基类。

将后端框架封装，以满足适配器使用。

参数

auto


### abstract propertyserver_app​

- 类型:Any
- 说明:驱动 APP 对象

类型:Any

说明:驱动 APP 对象


### abstract propertyasgi​

- 类型:Any
- 说明:驱动 ASGI 对象

类型:Any

说明:驱动 ASGI 对象


### abstract methodsetup_http_server(setup)​

- 说明:设置一个 HTTP 服务器路由配置
- 参数setup(HTTPServerSetup)
- 返回None

说明:设置一个 HTTP 服务器路由配置

参数

- setup(HTTPServerSetup)

返回

- None


### abstract methodsetup_websocket_server(setup)​

- 说明:设置一个 WebSocket 服务器路由配置
- 参数setup(WebSocketServerSetup)
- 返回None

说明:设置一个 WebSocket 服务器路由配置

参数

- setup(WebSocketServerSetup)

返回

- None


## classCookies(cookies=None)​

- 参数cookies(CookieTypes)

- cookies(CookieTypes)


### methodset(name, value, domain="", path="/")​

- 参数name(str)value(str)domain(str)path(str)
- 返回None

参数

- name(str)
- value(str)
- domain(str)
- path(str)

name(str)

value(str)

domain(str)

path(str)

返回

- None


### methodget(name, default=None, domain=None, path=None)​

- 参数name(str)default(str | None)domain(str | None)path(str | None)
- 返回str | None

参数

- name(str)
- default(str | None)
- domain(str | None)
- path(str | None)

name(str)

default(str | None)

domain(str | None)

path(str | None)

返回

- str | None


### methoddelete(name, domain=None, path=None)​

- 参数name(str)domain(str | None)path(str | None)
- 返回None

参数

- name(str)
- domain(str | None)
- path(str | None)

name(str)

domain(str | None)

path(str | None)

返回

- None


### methodclear(domain=None, path=None)​

- 参数domain(str | None)path(str | None)
- 返回None

参数

- domain(str | None)
- path(str | None)

domain(str | None)

path(str | None)

返回

- None


### methodupdate(cookies=None)​

- 参数cookies(CookieTypes)
- 返回None

参数

- cookies(CookieTypes)

返回

- None


### methodas_header(request)​

- 参数request(Request)
- 返回dict[str, str]

参数

- request(Request)

返回

- dict[str, str]


## abstract classDriver(env, config)​

- 说明驱动器基类。驱动器控制框架的启动和停止，适配器的注册，以及机器人生命周期管理。
- 参数env(Env): 包含环境信息的 Env 对象config(Config): 包含配置信息的 Config 对象

说明

驱动器基类。

驱动器控制框架的启动和停止，适配器的注册，以及机器人生命周期管理。

参数

- env(Env): 包含环境信息的 Env 对象
- config(Config): 包含配置信息的 Config 对象

env(Env): 包含环境信息的 Env 对象

config(Config): 包含配置信息的 Config 对象


### instance-varenv​

- 类型:str
- 说明:环境名称

类型:str

说明:环境名称


### instance-varconfig​

- 类型:Config
- 说明:全局配置对象

类型:Config

说明:全局配置对象


### propertybots​

- 类型:dict[str,Bot]
- 说明:获取当前所有已连接的 Bot

类型:dict[str,Bot]

说明:获取当前所有已连接的 Bot


### methodregister_adapter(adapter, **kwargs)​

- 说明:注册一个协议适配器
- 参数adapter(type[Adapter]): 适配器类**kwargs: 其他传递给适配器的参数
- 返回None

说明:注册一个协议适配器

参数

- adapter(type[Adapter]): 适配器类
- **kwargs: 其他传递给适配器的参数

adapter(type[Adapter]): 适配器类

**kwargs: 其他传递给适配器的参数

返回

- None


### abstract propertytype​

- 类型:str
- 说明:驱动类型名称

类型:str

说明:驱动类型名称


### abstract propertylogger​

- 类型:untyped
- 说明:驱动专属 logger 日志记录器

类型:untyped

说明:驱动专属 logger 日志记录器


### abstract methodrun(*args, **kwargs)​

- 说明:启动驱动框架
- 参数*args**kwargs
- 返回untyped

说明:启动驱动框架

参数

- *args
- **kwargs

*args

**kwargs

返回

- untyped


### methodon_startup(func)​

- 说明:注册一个启动时执行的函数
- 参数func(LIFESPAN_FUNC)
- 返回LIFESPAN_FUNC

说明:注册一个启动时执行的函数

参数

- func(LIFESPAN_FUNC)

返回

- LIFESPAN_FUNC


### methodon_shutdown(func)​

- 说明:注册一个停止时执行的函数
- 参数func(LIFESPAN_FUNC)
- 返回LIFESPAN_FUNC

说明:注册一个停止时执行的函数

参数

- func(LIFESPAN_FUNC)

返回

- LIFESPAN_FUNC


### classmethodon_bot_connect(func)​

- 说明装饰一个函数使他在 bot 连接成功时执行。钩子函数参数:bot: 当前连接上的 Bot 对象
- 参数func(T_BotConnectionHook)
- 返回T_BotConnectionHook

说明

装饰一个函数使他在 bot 连接成功时执行。

钩子函数参数:

- bot: 当前连接上的 Bot 对象

参数

- func(T_BotConnectionHook)

返回

- T_BotConnectionHook


### classmethodon_bot_disconnect(func)​

- 说明装饰一个函数使他在 bot 连接断开时执行。钩子函数参数:bot: 当前连接上的 Bot 对象
- 参数func(T_BotDisconnectionHook)
- 返回T_BotDisconnectionHook

说明

装饰一个函数使他在 bot 连接断开时执行。

钩子函数参数:

- bot: 当前连接上的 Bot 对象

参数

- func(T_BotDisconnectionHook)

返回

- T_BotDisconnectionHook


## varForwardDriver​

- 类型:ForwardMixin
- 说明支持客户端请求的驱动器。Deprecated，请使用ForwardMixin或其子类代替。

类型:ForwardMixin

说明

支持客户端请求的驱动器。

Deprecated，请使用ForwardMixin或其子类代替。


## abstract classForwardMixin(<auto>)​

- 说明:客户端混入基类。
- 参数auto

说明:客户端混入基类。

参数

auto


## abstract classHTTPClientMixin(<auto>)​

- 说明:HTTP 客户端混入基类。
- 参数auto

说明:HTTP 客户端混入基类。

参数

auto


### abstract async methodrequest(setup)​

- 说明:发送一个 HTTP 请求
- 参数setup(Request)
- 返回Response

说明:发送一个 HTTP 请求

参数

- setup(Request)

返回

- Response


### abstract methodstream_request(setup, *, chunk_size=1024)​

- 说明:发送一个 HTTP 流式请求
- 参数setup(Request)chunk_size(int)
- 返回AsyncGenerator[Response, None]

说明:发送一个 HTTP 流式请求

参数

- setup(Request)
- chunk_size(int)

setup(Request)

chunk_size(int)

返回

- AsyncGenerator[Response, None]


### abstract methodget_session(params=None, headers=None, cookies=None, version=HTTPVersion.H11, timeout=None, proxy=None)​

- 说明:获取一个 HTTP 会话
- 参数params(QueryTypes)headers(HeaderTypes)cookies(CookieTypes)version(str |HTTPVersion)timeout(TimeoutTypes)proxy(str | None)
- 返回HTTPClientSession

说明:获取一个 HTTP 会话

参数

- params(QueryTypes)
- headers(HeaderTypes)
- cookies(CookieTypes)
- version(str |HTTPVersion)
- timeout(TimeoutTypes)
- proxy(str | None)

params(QueryTypes)

headers(HeaderTypes)

cookies(CookieTypes)

version(str |HTTPVersion)

timeout(TimeoutTypes)

proxy(str | None)

返回

- HTTPClientSession


## classHTTPServerSetup(<auto>)​

- 说明:HTTP 服务器路由配置。
- 参数auto

说明:HTTP 服务器路由配置。

参数

auto


## enumHTTPVersion​

- 参数autoH10: '1.0'H11: '1.1'H2: '2'

参数

auto

- H10: '1.0'
- H11: '1.1'
- H2: '2'

H10: '1.0'

H11: '1.1'

H2: '2'


## abstract classMixin(<auto>)​

- 说明:可与其他驱动器共用的混入基类。
- 参数auto

说明:可与其他驱动器共用的混入基类。

参数

auto


### abstract propertytype​

- 类型:str
- 说明:混入驱动类型名称

类型:str

说明:混入驱动类型名称


## classRequest(method, url, *, params=None, headers=None, cookies=None, content=None, data=None, json=None, files=None, version=HTTPVersion.H11, timeout=None, proxy=None)​

- 参数method(str | bytes)url(URL | str | RawURL)params(QueryTypes)headers(HeaderTypes)cookies(CookieTypes)content(ContentTypes)data(DataTypes)json(Any)files(FilesTypes)version(str | HTTPVersion)timeout(TimeoutTypes)proxy(str | None)

- method(str | bytes)
- url(URL | str | RawURL)
- params(QueryTypes)
- headers(HeaderTypes)
- cookies(CookieTypes)
- content(ContentTypes)
- data(DataTypes)
- json(Any)
- files(FilesTypes)
- version(str | HTTPVersion)
- timeout(TimeoutTypes)
- proxy(str | None)

method(str | bytes)

url(URL | str | RawURL)

params(QueryTypes)

headers(HeaderTypes)

cookies(CookieTypes)

content(ContentTypes)

data(DataTypes)

json(Any)

files(FilesTypes)

version(str | HTTPVersion)

timeout(TimeoutTypes)

proxy(str | None)


## classResponse(status_code, *, headers=None, content=None, request=None)​

- 参数status_code(int)headers(HeaderTypes)content(ContentTypes)request(Request | None)

- status_code(int)
- headers(HeaderTypes)
- content(ContentTypes)
- request(Request | None)

status_code(int)

headers(HeaderTypes)

content(ContentTypes)

request(Request | None)


## varReverseDriver​

- 类型:ReverseMixin
- 说明支持服务端请求的驱动器。Deprecated，请使用ReverseMixin或其子类代替。

类型:ReverseMixin

说明

支持服务端请求的驱动器。

Deprecated，请使用ReverseMixin或其子类代替。


## abstract classReverseMixin(<auto>)​

- 说明:服务端混入基类。
- 参数auto

说明:服务端混入基类。

参数

auto


## classTimeout(<auto>)​

- 说明:Request 超时配置。
- 参数auto

说明:Request 超时配置。

参数

auto


## abstract classWebSocket(*, request)​

- 参数request(Request)

- request(Request)


### abstract propertyclosed​

- 类型:bool
- 说明:连接是否已经关闭

类型:bool

说明:连接是否已经关闭


### abstract async methodaccept()​

- 说明:接受 WebSocket 连接请求
- 参数empty
- 返回None

说明:接受 WebSocket 连接请求

参数

empty

返回

- None


### abstract async methodclose(code=1000, reason="")​

- 说明:关闭 WebSocket 连接请求
- 参数code(int)reason(str)
- 返回None

说明:关闭 WebSocket 连接请求

参数

- code(int)
- reason(str)

code(int)

reason(str)

返回

- None


### abstract async methodreceive()​

- 说明:接收一条 WebSocket text/bytes 信息
- 参数empty
- 返回str | bytes

说明:接收一条 WebSocket text/bytes 信息

参数

empty

返回

- str | bytes


### abstract async methodreceive_text()​

- 说明:接收一条 WebSocket text 信息
- 参数empty
- 返回str

说明:接收一条 WebSocket text 信息

参数

empty

返回

- str


### abstract async methodreceive_bytes()​

- 说明:接收一条 WebSocket binary 信息
- 参数empty
- 返回bytes

说明:接收一条 WebSocket binary 信息

参数

empty

返回

- bytes


### async methodsend(data)​

- 说明:发送一条 WebSocket text/bytes 信息
- 参数data(str | bytes)
- 返回None

说明:发送一条 WebSocket text/bytes 信息

参数

- data(str | bytes)

返回

- None


### abstract async methodsend_text(data)​

- 说明:发送一条 WebSocket text 信息
- 参数data(str)
- 返回None

说明:发送一条 WebSocket text 信息

参数

- data(str)

返回

- None


### abstract async methodsend_bytes(data)​

- 说明:发送一条 WebSocket binary 信息
- 参数data(bytes)
- 返回None

说明:发送一条 WebSocket binary 信息

参数

- data(bytes)

返回

- None


## abstract classWebSocketClientMixin(<auto>)​

- 说明:WebSocket 客户端混入基类。
- 参数auto

说明:WebSocket 客户端混入基类。

参数

auto


### abstract methodwebsocket(setup)​

- 说明:发起一个 WebSocket 连接
- 参数setup(Request)
- 返回AsyncGenerator[WebSocket, None]

说明:发起一个 WebSocket 连接

参数

- setup(Request)

返回

- AsyncGenerator[WebSocket, None]


## classWebSocketServerSetup(<auto>)​

- 说明:WebSocket 服务器路由配置。
- 参数auto

说明:WebSocket 服务器路由配置。

参数

auto


## defcombine_driver(driver, *mixins)​

- 说明:将一个驱动器和多个混入类合并。
- 重载1.(driver) -> type[D]参数driver(type[D])返回type[D]2.(driver, __m, /, *mixins) -> type[CombinedDriver]参数driver(type[D])__m(type[Mixin])*mixins(type[Mixin])返回type[CombinedDriver]

说明:将一个驱动器和多个混入类合并。

重载

1.(driver) -> type[D]

- 参数driver(type[D])
- 返回type[D]

参数

- driver(type[D])

返回

- type[D]

2.(driver, __m, /, *mixins) -> type[CombinedDriver]

- 参数driver(type[D])__m(type[Mixin])*mixins(type[Mixin])
- 返回type[CombinedDriver]

参数

- driver(type[D])
- __m(type[Mixin])
- *mixins(type[Mixin])

driver(type[D])

__m(type[Mixin])

*mixins(type[Mixin])

返回

- type[CombinedDriver]

# nonebot.plugin

- nonebot.plugin


# nonebot.plugin

本模块为 NoneBot 插件开发提供便携的定义函数。


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
- require=>require
- PluginMetadata=>PluginMetadata


## defget_plugin(plugin_id)​

- 说明获取已经导入的某个插件。如果为load_plugins文件夹导入的插件，则为文件(夹)名。如果为嵌套的子插件，标识符为父插件标识符:子插件文件(夹)名。
- 参数plugin_id(str): 插件标识符，即Plugin.id_。
- 返回Plugin| None

说明

获取已经导入的某个插件。

如果为load_plugins文件夹导入的插件，则为文件(夹)名。

如果为嵌套的子插件，标识符为父插件标识符:子插件文件(夹)名。

参数

- plugin_id(str): 插件标识符，即Plugin.id_。

返回

- Plugin| None


## defget_plugin_by_module_name(module_name)​

- 说明通过模块名获取已经导入的某个插件。如果提供的模块名为某个插件的子模块，同样会返回该插件。
- 参数module_name(str): 模块名，即Plugin.module_name。
- 返回Plugin| None

说明

通过模块名获取已经导入的某个插件。

如果提供的模块名为某个插件的子模块，同样会返回该插件。

参数

- module_name(str): 模块名，即Plugin.module_name。

返回

- Plugin| None


## defget_loaded_plugins()​

- 说明:获取当前已导入的所有插件。
- 参数empty
- 返回set[Plugin]

说明:获取当前已导入的所有插件。

参数

empty

返回

- set[Plugin]


## defget_available_plugin_names()​

- 说明:获取当前所有可用的插件标识符（包含尚未加载的插件）。
- 参数empty
- 返回set[str]

说明:获取当前所有可用的插件标识符（包含尚未加载的插件）。

参数

empty

返回

- set[str]


## defget_plugin_config(config)​

- 说明:从全局配置获取当前插件需要的配置项。
- 参数config(type[C])
- 返回C

说明:从全局配置获取当前插件需要的配置项。

参数

- config(type[C])

返回

- C

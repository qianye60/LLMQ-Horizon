# nonebot.compat

- nonebot.compat


# nonebot.compat

本模块为 Pydantic 版本兼容层模块

为兼容 Pydantic V1 与 V2 版本，定义了一系列兼容函数与类供使用。


## varRequired​

- 类型:untyped
- 说明:Alias of Ellipsis for compatibility with pydantic v1

类型:untyped

说明:Alias of Ellipsis for compatibility with pydantic v1


## library-attrPydanticUndefined​

- 说明:Pydantic Undefined object


## library-attrPydanticUndefinedType​

- 说明:Pydantic Undefined type


## varDEFAULT_CONFIG​

- 类型:untyped
- 说明:Default config for validations

类型:untyped

说明:Default config for validations


## defLegacyUnionField(<auto>)​

- 说明:Mark field to use legacy left to right union mode
- 参数auto
- 返回untyped

说明:Mark field to use legacy left to right union mode

参数

auto

返回

- untyped


## classFieldInfo(default=PydanticUndefined, **kwargs)​

- 说明:FieldInfo class with extra property for compatibility with pydantic v1
- 参数default(Any)**kwargs(Any)

说明:FieldInfo class with extra property for compatibility with pydantic v1

参数

- default(Any)
- **kwargs(Any)

default(Any)

**kwargs(Any)


### propertyextra​

- 类型:dict[str, Any]
- 说明Extra data that is not part of the standard pydantic fields.For compatibility with pydantic v1.

类型:dict[str, Any]

说明

Extra data that is not part of the standard pydantic fields.

For compatibility with pydantic v1.


## classModelField(<auto>)​

- 说明:ModelField class for compatibility with pydantic v1
- 参数auto

说明:ModelField class for compatibility with pydantic v1

参数

auto


### instance-varname​

- 类型:str
- 说明:The name of the field.

类型:str

说明:The name of the field.


### instance-varannotation​

- 类型:Any
- 说明:The annotation of the field.

类型:Any

说明:The annotation of the field.


### instance-varfield_info​

- 类型:FieldInfo
- 说明:The FieldInfo of the field.

类型:FieldInfo

说明:The FieldInfo of the field.


### classmethodconstruct(name, annotation, field_info=None)​

- 说明:Construct a ModelField from given infos.
- 参数name(str)annotation(Any)field_info(FieldInfo | None)
- 返回Self

说明:Construct a ModelField from given infos.

参数

- name(str)
- annotation(Any)
- field_info(FieldInfo | None)

name(str)

annotation(Any)

field_info(FieldInfo | None)

返回

- Self


### methodget_default()​

- 说明:Get the default value of the field.
- 参数empty
- 返回Any

说明:Get the default value of the field.

参数

empty

返回

- Any


### methodvalidate_value(value)​

- 说明:Validate the value pass to the field.
- 参数value(Any)
- 返回Any

说明:Validate the value pass to the field.

参数

- value(Any)

返回

- Any


## defmodel_fields(model)​

- 说明:Get field list of a model.
- 参数model(type[BaseModel])
- 返回list[ModelField]

说明:Get field list of a model.

参数

- model(type[BaseModel])

返回

- list[ModelField]


## defmodel_config(model)​

- 说明:Get config of a model.
- 参数model(type[BaseModel])
- 返回Any

说明:Get config of a model.

参数

- model(type[BaseModel])

返回

- Any


## defmodel_dump(model, include=None, exclude=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False)​

- 参数model(BaseModel)include(set[str] | None)exclude(set[str] | None)by_alias(bool)exclude_unset(bool)exclude_defaults(bool)exclude_none(bool)
- 返回dict[str, Any]

参数

- model(BaseModel)
- include(set[str] | None)
- exclude(set[str] | None)
- by_alias(bool)
- exclude_unset(bool)
- exclude_defaults(bool)
- exclude_none(bool)

model(BaseModel)

include(set[str] | None)

exclude(set[str] | None)

by_alias(bool)

exclude_unset(bool)

exclude_defaults(bool)

exclude_none(bool)

返回

- dict[str, Any]


## deftype_validate_python(type_, data)​

- 说明:Validate data with given type.
- 参数type_(type[T])data(Any)
- 返回T

说明:Validate data with given type.

参数

- type_(type[T])
- data(Any)

type_(type[T])

data(Any)

返回

- T


## deftype_validate_json(type_, data)​

- 说明:Validate JSON with given type.
- 参数type_(type[T])data(str | bytes)
- 返回T

说明:Validate JSON with given type.

参数

- type_(type[T])
- data(str | bytes)

type_(type[T])

data(str | bytes)

返回

- T


## defcustom_validation(class_)​

- 说明:Use pydantic v1 like validator generator in pydantic v2
- 参数class_(type[CVC])
- 返回type[CVC]

说明:Use pydantic v1 like validator generator in pydantic v2

参数

- class_(type[CVC])

返回

- type[CVC]

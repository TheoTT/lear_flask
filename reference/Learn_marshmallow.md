# marshmallow

参考：

	官方文档：https://marshmallow.readthedocs.io/en/latest/custom_fields.html#method-fields
	
	简书：https://www.jianshu.com/p/594865f0681b



In short, marshmallow schemas can be used to:

- **Validate** input data.
- **Deserialize** input data to app-level objects.
- **Serialize** app-level objects to primitive Python  types. The serialized objects can then be rendered to standard formats  such as JSON for use in an HTTP API.

实现orm对象与python原生数据类型的相互转换。

- `object -> dict`
-  `objects -> list`
-  `string -> dict`
-  `string -> list`

前提条件：存在一个用于序列化和反序列化的类。

	序列化：类（objecs）转化为json数据（可存储或可传输）
	
	反序列化：json数据转化为类。



### 安装marshmallow

```
pip install -U marshmallow --pre


```



### Schema

Schema ： object 与 json数据相互转换时的中间载体（除了转换以外，Schema还可以用来做数据校验每个需要转换的类，都需要一个对应的Schema）

Schema中一般都是Field obj



### Serializing（序列化）

dump()` 实现`obj -> dict

dumps()`实现 `obj -> string

注：

Flask提供的jsonify方法能直接序列化dict，一般还会对字典进行进一步处理，一般不会直接把obj直接转化为string（dumps方法不经常使用）

可以使用`only`，exclude参数来指定需要输出的字段

















### Deserializing（反序列化）

反序列化将字典等类型转换成应用层的数据结构，即orm对象

load()` 实现`dict -> obj  方法需要自己实现，再用post_load装饰器装饰

loads()`实现 `string -> obj





### Objects <-> List（多个obj的序列化与反序列化）

对于objects的处理，只需在schema中增加一个参数：`many=True`



### Schema.validate(仅使用Schema的验证功能，而不生成对象)

使用`Schema.validate()`

```

```





### Field

常用Field类型：

```
	username": fields.Str(required=True),
    # Validation
    "password": fields.Str(validate=lambda p: len(p) >= 6),
    # OR use marshmallow's built-in validators
    "password": fields.Str(validate=validate.Length(min=6)),
    # Default value when argument is missing
    "display_per_page": fields.Int(missing=10),
    # Repeated parameter, e.g. "/?nickname=Fred&nickname=Freddie"
    "nickname": fields.List(fields.Str()),
    # Delimited list, e.g. "/?languages=python,javascript"
    "languages": fields.DelimitedList(fields.Str()),
    # When you know where an argument should be parsed from
    "active": fields.Bool(location="query"),
    # When value is keyed on a variable-unsafe name
    # or you want to rename a key
    "content_type": fields.Str(load_from="Content-Type", location="headers")
```



`Nested field`：外键对象

当model obj 中存在外键时，`Nested field`表示外键对象，这样序列化时，会带上外键到信息：

```


#如果有两个对象需要相互包含，可以指定Nested对象的类名字符串，而不需要类。这样可以包含一个还未定义的对象



#如果外键对象是自引用，则Nested里第一个参数为'self'


```





#### Validation参数

`Schema.load()` 和 `loads()`方法会在返回值中加入验证错误的`dictionary`。

内建验证器：

```python3
#url验证


#email验证



#当验证一个集合时，返回的错误`dictionary`会以错误序号对应错误信息的key：value形式保存


```

通过Field到validate参数定制验证器，`validate`的值可以是函数，匿名函数`lambda`，或者是定义了`__call__`的对象

```
#函数


#lambda函数


#定义了__call__的obj





```

传入的函数中定义了`ValidationError`，当它触发时，错误信息会得到保存：

```

```

使用`validates` 装饰器可以注册一个验证方法：

```

```





注：

 如果需要执行多个验证，应该传入可调用的验证器的集合（list, tuple, generator）

strict Mode参数：

Required 

在`field`中传入`required=True`.当`Schema.load()`的输入缺少某个字段时错误会记录下来。

通过传入error_messages 参数定制required到错误信息。





 `Schema.dump()` 也会返回错误信息`dictionary`，也会包含序列化时的所有`ValidationE``rrors`。但是`required`, `allow_none`, `validate`, `@validates`, 和 `@validates_schema` 只用于反序列化，即`Schema.load()`。





#### strict 参数

如果将`strict=True`传入`Schema`构造器或者`class`的`Meta`参数里，则仅会在传入无效数据	是报错。可以使用`ValidationError.messages`变量来获取验证错误的`dictionary`

一般都会将strict 的值置为True

```

```



#### `many`参数

如果field 是多个对象的集合，定义时可以使用`many`参数

```

```



#### only参数







Specifying Which Fields to Nest

如果你想指定外键对象序列化后只保留它的几个字段

```

```

如果需要选择外键对象的字段层次较多，可以使用"."操作符来指定：

```

```



如果`Nested`是多个对象的列表，传入only可以获得这列表的指定字段：

```

```



#### `partial`参数（Partial Loading）

RESTful架构中，更新数据有如下两种方法：

- PUT：需要把完整的数据全部传给服务器。

- PATCH：只需把需要改动的部分数据传给服务器。

在使用PATCH时，若在Filed设置了required参数，可能存在无法通过`Marshmallow` 数据校验的风险，可以使用Partial Loading解决该问题。

实现`Partial Loadig`只要在`schema`构造器中增加一个`partial`参数：

```

```





#### attribute参数（Specifying Attribute Names）

序列化时指定字典元素的名称，不使用默认名称。通过传入attribute参数实现：

```

```



#### load_from参数（Specifying Deserialization Keys）

反序列化时，若目标元素的字段名（key 或者 strName）与Schema中field字段名不匹配，可以使用load_from参数指定需要增加load的字段名（仍然优先load原字段名）



```

```



### `dump_to`参数（Specifying Serialization Keys）

需要编列一个`field`成一个不同的key名时，可以使用`dump_to`，逻辑和`load_from`类似：

```

```



### load_only and dump_only参数

指定某些字段只能够`dump()`或`load()`

```

```









## flask -marshallow

Flask和marshmallow的中间层。








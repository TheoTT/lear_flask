# [webargs](https://webargs.readthedocs.io/en/latest/index.html)



webargs用于解析http请求的参数，同时还能对传递过来的参数进行验证（validate）。



```
from webargs import fields, validate

user_args = {
    # Required arguments
    "username": fields.Str(required=True),
    
    # Validation
    "password": fields.Str(validate=lambda p: len(p) >= 6),
    # OR use marshmallow's built-in validators
    "password": fields.Str(validate=validate.Length(min=6)),
    
    # Default value when argument is missing
    "display_per_page": fields.Int(missing=10),
    
    # Repeated parameter, e.g. "/?nickname=Fred&nickname=Freddie"
    #（从参数字典中，读取nickname的值转换为字符串再放入nickname列表中，即nickname['Fred','Freddie']）
    "nickname": fields.List(fields.Str()),
    
    # Delimited list, e.g. "/?languages=python,javascript"
    "languages": fields.DelimitedList(fields.Str()),
    
    # When you know where an argument should be parsed from
    "active": fields.Bool(location="query"),
    
    # When value is keyed on a variable-unsafe name
    # or you want to rename a key
    "content_type": fields.Str(load_from="Content-Type", location="headers"),
}
```





To parse request arguments, use the [`parse`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.parse) method of a [`Parser`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser) object.（使用Parser对象的parse方法对request对象进行解析（一般不用了，直接用下面的装饰器）

```
from flask import request
from webargs.flaskparser import parser


@app.route("/register", methods=["POST"])
def register():
    args = parser.parse(user_args, request)
    return register_user(
        args["username"],
        args["password"],
        fullname=args["fullname"],
        per_page=args["display_per_page"],
    )
```

## Decorator API（装饰器：use_args及use_kwargs）

As an alternative to `Parser.parse`, you can decorate your view with [`use_args`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_args) or [`use_kwargs`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_kwargs). The parsed arguments dictionary will be injected as a parameter of your view function or as keyword arguments, respectively.（前面parser方法的替代品）

@use_args() 装饰view函数时，会将request请求中的参数解析后注入view的参数字典中；

@use_kargs()装饰view函数时，会将request请求中的参数解析后注入view的关键字参数中。

```
from webargs.flaskparser import use_args, use_kwargs


@app.route("/register", methods=["POST"])
@use_args(user_args)  # Injects args dictionary
def register(args):
    return register_user(
        args["username"],
        args["password"],
        fullname=args["fullname"],
        per_page=args["display_per_page"],
    )


@app.route("/settings", methods=["POST"])
@use_kwargs(user_args)  # Injects keyword arguments
def user_settings(username, password, fullname, display_per_page, nickname):
    return render_template("settings.html", username=username, nickname=nickname)
    
    
#When using use_kwargs, any missing values for non-required fields will take the special value missing.（使用@use_kargs（）装饰器时，如果给定的参数值是non-required fields时，会默认将该参数的数值置为missing）

from webargs import fields, missing


@use_kwargs({"name": fields.Str(), "nickname": fields.Str(required=False)})
def myview(name, nickname):
    if nickname is missing:
        # ...
        pass

```

## Request “Locations”（指定解析参数的位置）

By default, webargs will search for arguments from the URL query string (e.g. `"/?name=foo"`), form data, and JSON data (in that order). You can explicitly specify which locations to search

可以指定的位置如下：

- `'querystring'` (same as `'query'`)
- `'json'`
- `'form'`
- `'headers'`
- `'cookies'`
- `'files'`

```
@app.route("/register")
@use_args(user_args, locations=("json", "form"))
def register(args):
    return "registration page"
```



验证（Validation）

所有的Field对象都可以通过指定validation参数进行验证

```
from webargs import fields

args = {"age": fields.Int(validate=lambda val: val > 0)}

#验证错误处理
#The validator may return either a boolean or raise a ValidationError.（验证器返回布尔值或者引发一个错误）

from webargs import fields, ValidationError


def must_exist_in_db(val):
    if not User.query.get(val):
        # Optionally pass a status_code
        raise ValidationError("User does not exist")


argmap = {"id": fields.Int(validate=must_exist_in_db)}

#验证器返回None，通过验证，验证失败则返回布尔值，或者引发一个错误，或者在引发错误时，返回一个HTTP status code。

def must_exist_in_db(val):
    if not User.query.get(val):
        # Optionally pass a status_code
        raise ValidationError('User does not exist', status_code=404)

argmap = {
    'id': fields.Int(validate=must_exist_in_db)
}


#同时验证整个参数字典
The full arguments dictionary can also be validated by passing validate to Parser.parse, Parser.use_args, Parser.use_kwargs.

from webargs import fields
from webargs.flaskparser import parser

argmap = {"age": fields.Int(), "years_employed": fields.Int()}

# ...
result = parser.parse(
    argmap, validate=lambda args: args["years_employed"] < args["age"]
)



```



## Error Handling（错误处理）

Each parser has a default error handling method. To override the error handling callback, write a function that receives an error, the request, and the [`marshmallow.Schema`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.Schema) instance. Then decorate that function with [`Parser.error_handler`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.error_handler).（覆盖默认的err handling method，重写一个函数，函数的参数为err，request，schema，再使用@Parser.error_handler()装饰该函数）

```
from webargs import flaskparser

parser = flaskparser.FlaskParser()


class CustomError(Exception):
    pass


@parser.error_handler
def handle_error(error, req, schema):
    raise CustomError(error.messages)
```



## Nesting Fields（嵌套Fields）[¶](https://webargs.readthedocs.io/en/latest/quickstart.html#nesting-fields)

Field对象可以互相嵌套，通过该特性可以很方便验证嵌套的数据。

（注：默认情况下，webargs只从request的json参数进行nested Field的解析，但是可以自己实现解析器，将嵌套字段解析功能添加到其他地方）

```
from webargs import fields

args = {
    "name": fields.Nested(
        {"first": fields.Str(required=True), "last": fields.Str(required=True)}
    )
}
```





## Custom Location Handlers（自定义解析函数，解析任意位置的参数）

To add your own custom location handler, write a function that receives a request, an argument name, and a [`Field`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.fields.Field), then decorate that function with [`Parser.location_handler`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.location_handler).

```
from webargs import fields
from webargs.flaskparser import parser


@parser.location_handler("data")
def parse_data(request, name, field):
    return request.data.get(name)


# Now 'data' can be specified as a location
@parser.use_args({"per_page": fields.Int()}, locations=("data",))
def posts(args):
    return "displaying {} posts".format(args["per_page"])
```

## Marshmallow Integration

When you need more flexibility in defining input schemas, you can pass a marshmallow [`Schema`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.Schema) instead of a dictionary to [`Parser.parse`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.parse), [`Parser.use_args`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_args), and [`Parser.use_kwargs`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_kwargs).

（通过定义Schema，可以让 [`Parser.parse`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.parse), [`Parser.use_args`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_args), and [`Parser.use_kwargs`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_kwargs).接收自定义类型的输入）

注：

​	1.You should always set `strict=True` (either as a `class Meta` option or in the Schema’s constructor) when passing a schema to webargs. This will ensure that the parser’s error handler is invoked when expected.（需要指定strict=True，或者在定义所需的schema时在class Meta中定义stric = True，这样能够确保在发生解析错误时，调用所期望的错误处理程序）

​	2. Any [`Schema`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.Schema) passed to [`use_kwargs`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_kwargs) MUST deserialize to a dictionary of data. Keep this in mind when writing [`post_load`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.decorators.post_load)methods.（所有传递给webargs的schema，都需要进行反序列化）

```
from marshmallow import Schema, fields
from webargs.flaskparser import use_args


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # read-only (won't be parsed by webargs)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)  # write-only
    first_name = fields.Str(missing="")
    last_name = fields.Str(missing="")
    date_registered = fields.DateTime(dump_only=True)

    class Meta:
        strict = True


@use_args(UserSchema())
def profile_view(args):
    username = args["userame"]
    # ...


@use_kwargs(UserSchema())
def profile_update(username, password, first_name, last_name):
    update_profile(username, password, first_name, last_name)
    # ...


# You can add additional parameters
@use_kwargs({"posts_per_page": fields.Int(missing=10, location="query")})
@use_args(UserSchema())
def profile_posts(args, posts_per_page):
    username = args["username"]
    # ...
```

## Schema Factories

If you need to parametrize a schema based on a given request, you can use a “Schema factory”: a callable that receives the current `request` and returns a [`marshmallow.Schema`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.Schema) instance.(接收request中的参数，返回一个schema)

Consider the following use cases:

- Filtering via a query parameter by passing `only` to the Schema.
- Handle partial updates for PATCH requests using marshmallow’s [partial loading](https://marshmallow.readthedocs.io/en/latest/quickstart.html#partial-loading) API.



```
from marshmallow import Schema, fields
from webargs.flaskparser import use_args


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)
    first_name = fields.Str(missing="")
    last_name = fields.Str(missing="")
    date_registered = fields.DateTime(dump_only=True)

    class Meta:
        strict = True


def make_user_schema(request):
    # Filter based on 'fields' query parameter
    only = request.args.get("fields", None)
    # Respect partial updates for PATCH requests
    partial = request.method == "PATCH"
    # Add current request to the schema's context
    return UserSchema(only=only, partial=partial, context={"request": request})


# Pass the factory to .parse, .use_args, or .use_kwargs
@use_args(make_user_schema)
def profile_view(args):
    username = args["username"]
    # ...
```





### Reducing Boilerplate（没太看懂）

```
e can reduce boilerplate and improve [re]usability with a simple helper function:

from webargs.flaskparser import use_args


def use_args_with(schema_cls, schema_kwargs=None, **kwargs):
    schema_kwargs = schema_kwargs or {}

    def factory(request):
        # Filter based on 'fields' query parameter
        only = request.args.get("fields", None)
        # Respect partial updates for PATCH requests
        partial = request.method == "PATCH"
        # Add current request to the schema's context
        # and ensure we're always using strict mode
        return schema_cls(
            only=only,
            partial=partial,
            strict=True,
            context={"request": request},
            **schema_kwargs
        )

    return use_args(factory, **kwargs)
Now we can attach input schemas to our view functions like so:

@use_args_with(UserSchema)
def profile_view(args):
    # ...
    get_profile(**args)
```



## Custom Fields（自定义Fields）[¶](https://webargs.readthedocs.io/en/latest/advanced.html#custom-fields)

See the “Custom Fields” section of the marshmallow docs for a detailed guide on defining custom fields which you can pass to webargs parsers: [https://marshmallow.readthedocs.io/en/latest/custom_fields.html](https://marshmallow.readthedocs.io/en/latest/custom_fields.html).

### Using `Method` and `Function` Fields with webargs

Using the [`Method`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.fields.Method) and [`Function`](https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.fields.Function) fields requires that you pass the `deserialize` parameter.



```
@use_args({"cube": fields.Function(deserialize=lambda x: int(x) ** 3)})
def math_view(args):
    cube = args["cube"]
    # ...
```

## Custom Parsers

To add your own parser, extend [`Parser`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser) and implement the `parse_*` method(s) you need to override. For example, here is a custom Flask parser that handles nested query string arguments.

```
import re

from webargs import core
from webargs.flaskparser import FlaskParser


class NestedQueryFlaskParser(FlaskParser):
    """Parses nested query args

    This parser handles nested query args. It expects nested levels
    delimited by a period and then deserializes the query args into a
    nested dict.

    For example, the URL query params `?name.first=John&name.last=Boone`
    will yield the following dict:

        {
            'name': {
                'first': 'John',
                'last': 'Boone',
            }
        }
        
    """

    def parse_querystring(self, req, name, field):
        return core.get_value(_structure_dict(req.args), name, field)


def _structure_dict(dict_):
    def structure_dict_pair(r, key, value):
        m = re.match(r"(\w+)\.(.*)", key)
        if m:
            if r.get(m.group(1)) is None:
                r[m.group(1)] = {}
            structure_dict_pair(r[m.group(1)], m.group(2), value)
        else:
            r[key] = value

    r = {}
    for k, v in dict_.items():
        structure_dict_pair(r, k, v)
    return r
```

## Returning HTTP 400 Responses

If you’d prefer validation errors to return status code `400` instead of `422`, you can override `DEFAULT_VALIDATION_STATUS` on a [`Parser`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser).

```
from webargs.falconparser import FalconParser


class Parser(FalconParser):
    DEFAULT_VALIDATION_STATUS = 400


parser = Parser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs

```

## Bulk-type Arguments

In order to parse a JSON array of objects, pass `many=True` to your input `Schema` .

For example, you might implement JSON PATCH according to [RFC 6902](https://tools.ietf.org/html/rfc6902) like so:

```
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import Schema, validate


class PatchSchema(Schema):
    op = fields.Str(
        required=True,
        validate=validate.OneOf(["add", "remove", "replace", "move", "copy"]),
    )
    path = fields.Str(required=True)
    value = fields.Str(required=True)

    class Meta:
        strict = True


@app.route("/profile/", methods=["patch"])
@use_args(PatchSchema(many=True), locations=("json",))
def patch_blog(args):
    """Implements JSON Patch for the user profile

    Example JSON body:

    [
        {"op": "replace", "path": "/email", "value": "mynewemail@test.org"}
    ]
    """
    # ...

```

## Mixing Locations

Arguments for different locations can be specified by passing `location` to each field individually:

```
@app.route("/stacked", methods=["POST"])
@use_args(
    {
        "page": fields.Int(location="query"),
        "q": fields.Str(location="query"),
        "name": fields.Str(location="json"),
    }
)
def viewfunc(args):
    page = args["page"]
    # ...

```

Alternatively, you can pass multiple locations to [`use_args`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_args):

```
@app.route("/stacked", methods=["POST"])
@use_args(
    {"page": fields.Int(), "q": fields.Str(), "name": fields.Str()},
    locations=("query", "json"),
)
def viewfunc(args):
    page = args["page"]
    # ...

```

However, this allows `page` and `q` to be passed in the request body and `name` to be passed as a query parameter.

To restrict the arguments to single locations without having to pass `location` to every field, you can call the [`use_args`](https://webargs.readthedocs.io/en/latest/api.html#webargs.core.Parser.use_args) multiple times:

```
query_args = {"page": fields.Int(), "q": fields.Int()}
json_args = {"name": fields.Str()}


@app.route("/stacked", methods=["POST"])
@use_args(query_args, locations=("query",))
@use_args(json_args, locations=("json",))
def viewfunc(query_parsed, json_parsed):
    page = query_parsed["page"]
    name = json_parsed["name"]
    # ...

```

To reduce boilerplate, you could create shortcuts, like so:

```
import functools

query = functools.partial(use_args, locations=("query",))
body = functools.partial(use_args, locations=("json",))


@query(query_args)
@body(json_args)
def viewfunc(query_parsed, json_parsed):
    page = query_parsed["page"]
    name = json_parsed["name"]
    # ...
```


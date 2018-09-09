

# Flask-SQLAlchemy

参考：

​	https://blog.csdn.net/zyshappy/article/details/74092153

	http://flask-sqlalchemy.pocoo.org/2.1/api/

	http://www.pythondoc.com/flask-sqlalchemy/quickstart.html

​	https://blog.csdn.net/dszgf5717/article/details/53184025





## Declaring Models

- 所有模型的基类都称为db.Model。 它存储在您必须创建的SQLAlchemy实例上。
- SQLAlchemy中所需的某些部分在Flask-SQLAlchemy中是可选的。 例如，除非被覆盖，否则将自动为您设置表名。 它源自转换为小写的类名，并将“CamelCase”转换为“camel_case”。 要覆盖表名，请设置__tablename__类属性。



数据类型：

| [`Integer`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Integer) | an integer                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`String(size)`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.String) | a string with a maximum length (optional in some databases, e.g. PostgreSQL) |
| [`Text`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Text) | some longer unicode text                                     |
| [`DateTime`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.DateTime) | date and time expressed as Python [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime) object. |
| [`Float`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Float) | stores floating point values                                 |
| [`Boolean`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Boolean) | stores a boolean value                                       |
| [`PickleType`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.PickleType) | stores a pickled Python object                               |
| [`LargeBinary`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.LargeBinary) | stores large arbitrary binary data                           |

（pickled 与JSON不同的是pickle不是用于多种语言间的数据传输，它仅作为python对象的持久化或者python程序间进行互相传输对象的方法，因此它支持了python所有的数据类型。可以参考：https://www.cnblogs.com/tkqasn/p/6005025.html）

```
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
```





### One-to-Many Relationships

```
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)
        
        
       
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', lazy='select',
        backref=db.backref('person', lazy='joined'))

```





### Many-to-Many Relationships

```
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```





## 操作数据库



### Inserting Records

1. Create the Python object
2. Add it to the session
3. Commit the session



```
>>> from yourapp import User
>>> me = User('admin', 'admin@example.com')
>>> db.session.add(me)
>>> db.session.commit()
```



### Deleting Records

```
>>> db.session.delete(me)
>>> db.session.commit()
```



### Querying Records



`filter()` to filter the records before
you fire the select with `all()` or
`first()`.  If you want to go by
primary key you can also use `get()`.



### Queries in Views

Instead of
[`get()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get) one can use
`get_or_404()` and instead of



[`first()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.first) `first_or_404()`.
This will raise 404 errors instead of returning None:



## 配置

​	Flask-SQLAlchemy存在以下配置值，运行时从Flask app的主配置中加载。其中一些配置值在创建引擎之后无法修改。



| `SQLALCHEMY_DATABASE_URI`        | The database URI that should be used for the connection.  Examples:  `sqlite:////tmp/test.db` `mysql://username:password@server/db` |
| -------------------------------- | ------------------------------------------------------------ |
| `SQLALCHEMY_BINDS`               | A dictionary that maps bind keys to SQLAlchemy connection URIs.  For more information about binds see [Multiple Databases with Binds](http://flask-sqlalchemy.pocoo.org/2.3/binds/#binds).（将绑定键映射到SQLAlchemy连接URI的字典。） |
| `SQLALCHEMY_ECHO`                | If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.（如果设置为True SQLAlchemy将记录发送到stderr的所有语句，这对调试很有用。） |
| `SQLALCHEMY_RECORD_QUERIES`      | Can be used to explicitly disable or enable query recording.  Query recording automatically happens in debug or testing mode.  See `get_debug_queries()` for more information.（可用于显式禁用或启用查询记录。 查询记录在调试或测试模式下自动进行） |
| `SQLALCHEMY_NATIVE_UNICODE`      | Can be used to explicitly disable native unicode support.  This is required for some database adapters (like PostgreSQL on some Ubuntu versions) when used with improper database defaults that specify encoding-less databases.（可用于显式禁用本机unicode支持。 对于某些数据库适配器（如某些Ubuntu版本上的PostgreSQL），当与指定无编码数据库的不正确的数据库默认值一起使用时，这是必需的。） |
| `SQLALCHEMY_POOL_SIZE`           | The size of the database pool.  Defaults to the engine’s default (usually 5)（数据库池的大小。 默认为引擎的默认值（通常为5）） |
| `SQLALCHEMY_POOL_TIMEOUT`        | Specifies the connection timeout in seconds for the pool.    |
| `SQLALCHEMY_POOL_RECYCLE`        | 自动收回连接到秒数，这是MySQL所必需的，默认情况下在8小时空闲后删除连接。 请注意，如果使用MySQL，Flask-SQLAlchemy会自动将其设置为2小时。 某些后端可能使用不同的默认超时值。 [Timeouts](http://flask-sqlalchemy.pocoo.org/2.3/config/#timeouts). |
| `SQLALCHEMY_MAX_OVERFLOW`        | Controls the number of connections that can be created after the pool reached its maximum size.  When those additional connections are returned to the pool, they are disconnected and discarded.控制池达到其最大大小后可以创建的连接数。 当这些附加连接返回到池时，它们将被断开连接并被丢弃。 |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | If set to `True`, Flask-SQLAlchemy will track modifications of objects and emit signals.  The default is `None`, which enables tracking but issues a warning that it will be disabled by default in the future.  This requires extra memory and should be disabled if not needed.如果设置为True，Flask-SQLAlchemy将跟踪对象的修改并发出信号。 默认值为None，它启用跟踪，但会发出警告，默认情况下将来会禁用它。 这需要额外的内存，如果不需要应该禁用。 |

### Connection URI Format（连接数据库url的格式）

```
dialect+driver://username:password@host:port/database

Postgres:

postgresql://scott:tiger@localhost/mydatabase

MySQL:

mysql://scott:tiger@localhost/mydatabase

Oracle:

oracle://scott:tiger@127.0.0.1:1521/sidname

SQLite (note that platform path conventions apply):

#Unix/Mac (note the four leading slashes)
sqlite:////absolute/path/to/foo.db
#Windows (note 3 leading forward slashes and backslash escapes)
sqlite:///C:\\absolute\\path\\to\\foo.db
#Windows (alternative using raw string)
r'sqlite:///C:\absolute\path\to\foo.db'




```

### Timeouts

​	某些数据库后端可能会施加不同的非活动连接超时，这会干扰Flask-SQLAlchemy的连接池，例如默认情况下，MariaDB配置为600秒超时。 这通常难以调试，生产环境只有例外（2013: Lost connection to MySQL server during query）这条异常提示。

​	如果使用具有较低连接超时的后端（或预先配置的数据库即服务），建议SQLALCHEMY_POOL_RECYCLE设置为小于后端超时的值。





## Multiple Databases with Binds（连接多个数据库）









## Signalling Support

首要条件：`SQLALCHEMY_TRACK_MODIFICATIONS` is enabled in the config

-  `models_committed`

  This signal is sent when changed models were committed to the database. The sender is the application that emitted the changes. The receiver is passed the `changes` parameter with a list of tuples in the form `(model instance, operation)`. The operation is one of `'insert'`, `'update'`, and `'delete'`. 

-  `before_models_committed`

  This signal works exactly like [`models_committed`](http://flask-sqlalchemy.pocoo.org/2.3/signals/#models_committed) but is emitted before the commit takes place. 







# Customizing









## API




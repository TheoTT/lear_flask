

# Flask-SQLAlchemy

参考：

	https://www.cnblogs.com/mrchige/p/6389588.html
	
	http://flask-sqlalchemy.pocoo.org/2.1/api/
	http://flask-sqlalchemy.pocoo.org/2.3/models/#declaring-models
	http://www.pythondoc.com/flask-sqlalchemy/quickstart.html
	
	https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh/blob/master/docs/%e7%ac%ac%e5%9b%9b%e7%ab%a0%ef%bc%9a%e6%95%b0%e6%8d%ae%e5%ba%93.md
	
	https://www.cnblogs.com/franknihao/p/7268752.html


	





```
    def teardown_method(self, method):                                          
	       for model in [User, Company, Customer, Product, ProfitCenter, ProductGroup, Material, Receivable]:
              db.session.query(model).delete()                                       
              db.session.commit()
```



## Declaring Models

- 所有模型的基类都称为db.Model。 它存储在您必须创建的SQLAlchemy实例上。
- SQLAlchemy中所需的某些部分在Flask-SQLAlchemy中是可选的。 例如，除非被覆盖，否则将自动为您设置表名。 它源自转换为小写的类名，并将“CamelCase”转换为“camel_case”。 要覆盖表名，请设置__tablename__类属性。



### 数据类型：

| 常用列类型                                                   | python对象      | 说明                                                         |
| ------------------------------------------------------------ | --------------- | ------------------------------------------------------------ |
| [`Integer`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Integer) | int             | an integer（一般为32位）                                     |
| SmallInteger                                                 | int             | 取值范围小的整数，一般为16位                                 |
| [`String(size)`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.String) | str             | a string with a maximum length (optional in some databases, e.g. PostgreSQL) |
| [`Text`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Text) | str             | some longer unicode text                                     |
| unicode                                                      | unicode         | 变长unicode字符串                                            |
| unicodeText                                                  | unicode         |                                                              |
| [`DateTime`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.DateTime) |                 | date and time expressed as Python [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime) object. |
| Date                                                         | datetime.date   | 日期                                                         |
| Time                                                         | datetime.time   | 时间                                                         |
| [`Float`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Float) | float           | stores floating point values                                 |
| Numeric                                                      | decimal.Decimal | 定点数                                                       |
| [`Boolean`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Boolean) | bool            | stores a boolean value                                       |
| [`PickleType`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.PickleType) |                 | stores a pickled Python object(python对象)                   |
| [`LargeBinary`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.LargeBinary) | str             | stores large arbitrary binary data（二进制文件）             |
|                                                              |                 |                                                              |

	Flask-SQLAlchemy要求每一个model都定义主键（id）
	
	（pickled 与JSON不同的是pickle不是用于多种语言间的数据传输，它仅作为python对象的持久化或者python程序间进行互相传输对象的方法，因此它支持了python所有的数据类型。可以参考：https://www.cnblogs.com/tkqasn/p/6005025.html）
	
	(定点数（fixed-point）：字面意思看，小数点位置是固定的，即约定机器中所有数据的小数点位置是不变的。在计算机中通常有两种简单的约定：将小数点的位置固定放在数据的最高位之前，或者固定在最低位数据之后，一般称前者为定点小数，后者为定点整数)

### 数据约束：

| primary_key | 主键                        |
| ----------- | --------------------------- |
| unique      | 不允许重复                  |
| index       | 是否创建索引                |
| nullable    | 是否允许为空（False不允许） |
| default     | 定义默认值                  |



外键foreign key



ON DELETE 和 ON UPDATE,表示当发生delete和update时,会发生什么行为

    NO ACTION:默认的,表示没有什么行为.
    RESTRICT:当有一个child关联到parent时,禁止delete或update parent
    SET NULL:当parent被delete或update时,child的的关联字段被置为null(如果字段有not null,就出错)
    SET DEFAULT:类似于SET NULL (是不是设置默认值?没有试过)
    CASCADE:将实施在parent上的删除或更新操作,传播给你吧与之关联的child上.
    对于 ON DELETE CASCADE, 同被删除的父表中的行 相关联的子表中的每1行,也会被删除.
    对于ON UPDATE CASCADE, 存储在子表中的每1行,对应的字段的值会被自动修改成同新的父键匹配

3.使用注意

不论update,insert,replace,要涉及到外键的改变的,要确保父表的存在,否则会因为约束的存在,导致操作失败.







```
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
```



### 表关系：



#### One-to-Many Relationships

对于一个普通的博客应用来说，用户和文章显然是一个一对多的关系，一篇文章属于一个用户，一个用户可以写很多篇文章，那么他们之间的关系可以这样定义：

class User(Base):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    articles = relationship('Article')
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class Article(Base):

    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)

每篇文章有一个外键指向 users 表中的主键 id， 而在 User 中使用 SQLAlchemy 提供的 relationship 描述 关系。而用户与文章的之间的这个关系是双向的，所以我们看到上面的两张表中都定义了 relationship。

SQLAlchemy 提供了 backref 让我们可以只需要定义一个关系：

articles = relationship('Article', backref='author')

添加了这个就可以不用再在 Article 中定义 relationship 了！



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



#### One-to-One Relationships



在 User 中我们只定义了几个必须的字段， 但通常用户还有很多其他信息，但这些信息可能不是必须填写的，我们可以把它们放到另一张 UserInfo 表中，这样User 和 UserInfo 就形成了一对一的关系。你可能会奇怪一对一关系为什么不在一对多关系前面？那是因为一对一关系是基于一对多定义的：

class User(Base):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    articles = relationship('Article', backref='author')
    userinfo = relationship('UserInfo', backref='user', uselist=False)
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class UserInfo(Base):

    __tablename__ = 'userinfos'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    qq = Column(String(11))
    phone = Column(String(11))
    link = Column(String(64))
    user_id = Column(Integer, ForeignKey('users.id'))

定义方法和一对多相同，只是需要添加 userlist=False 。



#### Many-to-Many Relationships

一遍博客通常有一个分类，好几个标签。标签与博客之间就是一个多对多的关系。多对多关系不能直接定义，需要分解成俩个一对多的关系，为此，需要一张额外的表来协助完成：

article_tag = Table(
    'article_tag', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Tag(Base):

    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)




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







#### 自引用





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

	Flask-SQLAlchemy存在以下配置值，运行时从Flask app的主配置中加载。其中一些配置值在创建引擎之后无法修改。



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

	某些数据库后端可能会施加不同的非活动连接超时，这会干扰Flask-SQLAlchemy的连接池，例如默认情况下，MariaDB配置为600秒超时。 这通常难以调试，生产环境只有例外（2013: Lost connection to MySQL server during query）这条异常提示。
	
	如果使用具有较低连接超时的后端（或预先配置的数据库即服务），建议SQLALCHEMY_POOL_RECYCLE设置为小于后端超时的值。





## Multiple Databases with Binds（连接多个数据库）









## Signalling Support

首要条件：`SQLALCHEMY_TRACK_MODIFICATIONS` is enabled in the config

-  `models_committed`

  This signal is sent when changed models were committed to the database. The sender is the application that emitted the changes. The receiver is passed the `changes` parameter with a list of tuples in the form `(model instance, operation)`. The operation is one of `'insert'`, `'update'`, and `'delete'`. 

-  `before_models_committed`

  This signal works exactly like [`models_committed`](http://flask-sqlalchemy.pocoo.org/2.3/signals/#models_committed) but is emitted before the commit takes place. 







# Customizing









## API





extract

一种方法是先获取那个月份的第一天和最后一天的datetime，再使用`between`，例如：

```Python
# 基于Flask的SQLAlchemy

# models
class History(db.Model):
    __tablename__ = 'historys'
    id = db.Column(db.Integer, primary_key=True)
    date= db.Column(db.Date)
# firstDay：某年某月的第一天，datetime类型
# lastDay：某年某月的最后一天，datetime类型
historys = History.query.filter(History.date.between(firstDay, lastDay)).all()
```

关于获取某月份的第一天和最后一天，可以参考[这里](http://blog.csdn.net/yannanxiu/article/details/53809600)。



这个方法要使用`extract`函数，这个函数可以从datetime字段中分解出年月。不过在flask_sqlalchemy中没有`extract`，所以只能从sqlalchemy包导入。

```Python
from sqlalchemy import extract1
```

之后只需要这么写，就可以获取某月份的所有数据了

```Python
# 获取12月份的所有数据
historys = History.query.filter(extract('month', History.date) == 12).all()12
```

但是用上面的查询会把往年的12月也查询出来，那么就加上年份的查询

```Python
from sqlalchemy import extract, and_

historys = History.query.filter(_and(
    extract('year', History.date) == 2016,
    extract('month', History.date) == 12
).all()
```





“Group By”从字面意义上理解就是根据“By”指定的规则对数据进行分组，所谓的分组就是将一个“数据集”划分成若干个“小区域”，然后针对若干个“小区域”进行数据处理。

| 函数        | 作用         | 支持性               |
| ----------- | ------------ | -------------------- |
| sum(列名)   | 求和         |                      |
| max(列名)   | 最大值       |                      |
| min(列名)   | 最小值       |                      |
| avg(列名)   | 平均值       |                      |
| first(列名) | 第一条记录   | 仅Access支持         |
| last(列名)  | 最后一条记录 | 仅Access支持         |
| count(列名) | 统计记录数   | 注意和count(*)的区别 |

group by 一般和聚合函数一起使用才有意义,比如 count sum avg等,使用group by的两个要素:
    (1) 出现在select后面的字段 要么是是聚合函数中的,要么就是group by 中的.
    (2) 要筛选结果 可以先使用where 再用group by 或者先用group by 再用having
 下面看下 group by多个条件的分析:
 在SQL查询器输入以下语句
 create table test
 (
 a varchar(20),
 b varchar(20),
 c varchar(20)
 )
 insert into test values(1,'a','甲')
 insert into test values(1,'a','甲')
 insert into test values(1,'a','甲')
 insert into test values(1,'a','甲')
 insert into test values(1,'a','乙')
 insert into test values(1,'b','乙')
 insert into test values(1,'b','乙')
 insert into test values(1,'b','乙')
 第一次查询

select * from test; 结果如下图:

![img](http://dl.iteye.com/upload/attachment/0070/0159/3c12766b-18e8-339a-b8f1-b05e7a02b825.jpg)

结果中 按照b列来分:则是 5个a 3个b.


 按照c列来分:则是 4个甲 4个乙.


 第二次 按照 b列来分组 代码如下
 select   count(a),b from test group by b

![img](http://dl.iteye.com/upload/attachment/0070/0161/a9fce563-3cb7-3cbc-b12e-90e6561b42c3.jpg)

第三次 按照 c列来分组 代码如下
 select count(a),c from test group by c

![img](http://dl.iteye.com/upload/attachment/0070/0163/0a9e81c6-e246-37aa-8c59-2d0053d00254.jpg)

第四次 按照 b c两个条件来分组
 select count(a),b,c from test group by b,c

![img](http://dl.iteye.com/upload/attachment/0070/0165/7539f2cc-6157-386b-a908-1c0bafc2fc92.jpg)

第五次 按照 c b 顺序分组
 select count(a),b,c from test group by c,b

![img](http://dl.iteye.com/upload/attachment/0070/0167/39e0d458-47e2-32e9-93ed-1cd185cba0d9.jpg)
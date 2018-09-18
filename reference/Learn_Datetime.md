# Learn_Datetime

参考：

https://blog.csdn.net/google19890102/article/details/51355282
https://blog.csdn.net/orangleliu/article/details/73565593
https://blog.csdn.net/claroja/article/details/72677661?utm_source=itdadao&utm_medium=referral
https://www.cnblogs.com/sunshineyang/p/6818834.html
https://www.cnblogs.com/zhangxinqi/p/7687862.html



> 每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示，时间戳单位最适于做日期运算。但是1970年之前的日期就无法以此表示了。太遥远的日期也不行，UNIX和Windows只支持到2038年。





python中，有如下模块进行时间日期的处理：datetime，time，calendar（Calendar模块用来处理年历和月历）。





# datetime

datetime模块一共有如下子模块：

```
'MINYEAR': 1,
 'MAXYEAR': 9999,
 'timedelta': datetime.timedelta,
 'date': datetime.date,
 'tzinfo': datetime.tzinfo,
 'time': datetime.time,
 'datetime': datetime.datetime,
 'timezone': datetime.timezone,
 'datetime_CAPI': <capsule object "datetime.datetime_CAPI" at 0x7f5b448abf90>
```

| 类型                | 说明                                                         | 属性                                                        |
| ------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| datetime. date      | 公历日期                                                     | year，month和day                                            |
| datetime. time      | 每天精确地具有24*60*60秒                                     | hour、minute、second、microsecond和tzinfo                   |
| datetime. datetime  | 日期和时间的组合                                             | year、month、day、hour、minute、second、microsecond和tzinfo |
| datetime. timedelta | 表示两个date、time或datetime实例之间相差的时间，分辨率达到微秒 |                                                             |
| datetime. tzinfo    | 时区信息对象的抽象基类。提供自定义时间的调整（例如，计算时区和/或夏令时） |                                                             |
| datetime. timezone  | 实现tzinfo抽象基类的类，表示与UTC的固定偏移量                |                                                             |



## timedelta对象

### 基本介绍

class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0) 

内部只存储days、seconds 和 microseconds 。 所有的参数都将转换成这三个单位： 

- 1毫秒转换为1000微秒。 

- 1分钟转换为60秒。 

- 1小时转换为3600秒。 

- 1周被转换为7天。

### 类属性

| 类型                 | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| timedelta.min        | 最小的timedelta对象，timedelta(-999999999)                   |
| timedelta.max        | 最大的timedelta对象，timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999) |
| timedelta.resolution | 不相等的timedelta对象之间的最小可能差值，timedelta(microseconds=1) |

### 实例属性

| 属性         | 值                                                         |
| ------------ | ---------------------------------------------------------- |
| days         | 介于-999999999和999999999之间（包括-999999999和999999999） |
| seconds      | 介于0和86399之间（包括0和86399）                           |
| microseconds | 介于0和999999之间（包括0和999999）                         |

### 实例方法

| 方法                      | 值                                                          |
| ------------------------- | ----------------------------------------------------------- |
| timedelta.total_seconds() | 返回时间差中包含的总的秒数。等同于td / timedelta(seconds=1) |

### 可用操作

| 操作                                       | 结果                                                         |
| ------------------------------------------ | ------------------------------------------------------------ |
| t1 = t2 + t3                               | t2和t3的和。之后，t1-t2 == t3 and t1-t3 == t2为真。（1）     |
| t1 = t2 - t3                               | t2和t3的差。之后t1 == t2 - t3 and t2 == t1 + t3为真。（1）   |
| t1 = t2 * i 或 t1 = i * t2                 | Delta乘以一个整数。之后，如果i != 0，则t1 // i == t2为真。   |
| 通常，t1 * i == t1 * (i-1) + t1为真。（1） |                                                              |
| t1 = t2 * f 或 t1 = f * t2                 | Delta乘以一个浮点数。结果使用round-half-to-even舍入到timedelta.resolution最近的倍数。 |
| f = t2 / t3                                | t2除以t3（3）。返回一个float对象。                           |
| t1 = t2 / f 或 t1 = t2 / i                 | Delta除以一个浮点数或整数。结果使用round-half-to-even舍入到timedelta.resolution最近的倍数。 |
| t1 = t2 // i或t1 = t2 // t3                | 计算商，余数（如果有的话）被丢弃。在第二种情况下，返回一个整数。（3） |
| t1 = t2 ％ t3                              | 计算余数，为一个timedelta对象。（3）                         |
| q， r = divmod（t1， t2） t0>              | 计算商和余数：q = t1 // t2 (3)且r = t1 % t2。q一个是整数，r是一个timedelta对象。 |
| 0                                          | 返回具有相同值的timedelta对象。（2）                         |
| 0                                          | 等效于timedelta(-t1.days, -t1.seconds, -t1.microseconds)，和t1* -1。（1）（4） |
| abs(t)                                     | 当t.days >= 0时等效于+t，当t.days < 0时等效于-t。（2）       |
| str(t)                                     | 以[D day[s], ][H]H:MM:SS[.UUUUUU]形式返回一个字符串，其中对于负tD为负数。(5) |
| repr(t)                                    | 以datetime.timedelta(D[, S[, U]])形式返回一个字符串，其中对于负tD为负数。(5) |

## date对象

### 简介

class datetime.date(year, month, day) 
 classmethod date.today()

### 类属性

| 属性            | 值                                                      |
| --------------- | ------------------------------------------------------- |
| date.min        | 可表示的最早日期，date(MINYEAR, 1, 1)。                 |
| date.max        | 可表示最晚的日期，date(MAXYEAR, 12, 31)。               |
| date.resolution | 不相等的日期对象之间的最小可能差异，timedelta(days=1)。 |

### 实例属性

| 属性       | 值                                     |
| ---------- | -------------------------------------- |
| date.year  | 在MINYEAR和MAXYEAR之间，包括这两个值。 |
| date.month | 在 1 到 12 之间，包括 1 和 12。        |
| date.day   | 在 1 到给出的年份和月份之间的天数。    |

### 实例方法

| 方法                           | 说明                                                     |
| ------------------------------ | -------------------------------------------------------- |
| date.replace(year, month, day) | 依据关键字参数给出的新值，返回一个新的日期               |
| date.timetuple()               | 返回一个time.struct_time，类似time.localtime()的返回值。 |
| date.toordinal()               | 返回公历日期的序数，其中第1年的1月1日为第1天。           |
| date.weekday()                 | 返回一星期中的第几天，其中星期一是0，星期日是6。         |
| date.isocalendar()             | 返回一年中的第几周                                       |
| date.isoweekday()              | 返回一星期中的第几天，其中星期一是1，星期日是7。         |
| date.isoformat()               | 返回以ISO 8601 格式‘YYYY-MM-DD’表示日期的字符串。        |
| date.ctime()                   | 返回表示日期的字符串                                     |
| date.strftime(format)          | 返回一个表示日期的字符串，由显式的格式字符串控制。       |

### 支持的操作

| 操作                      | 结果                                                  |
| ------------------------- | ----------------------------------------------------- |
| date2 = date1 + timedelta | date2为从date1中移除timedelta.days天。（1）           |
| date2 = date1 - timedelta | 计算date2，以便date2 + timedelta == date1。（2）      |
| timedelta = date1 - date2 | -3                                                    |
| date1 date2               | 当date1在时间上位于date2之前，则date1小于date2。（4） |



## time对象

### 简介

class datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None) 

- 0 小时 24 

- 0 分钟 60 

- 0 秒 60 

- 0 微秒 1000000 

### 类属性

| 属性            | 值                                           |
| --------------- | -------------------------------------------- |
| time.min        | 可表示的最早的time，time(0, 0, 0, 0)         |
| time.max        | 可表示的最晚的time，time(23, 59, 59, 999999) |
| time.resolution | 不相等的time对象之间的最小可能差             |

### 实例属性

| 属性             | 值                                                           |
| ---------------- | ------------------------------------------------------------ |
| time.hour        | 在range(24)之间                                              |
| time.minute      | 在range(60)之间                                              |
| time.second      | time.second                                                  |
| time.microsecond | 在range(1000000)之间                                         |
| time.tzinfo      | 作为tzinfo参数传递给time构造函数的对象，如果没有传递则为None |

### 实例方法

| 方法                                                         | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| time.replace([hour[, minute[, second[, microsecond[, tzinfo]]]]]) | 返回具有相同值的time                                         |
| time.isoformat()                                             | 返回以ISO 8601 格式HH:MM:SS.mmmmmm表示间的字符串             |
| time.strftime(format)                                        | 返回一个表示time的字符串，由显式的格式字符串控制。           |
| time.utcoffset()                                             | 如果tzinfo为None，则返回None，否则返回self.tzinfo.utcoffset(None) |
| time.dst()                                                   | 如果tzinfo为None，则返回None，否则返回self.tzinfo.utcoffset(None) |
| time.tzname()                                                | 如果tzinfo为None，则返回None，否则返回self.tzinfo.tzname(None) |



## datetime对象

### 简介

class datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None) 
 classmethod datetime.today() 
 classmethod datetime.now(tz=None) 
 classmethod datetime.fromtimestamp(timestamp, tz=None) 
 classmethod datetime.fromordinal(ordinal)

### 类属性

| 属性                | 描述                                   |
| ------------------- | -------------------------------------- |
| datetime.min        | 可表示的最早datetime                   |
| datetime.max        | 可表示的最晚datetime                   |
| datetime.resolution | 不相等的datetime对象之间的最小可能差值 |

### 实例属性

| 属性                 | 描述                              |
| -------------------- | --------------------------------- |
| datetime.year        | 在MINYEAR和MAXYEAR之间            |
| datetime.month       | 在 1 到 12 之间，包括 1 和 12     |
| datetime.day         | 在 1 到给出的年份和月份之间的天数 |
| datetime.hour        | 在range(24)之间                   |
| datetime.minute      | 在range(60)之间                   |
| datetime.second      | 在range(60)之间                   |
| datetime.microsecond | 在range(1000000)之间              |



### 实例方法

| 方法                         | 说明                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| datetime.date()              | 返回具有相同年、月和日的date对象                             |
| datetime.time()              | 返回具有相同小时、分钟、秒和微秒的time对象                   |
| datetime.timetz()            | 返回具有相同小时、分钟、秒、微秒和tzinfo属性的time对象。     |
| datetime.replace()           | 返回具有相同属性的 datetime                                  |
| datetime.astimezone(tz=None) | 返回带有新tzinfo属性tz的datetime对象                         |
| datetime.toordinal()         | 返回日期的公历序数                                           |
| datetime.timestamp()         | 返回对应于datetime实例的POSIX时间戳                          |
| datetime.weekday()           | 返回一星期中的第几天，其中星期一是0，星期日是6               |
| date.isocalendar()           | 返回一年中的第几周                                           |
| datetime.isoweekday()        | 返回一星期中的第几天，其中星期一是1，星期日是7               |
| datetime.isoformat(sep=’T’)  | 返回以ISO 8601 格式YYYY-MM-DDTHH:MM:SS.mmmmmm表示日期和时间的字符串 |
| datetime.ctime()             | 返回一个表示日期和时间的字符串                               |
| datetime.strftime(format)    | 返回一个表示日期和时间的字符串，由显式的格式字符串控制       |





## 格式化时间

date、datetime和time对象都支持strftime(format)方法，在显式格式字符串的控制下创建一个表示时间的字符串

| 指令 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| %a   | 星期名称的区域性简写。                                       |
| %A   | 星期名称的区域性全称。                                       |
| %w   | 数字形式的星期，0表示星期日，6表示星期六。                   |
| %d   | 以0填充的十进制数字表示的月份中的日期。                      |
| %b   | 月份名称的区域性简写。                                       |
| %B   | 月份名称的区域性全称。                                       |
| %m   | 以0填充的十进制数表示的月份。                                |
| %y   | 以0填充的十进制数表示的不带世纪的年份。                      |
| %Y   | 以0填充的十进制数表示的带有世纪的年份。                      |
| %H   | 以0填充的十进制数表示的小时（24小时制）。                    |
| %I   | 以0填充的十进制数表示的小时（12小时制）。                    |
| %p   | AM或PM区域性设置。                                           |
| %M   | 以0填充的十进制数表示的分钟。                                |
| %S   | 以0填充的十进制数表示的秒数。                                |
| %f   | 十进制数表示的微秒，左边以0填充。                            |
| %z   | +HHMM或-HHMM形式的UTC偏移（如果对象是naive的，则为空字符串）。 |
| %Z   | 时区名称（如果对象是naive的，则为空字符串）。                |
| %j   | 以0填充的十进制数字表示的一年中的日期。                      |
| %U   | 以0填充的十进制数字表示的一年中的第几个星期（星期天作为一个星期的第一天）。新的一年中第一个星期天之前的所有日期都被认为是在第0个星期。 |
| %W   | 以0填充的十进制数字表示的一年中的第几个星期（星期一作为一个星期的第一天）。 新的一年中第一个星期一之前的所有日期都被认为是在第0个星期。 |
| %c   | 适合区域设置的日期和时间表示。                               |
| %x   | 适合区域的日期表示。                                         |
| %X   | 适合区域的时间表示。                                         |
| %%   | 字面值’％’字符。                                             |



### 时间元组

很多Python函数用一个元组装起来的9组数字处理时间

| 字段         | 属性     | 值                                                         |
| ------------ | -------- | ---------------------------------------------------------- |
| 4位年数      | tm_year  | 2017                                                       |
| 月           | tm_mon   | 1到12                                                      |
| 日           | tm_mday  | 1到31                                                      |
| 小时         | tm_hour  | 0到23                                                      |
| 分钟         | tm_min   | 0到59                                                      |
| 秒           | tm_sec   | 0到61（60或61是润秒）                                      |
| 一周的第几日 | tm_wday  | 0到6(0是周一)                                              |
| 一年的第几日 | tm_yday  | 1到366,一年中的第几天                                      |
| 夏令时       | tm_isdst | 是否为夏令时，值为1时是夏令时，值为0时不是夏令时，默认为-1 |


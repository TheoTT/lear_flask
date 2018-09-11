# Learn_模块与包

 记住，使用from Package import specific_submodule这种方法永远不会有错。事实上，这也是推荐的方法。除非是你要导入的子模块有可能和其他包的子模块重名。

   如果在结构中包是一个子包（比如这个例子中对于包:mod:sound来说），而你又想导入兄弟包（同级别的包）你就得使用导入绝对的路径来导入。比如，如果模块:mod:sound.filters.vocoder  要使用包:mod:sound.effects中的模块:mod:echo，你就要写成 from sound.effects import  echo。

```
from . import echo
from .. import formats
from ..filters import equalizer
```

 无论是隐式的还是显式的相对导入都是从当前模块开始的。主模块的名字永远是"__main__"，一个Python应用程序的主模块，应当总是使用绝对路径引用。 

   包还提供一个额外的属性，:attr:__path__。这是一个目录列表，里面每一个包含的目录都有为这个包服务的:file:__init__.py，你得在其他:file:__init__.py被执行前定义哦。可以修改这个变量，用来影响包含在包里面的模块和子包。  

 这个功能并不常用，一般用来扩展包里面的模块。 



 包是一种管理 Python 模块命名空间的形式，采用"点模块名称"。

 比如一个模块的名称是 A.B， 那么他表示一个包 A中的子模块 
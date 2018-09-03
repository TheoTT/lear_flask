"""
MVC:
M：Model ==> 数据库模型
V：Views ==> 可以理解为定义网页的地址，以及渲染网页等
C：Controller ==> 可以理解为 网页功能的逻辑，实现

render_template("index.html",name='name')传入的第一个参数是模板的文
件名称，它会去寻找一个名为templates的文件夹，在这个文件下去寻找模板index.html,并把参数name传入模板中。
其中：
    1.Flask(__name__,template_folder=”存放模板文件夹名称”)，在这里指定templates文件夹，名称及路径。
    2.

jinjia2到一些简单用法：

    {# … #} 模板中的注释
    {% … %} 用于执行for循环，if条件判断登语句

	{% for item in name %}
		<li>name:{{ item }} </li>
	{% endfor %}

     {{ …  }} 用于把表达式的结果输出到模板上，不止可以传数值，还能传列表，数组，字典等
	<center><h1>{{ name }}</h1></center>
	{{ name }}  接收render_template函数传过来的参数。

 @app.route('/test/<id>')
	尖括号里面的内容是动态的，凡是匹配到/user/前缀的URL都会映射到这个路由上，在内部将uid作为参数。默认的数值类型是字符串，如果需要指定其他类型，则需要其他写法
通常格式是 <converter:variable_name> 其中，冒号左边的 converter 有这样几种

    string 接受任何没有/的文本，这也是默认
    int 整数型
    float： 浮点型
    path： 路径，接受/

构造URL

Flask用url_for()函数构造url，用起来很方便。它的第一个参数是函数名.

举例：利用url_for()去构造一个有参数id=10，name=‘XeanYu’,age=16的一个URL
url_for('index',id=10,name='XeanYu',age=16)

跳转和重定向

跳转（状态码通常301） => 通常用于旧网址转移到了新网址

重定向(状态码通常302)  => 表示页面是暂时性的转移

在Flask中，重定向是 redirect

方法 Method

@app.route('/',methods=['GET','POST']),允许了GET和POST方法(GET方法为默认方法)

abort错误
用 redirect() 函数把用户重定向到其它地方。放弃请求并返回错误代码，用 abort() 函数



请求上下文之 request:

request.url :返回当前视图函数到url

request.method：请求方法

request.host：请求的主机名

request.file：获取请求中提交的文件

request.headers：请求头到dict

request.environ：返回一个列表，列表是 HTTP头的详情和 WSGI的详情，可用 request.environ.get()  来获取数据

request.remote_addr：客户端地址

request.user_agent:客户端的 User_Agent

form:  获取html表单提交的POST数据
args: 获取GET数据
values: 是form和args的结合，既包括表单数据，也包括args数据
json: 如果客户端提交的是json数据，则用本方法去解析
is_xhr: 返回True或是False。用于判断客户端是否是通过JavaScrpt的XMLHttpRequest提交的，其实就是Ajax提交

请求上下文之一  Session

默认情况下，用户回话保存在客户端的cookie中，使用设置的 SECRET_KEY 进行加密签名，如果篡改了cookie的内容，签名就会失效，回话也会消失





"""

import os
from flask import Flask,render_template,redirect,abort,request,session

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = os.urandom(24)#使用os.urandom生成随机key
)


#导入配置对象
"""
从应用主目录中到config.py文件中导入含有配置选项的类

"""
#app.config.from_object(devEnv)

#从文件导入配置
"""
 从config.conf文件中导入配置

"""
#app.config.from_pyfile(config.conf,silent=True)

app.config.update


name = ['a','b','c','d','e','f','lee']

#测试跳转
@app.route('/<id>')
def redir(id):
    return redirect('/test/%s'%(int(id)))



#测试跳转并指定错误
@app.route('/testerror')
def testAbort():
    return redirect('/error')

@app.route('/error')
def error():
    abort(401)

@app.route('/test/<id>')
def index(id):
#    return "<h1>这是第一个flask程序</h1>"
    return render_template('index.html',name=name[int(id)])



#获取前端数据

@app.route('/get/',methods=['GET','POST'])
def getdata():
    if request.method =='GET':
        #name = request.args.get('name')
        #age = request.args.get('age')
       #print("name:%s  age:%s"%(name,age))
        return render_template('index.html')
    if request.method =='POST':
        name = request.form.get('name')
        age = request.form.get('age')
        return render_template('index.html',name=name,age=age)


#session
@app.route('/session/',methods=['GET','POST'])
def testSess():
    if request.method =='GET':
        return render_template("session.html",id=session.get('id'))

    session['id'] = request.form.get('id')
    return render_template('session.html',id=session.get('id'))

#自定义错误
@app.errorhandler(404)
def error_404(error):
    return '404 Not Found',404



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,debug=True)

import os
import time
from flask import Flask, render_template, redirect, abort, request, session,url_for
from webargs import fields, validate
from flask_sqlalchemy import SQLAlchemy

conments = []
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////tmp/test.db'    #加上数据库配置
db = SQLAlchemy(app)    #创建SQLALchemy对象，将flask app作为参数传入

"""
SQLALchemy对象创建后，会包含sqlalchemy及sqlalchemy.orm中的所有方法及属性，
其中Model类用于声明模型时到declarative基类

"""


@app.route('/testPost/',methods=['POST','GET'])
def test():
    if request.method == 'GET':
        return  render_template('postTest.html')
    else :
        print(request.values.get("user"))
        return 'OK'

@app.route('/blog/',methods=['GET','POST'])
def index():
    if request.method =='GET':
        return render_template('index.html',conments=conments)


    else:
        user = request.form.get("user")
        title = request.form.get("title")
        conment = request.form.get("conment")
        date = time.strftime("%Y-%m-%d %H:%M:%s",time.localtime())

        conments.append({
                    'user': user,
                    'title': title,
                    'conment': conment,
                    'createTime': date
                    })

        return redirect(url_for('index'))

"""
数据类型：
Integer-自增长类型


"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    created_time = db.Column()
    title = db.Column()
    conment = db.Column()

    def __init__(self, username, title, conment):
        self.username = username
        self.created_time = []

        self.title = title
        self.conment = conment

    def __repr__(self):
        return '<User %r>' % self.username



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,debug=True)

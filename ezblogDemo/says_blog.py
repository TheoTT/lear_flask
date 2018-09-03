"""
1.实现简单留言板（没有样式，无数据库）//done
2.加上数据库（关系postgre，非关系mongo）
3.使用docker部署
4.加上样式
5.加上js效果

"""



from flask import Flask,request,render_template,redirect,url_for
import time
app = Flask(__name__)

users = [] # 这里存放所有的留言

@app.route('/say/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index1.html',says=users)

    else:
        title = request.form.get('say_title')
        text = request.form.get('say')
        user = request.form.get('say_user')
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

        users.append({"title": title,
                      "text":text,
                      "user":user,
                      "date": date})

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,)

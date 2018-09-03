
import os
import time
from flask import Flask,render_template,redirect,abort,request,session,url_for

conments = []
app = Flask(__name__)


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

        print(conments)
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,debug=True)



import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from blogApp.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')#url_prefix 会添加到所有与该蓝图关联的 URL 前面

#注册

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Blueprint 是一种组织一组相关视图及其他代码的方式。与把视图及其他 代码直接注册到应用的方式不同，蓝图方式是把它们注册到蓝图，然后在工厂函数中 把蓝图注册到应用
    @bp.route 关联了 URL /register 和 register 视图函数,当 Flask 收到一个指向 /auth/register 的请求时就会调用 register 视图并把其返回值作为响应。
    db.execute 使用了带有 ? 占位符 的 SQL 查询语句。占位符可以代替后面的元组参数中相应的值。使用占位符的 好处是会自动帮你转义输入值，以抵御 SQL 注入攻击
    fetchone() 根据查询返回一个记录行。 如果查询没有结果，则返回 None 。
    fetchall() ，它返回包括所有结果的列表。
    generate_password_hash() 生成安全的哈希值并储存 到数据库中
    url_for() 根据登录视图的名称生成相应的 URL
    redirect() 为生成的 URL 生成一个重定向响应
    flash() 用于储存在渲染模块时可以调用的信息。
    render_template() 会渲染一个包含 HTML 的模板。
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

#登录

@bp.route('/login',methods=(['POST','GET']))
def login():
    """
    check_password_hash() 以相同的方式哈希提交的 密码并安全的比较哈希值。
    session 是一个 dict ，它用于储存横跨请求的值。当验证 成功后，用户的 id 被储存于一个新的会话中。
    会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返回它。
    Flask 会安全对数据进行 签名 以防数据被篡改
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',(username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password.'


        if error is None:
            session.clear()
            session['user_id'] = user['id']#id 已被储存在 session 中，可以被后续的请求使用(如果验证成功)
            return redirect(url_for('index'))
        flash(error)

    return render_template('auth/login.html')

#加载已经登录成功到user

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user =None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',(user_id,)
        ).fetchone()



#注销已经登录的user
@bp.route('/logout')
def logout():
    session.clear()#将用户id从session中移除
    return redirect(url_for('index'))

#在其他视图中对用户进行验证
def login_required(view):
    """
装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户 是否已载入。如果已载入，那么就继续正常执行原视图，
否则就重定向到登录页面。
    :param view:
    :return:
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()

import os

from flask import Flask


def create_app(test_config=None):
    """
    application factory function
    __name__ 是当前 Python 模块的名称
    instance_relative_config=True 告诉应用配置文件是相对于 instance folder 的相对路径(instance folder在 flaskr 包的外面，用于存放本地数据（例如配置密钥和数据库），不应当 提交到版本控制系统)
    app.config.from_mapping() 设置一个应用的 缺省配置



    :param test_config:
    :return:
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',#SECRET_KEY 是被 Flask 和扩展用于保证数据安全的。在开发过程中， 为了方便可以设置为 'dev' ，但是在发布的时候应当使用一个随机值来 重载它
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),# DATABASE SQLite 数据库文件存放在路径。它位于 Flask 用于存放实例的 app.instance_path 之内
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)#app.config.from_pyfile() 使用 config.py 中的值来重载缺省配置，如果 config.py 存在
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        #print(app.instance_path)
        os.makedirs(app.instance_path)#确保 app.instance_path 存在
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    #导入，注册auth蓝图
    from . import auth
    app.register_blueprint(auth.bp)     #app.register_blueprint() 在工厂中 导入和注册蓝图

    # 导入，注册blog蓝图
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

	

    return app

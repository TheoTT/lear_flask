"""
传说中的应用工厂函数

主要功能：
1.创建flask实例，加载配置
2.注册蓝图，数据库



"""
from flask import Flask, request, render_template, redirect, url_for


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev'
        )


    @app.route('/hello/')
    def hello():
        return "<center><h1>hello world!</h1></center>"
    return app
app = create_app()

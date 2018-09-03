import sqlite3

import pytest
from blogApp.db import get_db


def test_get_close_db(app):
    """
    在一个应用环境中，每次调用 get_db 都应当返回相同的连接。退出环境后， 连接应当已关闭。
    :param app:
    """
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e)


def test_init_db_command(runner, monkeypatch):
    """
    init-db 命令应当调用 init_db 函数并输出一个信息
    :param runner:
    :param monkeypatch:
    """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('blogApp.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'initialized the database.' in result.output
    assert Recorder.called


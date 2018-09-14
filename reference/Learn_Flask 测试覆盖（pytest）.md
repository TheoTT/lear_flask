Flask 测试覆盖（pytest）

参考：

	https://dormousehole.readthedocs.io/en/latest/tutorial/tests.html

https://dormousehole.readthedocs.io/en/latest/testing.html

	https://blog.csdn.net/huitailang1991/article/details/74053781



https://pytest-flask.readthedocs.io/en/latest/tutorial.html

https://docs.pytest.org/en/latest/contents.html#toc

https://docs.pytest.org/en/latest/plugins.html





构造测试数据：

https://pypi.org/project/mimesis-factory/0.0.2/

https://www.jianshu.com/p/60ae91b29def

https://github.com/pytest-dev/pytest-factoryboy

https://github.com/mimesis-lab/mimesis-factory

https://pypi.org/project/mimesis/0.0.6/

https://mimesis.readthedocs.io/advanced.html#using-with-orm

http://joke2k.net/faker/













如何在构造test请求时，传递参数：

```
self.app.post('/path-to-request', data=dict(var1='data1', var2='data2', ...))
self.app.get('/path-to-request', query_string=dict(arg1='data1', arg2='data2', ...))


from . import BaseTest
from erp.models import ProfitCenter, Material

#第一种
class TestMmCode(BaseTest):

    def test_chart_inventory_analysis(self, client):
        profit_center_id = ProfitCenter.query.first().id
        year = Material.query.first().date.year
        params = {
            'profit_center_id': profit_center_id,
            'year': year
        }

        resp = client.get(
            '/api/mm/chart/inventory-analysis', query_string=params)
        assert resp.json[0]['year'] == 2018
        assert resp.json[0]['quantity'] == 123


#第二种
class TestMmCode(BaseTest):

    def test_chart_inventory_analysis(self, client):
        profit_center_id = ProfitCenter.query.first().id
        year = Material.query.first().date.year
        params = {
            'profit_center_id': profit_center_id,
            'year': year
        }

        resp = client.get(
            '/api/mm/chart/inventory-analysis', query_string=params)
        #使用url_for()
        resp = client.get(url_for('mm.chart_inventory_analysis', profit_center_id=profitcenter)
        assert resp.json[0]['year'] == 2018
        assert resp.json[0]['quantity'] == 123
```





```
#to use test_request_context

import unittest
from myapp import extract_query_params

testapp = flask.Flask(__name__)

class TestFoo(unittest.TestCase):
    def test_happy(self):
        with testapp.test_request_context('?limit=1&offset=2'):
            limit, offset = extract_query_params(['limit', 'offset'])
            self.assertEquals(limit, 1)
            self.assertEquals(offset, 2)
```



    #a complete code example of a unit test
    
    testapp = app.test_client()
    
    class Test_test(unittest.TestCase):
        def test_user_registration_bad_password_short(self):
            response = self.register(name='pat',
                                     email='me@mail.com', 
                                     password='Flask', 
                                     password2='Flask')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'password should be 8 or more characters long', 
                          response.data)
    
    def register(self, name, email, password, password2):
        return testapp.post(
            '/register',
            data=dict(username=name, 
                      email=email, 
                      password=password, 
                      password2=password2),
            follow_redirects=True
        )




遇到的问题：

E           sqlalchemy.exc.StatementError: (builtins.TypeError) SQLite Date type only accepts Python date objects as input. [SQL: 'INSERT INTO materials (no, name, type, inventory_quantity, inventory_amount, date, profit_center_id) VALUES (?, ?, ?, ?, ?, ?, ?)'][parameters: [{'name': 'test', 'profit_center_id': 1, 'no': '1', 'inventory_amount': 13838.12, 'date': '2018-08-08', 'inventory_quantity': 123, 'type': None}]]

/home/t/.local/share/virtualenvs/sky-erp-Xrn8-nDU/lib/python3.6/site-packages/sqlalchemy/dialects/sqlite/base.py:671: StatementError




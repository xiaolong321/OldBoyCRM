from django.test import TestCase,Client
from crm import views

# Create your tests here.

class crm_tests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_hashstr(self):
        self.assertEqual(views.hashstr('123'), '202cb962ac59075b964b07152d234b70')

    def test_makePassword(self):
        data = views.makePassword()
        lenth = len(data)
        self.assertLessEqual(lenth, 12)
        self.assertGreaterEqual(lenth, 5)

    def test_addcustomer(self):
        ret = self.client.login(username='qjl@qq.com', password='qjl171012')
        self.client.session
        # ret = self.client.post('/crm/login/', {'username': 'qjl@qq.com', 'password': 'qjl171012', 'next': '/crm/'})
        response = self.client.get('/crm/addcustomer/')
        print('7777777777', response, '888888888', ret)
        self.assertEqual(response.status_code, 200)


    def test_searchcustomer(self):
        ret = self.client.post('/crm/login/', {'username': 'qjl@qq.com', 'password': 'qjl171012', 'next': '/crm/'})
        response = self.client.post('/crm/searchcustomer')
        print('+++++++', response)
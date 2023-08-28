import unittest
from app import app

class TestCurrencyExchange(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.app = app.test_client()
    
    def test_hello(self):
        response = self.app.get('/hello')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('message', ''), 'Hello world')

    def test_convert_currency_success(self):
        response = self.app.get('/api/v1/exchange?source=USD&target=JPY&amount=$1,525')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['source'], 'USD')
        self.assertEqual(data['target'], 'JPY')
        self.assertTrue('exchange_rate' in data)
        self.assertTrue('amount' in data)
        self.assertTrue('converted_amount' in data)

    def test_convert_currency_fail(self):
        response = self.app.get('/api/v1/exchange?source=USD&target=JPY&amount=asdf')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error' in data)

if __name__ == '__main__':
    unittest.main()
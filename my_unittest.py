import unittest
import requests

class TestBookAPI(unittest.TestCase):

    # 初始化设置
    def setUp(self):
        self.base_url = 'http://localhost:8000'

    # 测试创建图书接口
    def test_a_create_book(self):
        url = self.base_url + '/book'
        data = {
            'title': 'test title',
            'author': 'test author',
            'publisher': 'test publisher',
            'publish_time': '2023-01-01',
            'price': 6.66,
            'score': 5.0,
            'description': 'test description'
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], 'Book created successfully')

    # 测试获取图书列表接口
    def test_b_get_books(self):
        url = self.base_url + '/book'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'success')

    # 测试更新图书接口
    def test_c_update_book(self):
        url = self.base_url + '/book'
        data = {
            'title': 'test title',
            'author': 'test author v2'
        }
        response = requests.put(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], 'Book updated successfully')

    # 测试删除图书接口
    def test_d_delete_book(self):
        url = self.base_url + '/book'
        data = {
            'title': 'test title'
        }
        response = requests.delete(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], "Book deleted successfully")
        response = requests.delete(url, json=data)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python
"""
API测试脚本
用于测试用户认证和订单管理接口
"""

import requests
import json
import sys
import os

# 添加Django项目到路径
sys.path.append('/home/hyy/code/app_server')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_server.settings')

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
    
    def print_response(self, response):
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        except:
            print(f"Response: {response.text}")
        print("-" * 50)
    
    def test_register(self):
        """测试用户注册"""
        print("测试用户注册...")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "测试",
            "last_name": "用户",
            "phone": "13800138000"
        }
        
        response = requests.post(f"{self.base_url}/auth/register/", json=data)
        self.print_response(response)
        
        if response.status_code == 201:
            result = response.json()
            self.token = result['token']
            self.user_id = result['user']['id']
            print(f"注册成功，Token: {self.token}")
        
        return response.status_code == 201
    
    def test_login(self):
        """测试用户登录"""
        print("测试用户登录...")
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        response = requests.post(f"{self.base_url}/auth/login/", json=data)
        self.print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['token']
            self.user_id = result['user']['id']
            print(f"登录成功，Token: {self.token}")
        
        return response.status_code == 200
    
    def test_profile(self):
        """测试获取用户信息"""
        print("测试获取用户信息...")
        headers = {"Authorization": f"Token {self.token}"}
        
        response = requests.get(f"{self.base_url}/auth/profile/", headers=headers)
        self.print_response(response)
        
        return response.status_code == 200
    
    def test_create_order(self):
        """测试创建订单"""
        print("测试创建订单...")
        headers = {"Authorization": f"Token {self.token}"}
        data = {
            "receiver_name": "张三",
            "receiver_phone": "13900139000",
            "receiver_address": "北京市朝阳区某某街道某某号",
            "notes": "请在工作时间送货",
            "items": [
                {
                    "product_name": "iPhone 15",
                    "product_sku": "IP15-128G-BLK",
                    "product_image": "https://example.com/iphone15.jpg",
                    "quantity": 1,
                    "unit_price": "5999.00"
                },
                {
                    "product_name": "保护壳",
                    "product_sku": "CASE-IP15-BLK",
                    "quantity": 2,
                    "unit_price": "99.00"
                }
            ]
        }
        
        response = requests.post(f"{self.base_url}/orders/", json=data, headers=headers)
        self.print_response(response)
        
        if response.status_code == 201:
            result = response.json()
            self.order_id = result['data']['id']
            print(f"订单创建成功，订单ID: {self.order_id}")
        
        return response.status_code == 201
    
    def test_list_orders(self):
        """测试获取订单列表"""
        print("测试获取订单列表...")
        headers = {"Authorization": f"Token {self.token}"}
        
        response = requests.get(f"{self.base_url}/orders/", headers=headers)
        self.print_response(response)
        
        return response.status_code == 200
    
    def test_get_order_detail(self):
        """测试获取订单详情"""
        if not hasattr(self, 'order_id'):
            print("跳过订单详情测试：没有订单ID")
            return True
            
        print("测试获取订单详情...")
        headers = {"Authorization": f"Token {self.token}"}
        
        response = requests.get(f"{self.base_url}/orders/{self.order_id}/", headers=headers)
        self.print_response(response)
        
        return response.status_code == 200
    
    def test_update_order_status(self):
        """测试更新订单状态"""
        if not hasattr(self, 'order_id'):
            print("跳过订单状态更新测试：没有订单ID")
            return True
            
        print("测试更新订单状态...")
        headers = {"Authorization": f"Token {self.token}"}
        data = {
            "status": "paid",
            "notes": "用户已付款"
        }
        
        response = requests.patch(f"{self.base_url}/orders/{self.order_id}/update_status/", 
                                json=data, headers=headers)
        self.print_response(response)
        
        return response.status_code == 200
    
    def test_order_statistics(self):
        """测试订单统计"""
        print("测试订单统计...")
        headers = {"Authorization": f"Token {self.token}"}
        
        response = requests.get(f"{self.base_url}/orders/statistics/", headers=headers)
        self.print_response(response)
        
        return response.status_code == 200
    
    def test_logout(self):
        """测试用户登出"""
        print("测试用户登出...")
        headers = {"Authorization": f"Token {self.token}"}
        
        response = requests.post(f"{self.base_url}/auth/logout/", headers=headers)
        self.print_response(response)
        
        return response.status_code == 200
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始API测试...")
        print("=" * 50)
        
        tests = [
            ("用户注册", self.test_register),
            ("用户登录", self.test_login),
            ("获取用户信息", self.test_profile),
            ("创建订单", self.test_create_order),
            ("获取订单列表", self.test_list_orders),
            ("获取订单详情", self.test_get_order_detail),
            ("更新订单状态", self.test_update_order_status),
            ("订单统计", self.test_order_statistics),
            ("用户登出", self.test_logout),
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = "✓ 通过" if result else "✗ 失败"
                print()
            except Exception as e:
                results[test_name] = f"✗ 错误: {str(e)}"
                print(f"错误: {str(e)}")
                print()
        
        print("测试结果汇总:")
        print("=" * 50)
        for test_name, result in results.items():
            print(f"{test_name}: {result}")


if __name__ == "__main__":
    print("注意: 请确保Django服务器正在运行 (python manage.py runserver)")
    print("如果是首次运行，请先执行数据库迁移:")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print()
    
    tester = APITester()
    tester.run_all_tests()
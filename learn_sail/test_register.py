import requests
import json

# 测试注册端点
url = 'http://127.0.0.1:8000/api/users/register/'
headers = {'Content-Type': 'application/json'}
# 使用一个不会与现有用户冲突的用户名
data = {
    'username': 'testuser_new',
    'email': 'test_new@example.com',
    'password': 'testpassword123',
    'confirm_password': 'testpassword123',
    'phone': '1234567890'
}
"""
# 测试注册端点
{
  "username": "testuser_apifox",
  "email": "test_apifox@example.com",
  "password": "testpassword123",
  "confirm_password": "testpassword123",
  "phone": "1234567890"
}
"""

print(f'Sending POST request to {url}')
response = requests.post(url, headers=headers, data=json.dumps(data))

print(f'Response status code: {response.status_code}')
print(f'Response content: {response.text}')
if response.status_code == 201:
    print('Registration successful!')
else:
    print('Registration failed.')
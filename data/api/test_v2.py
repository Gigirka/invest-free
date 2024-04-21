from requests import get, delete, post

print(get('http://localhost:8185/api/v2/users').json())
print(get('http://localhost:8185/api/v2/users/5').json())
print(get('http://localhost:8185/api/v2/users/-1').json())
print(get('http://localhost:8185/api/v2/users/q').json())

print(delete('http://localhost:8185/api/v2/users/999').json())  # id = 999 нет в базе
print(delete('http://localhost:8185/api/v2/users/9').json())
print(post('http://localhost:8185/api/v2/users').json())  # нет словаря
print(post('http://localhost:8185/api/v2/users', json={'name': 'Ваня'}).json())  # не все поля
print(post('http://localhost:8185/api/v2/users', json={'type': 'investor', 'name': 'Ван3я3',
                                                       'age': 137, 'email': '103@mars.org', 'money': 123, 'exp': 'fds',
                                                       'personal': 'gfd', 'capital': 2322, 'private_or_fund': 'private',
                                                       'qualification': 'нет', 'speciality': 'прог3',
                                                       'address': 'module_3', 'password': '1233'}).json())

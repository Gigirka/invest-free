from requests import get, delete, post

print(get('http://localhost:8181/api/v2/users').json())
print(get('http://localhost:8181/api/v2/users/2').json())
print(get('http://localhost:8181/api/v2/users/-1').json())
print(get('http://localhost:8181/api/v2/users/q').json())

print(delete('http://localhost:8181/api/v2/users/999').json())  # id = 999 нет в базе
print(delete('http://localhost:8181/api/v2/users/3').json())
print(post('http://localhost:8183/api/v2/users').json())  # нет словаря
print(post('http://localhost:8183/api/v2/users', json={'name': 'Ваня'}).json())  # не все поля
print(post('http://localhost:8183/api/v2/users', json={'name': 'Ваня3', 'position': 'кок3',
                                                       'surname': 'Иванов3', 'age': 137, 'address': 'module_3',
                                                       'speciality': 'прог3',
                                                       'hashed_password': '1233', 'email': '1233@mars.org'}).json())

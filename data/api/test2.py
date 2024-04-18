from requests import get, post


print(post('http://localhost:8185/api/jobs',
           json={'project_name': 'installing a long-distance communication antenna', 'work_size': 5, 'user_id': 8,
                 'info': 'asddasasd', 'needed_money': 5, 'invested_money': 1, 'is_finished': True}).json())
print(post('http://localhost:8185/api/jobs', json={}).json())

print(post('http://localhost:8185/api/jobs',
           json={'job': '!!!'}).json())

print(get('http://localhost:8185/api/jobs').json())

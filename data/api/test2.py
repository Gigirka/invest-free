from requests import get, post


print(post('http://localhost:8008/api/jobs',
           json={'job': 'installing a long-distance communication antenna', 'team_leader': 1, 'work_size': 5,
                 'collaborators': '6, 3', 'is_finished': True}).json())
print(post('http://localhost:8008/api/jobs', json={}).json())

print(post('http://localhost:8008/api/jobs',
           json={'job': '!!!'}).json())

print(get('http://localhost:8008/api/jobs').json())

from requests import get

print(get('http://localhost:8008/api/jobs').json())

print(get('http://localhost:8008/api/jobs/1').json())

print(get('http://localhost:8008/api/jobs/999').json())

print(get('http://localhost:8008/api/jobs/abc').json())
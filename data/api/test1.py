from requests import get
import json

print(get('http://localhost:8185/api/jobs').json())

print(get('http://localhost:8185/api/jobs/1').json())

print(get('http://localhost:8185/api/jobs/999').json())

print(get('http://localhost:8185/api/jobs/abc').json())
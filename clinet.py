from requests import get, post

#response = get("http://localhost:8080/task", data={'task_id': 1})
response = get("http://localhost:8080/user/1")
print(response.json())


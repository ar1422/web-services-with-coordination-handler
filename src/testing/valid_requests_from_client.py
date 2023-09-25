import requests
s = requests


def valid_conversation_1():
    resource_url = 'http://127.0.0.1:8000/search/search_movies'
    params = {"search_string": "The Shawshank Redemption"}
    headers = {"username": "user_123", "password": "password_123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)

    resource_url = 'http://127.0.0.1:8000/rank/rank_movies'
    params = {"search_string": "The Shawshank Redemption", "rating": 9.5}
    headers = {"username": "user_123", "password": "password_123",
               "conversation_id": response.headers.get("conversation_id")}
    response = s.post(resource_url, json=params, headers=headers)
    print(response.content)


def valid_conversation_2():
    resource_url = 'http://127.0.0.1:8000/search/search_tv_series'
    params = {"search_string": "Breaking Bad"}
    headers = {"username": "user_123", "password": "password_123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)

    resource_url = 'http://127.0.0.1:8000/rank/rank_tv_series'
    params = {"search_string": "Breaking Bad", "rating": 9.5}
    headers = {"username": "user_123", "password": "password_123",
               "conversation_id": response.headers.get("conversation_id")}
    response = s.post(resource_url, json=params, headers=headers)
    print(response.content)


if __name__ == '__main__':
    print("Case 1 output - ")
    valid_conversation_1()
    print("Case 2 output - ")
    valid_conversation_2()

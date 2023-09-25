import requests
s = requests


def invalid_conversation_1():
    """
    Function to test invalid case where username and password is not included in the header.
    :return: An Error response code with Message asking for username and password.
    """
    resource_url = 'http://127.0.0.1:8000/search/search_movies'
    params = {"search_string": "The Shawshank Redemption"}
    response = s.get(resource_url, params=params)
    print(response.content)


def invalid_conversation_2():
    """
    Function to test invalid case where an invalid username and password is included in the header.
    :return: An Error response code with Message asking for username and password.
    """
    resource_url = 'http://127.0.0.1:8000/search/search_movies'
    params = {"search_string": "The Shawshank Redemption"}
    headers = {"username": "Arya Girisha Rao", "password": "password123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)


def invalid_conversation_3():
    resource_url = 'http://127.0.0.1:8000/search/search_movies'
    params = {"search_string": "The Shawshank Redemption"}
    headers = {"username": "user_123", "password": "password_123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)

    resource_url = 'http://127.0.0.1:8000/rank/rank_movies'
    params = {"search_string": "The Shawshank Redemption", "rating": 9.5}
    headers = {"username": "user_123", "password": "password_123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)


def invalid_conversation_4():

    resource_url = 'http://127.0.0.1:8000/rank/rank_movies'
    params = {"search_string": "The Shawshank Redemption", "rating": 9.5}
    headers = {"username": "user_123", "password": "password_123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)


def invalid_conversation_5():
    resource_url = 'http://127.0.0.1:8000/search/search_movies'
    params = {"search_string": "The Shawshank Redemption"}
    headers = {"username": "user_123", "password": "password_123"}
    response = s.get(resource_url, params=params, headers=headers)
    print(response.content)

    resource_url = 'http://127.0.0.1:8000/rank/rank_tv_series'
    params = {"search_string": "The Shawshank Redemption", "rating": 9.5}
    headers = {"username": "user_123", "password": "password_123",
               "conversation_id": response.headers.get("conversation_id")}
    response = s.post(resource_url, json=params, headers=headers)
    print(response.content)


if __name__ == '__main__':
    print("Case 1 output - ")
    invalid_conversation_1()
    print("Case 2 output - ")
    invalid_conversation_2()
    print("Case 3 output - ")
    invalid_conversation_3()
    print("Case 4 output - ")
    invalid_conversation_4()
    print("Case 5 output - ")
    invalid_conversation_5()

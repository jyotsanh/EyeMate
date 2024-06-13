from django.test import TestCase

# Create your tests here.
import requests
import json

def login_test():
    URL = "http://127.0.0.1:8000/api/user/login/"
    data = {
        'email':'jyotsan.hamal2027@pcmgmt.edu.np',
        'password':'password321'
    }
    response = requests.post(url=URL, data=data)

    if response.status_code == 200:
        # Login successful, extract tokens from the response
        tokens = response.json()

        print(tokens)
    else:
        # Login failed, print error message
        print("Login failed:", response.json())

def logout_test():
    URL = "http://127.0.0.1:8000/api/user/logout/"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3ODY1MDc3LCJpYXQiOjE3MTc4NjQxNzcsImp0aSI6ImVlMzNiNDIzYmExZTRjMDk4ZWY1NTg1YTYzMTRhZTY2IiwidXNlcl9pZCI6NH0.-_-1vA_gyWjHcUVS_T_9Ap2IxghnnXGzkNFW5GpTUb4',
        
        'Content-Type': 'application/json'
    }
    data = {
        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzk1MDU3NywiaWF0IjoxNzE3ODY0MTc3LCJqdGkiOiI2NzcyOTQ1ZTljNGM0OTM4YTMyNzk0N2MwNmMzODkyMiIsInVzZXJfaWQiOjR9.n6XVD9M6Gfi3mUFJXQwSIjMW79s06dg4XJ0zqj7KnmA'
    }
    
    response = requests.post(url=URL, headers=headers, json=data)
    print(response.json())
def register_test():
    url = "http://127.0.0.1:8000/api/user/register/"
    data = {
        'email': 'jyotsan.hamal2027@pcmgmt.edu.np',
        'username': 'testuser05',
        'first_name': 'Test05',
        'last_name': 'User05',
        'password': 'password123',
        'password2': 'password123',
    }

    # Send POST request with JSON data and correct Content-Type header
    response = requests.post(url, json=data)

    # Print response
    print(response.json())

def profile_test():
    URL = "http://127.0.0.1:8000/api/user/profile/"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MjEwOTQyLCJpYXQiOjE3MTgyMTA4ODIsImp0aSI6IjhmNTRjNTRkZjY5YTRmNzhhNDE0ODc4MGE1YjAwY2I1IiwidXNlcl9pZCI6OH0.0ZsYQ-Rsoc7Ls3VMMzFkjbouIWouuqJgp37JwL7b0lU'
    }
    
    response = requests.get(url=URL, headers=headers)
    print(response.json())

def otp_test():
    URL = "http://127.0.0.1:8000/api/user/reset-password/"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MjQyNTQ1LCJpYXQiOjE3MTgyNDIyNDUsImp0aSI6ImM5Mjk0ZjFjMzVkYjRiYjU5ZTYyMmIxOTAxNjQyZGZkIiwidXNlcl9pZCI6OH0.I0FXxkxGPINZKXi690E7bvu7Okiruig99UtX5ML_UiM'
    }
    
    data = {
        'email': 'jyotsan.hamal2027@pcmgmt.edu.np',
    }
    response = requests.post(url=URL, data=data, headers=headers)
    print(response.json())
    
def otp_reset_password():
    otp_code = '336911'
    URL = "http://127.0.0.1:8000/api/user/verify-reset-password/"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MjExNDIyLCJpYXQiOjE3MTgyMTExMjIsImp0aSI6ImNkNmEzMjJiZjVhZTQzYjI4NTAyODU4OGJhZGNjMDA2IiwidXNlcl9pZCI6OH0.XeIix175V8I81mPlKBkS6CEqxEyaQ3NIXwLJMcsN__8'
    }
    data = {
        'email': 'jyotsan.hamal2027@pcmgmt.edu.np',
        'new_password':'password321',
        'otp_code':otp_code
    }
    response = requests.post(url=URL, data=data, headers=headers)
    print(response.json())
    
otp_test()
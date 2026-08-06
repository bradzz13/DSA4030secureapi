import requests


BASE_URL = "http://127.0.0.1:5000"


def print_result(test_name, response):

    print("\n" + "=" * 60)

    print(test_name)

    print("=" * 60)

    print("Status Code:", response.status_code)

    print("Response:", response.json())


# TEST 1: UNAUTHENTICATED ACCESS

response = requests.get(
    f"{BASE_URL}/customers"
)

print_result(
    "TEST 1 - Unauthenticated Access",
    response
)


# TEST 2: INVALID JWT

response = requests.get(

    f"{BASE_URL}/customers",

    headers={
        "Authorization": "Bearer invalid.token.here"
    }

)

print_result(
    "TEST 2 - Invalid JWT",
    response
)


# TEST 3: WRONG CREDENTIALS

response = requests.post(

    f"{BASE_URL}/login",

    json={

        "username": "admin",

        "password": "wrongpassword"

    }

)

print_result(
    "TEST 3 - Invalid Credentials",
    response
)


# LOGIN AS ANALYST

response = requests.post(

    f"{BASE_URL}/login",

    json={

        "username": "analyst",

        "password": "Analyst123!"

    }

)

analyst_token = response.json()["access_token"]


# TEST 4: ANALYST ACCESSING ADMIN ENDPOINT

response = requests.get(

    f"{BASE_URL}/admin/customers",

    headers={

        "Authorization":
        f"Bearer {analyst_token}"

    }

)

print_result(

    "TEST 4 - Analyst Accessing Admin Endpoint",

    response

)


# LOGIN AS ADMIN

response = requests.post(

    f"{BASE_URL}/login",

    json={

        "username": "admin",

        "password": "Admin123!"

    }

)

admin_token = response.json()["access_token"]


# ==================================================
# TEST 5: ADMIN ACCESS
# ==================================================

response = requests.get(

    f"{BASE_URL}/admin/customers",

    headers={

        "Authorization":
        f"Bearer {admin_token}"

    }

)

print_result(

    "TEST 5 - Authorized Admin Access",

    response

)


# ==================================================
# TEST 6: RATE LIMITING
# ==================================================

print("\n" + "=" * 60)

print("TEST 6 - Rate Limiting")

print("=" * 60)


for i in range(7):

    response = requests.post(

        f"{BASE_URL}/login",

        json={

            "username": "admin",

            "password": "wrongpassword"

        }

    )

    print(

        f"Attempt {i + 1}: "

        f"Status Code = "

        f"{response.status_code}"

    )
# Secure REST API

## Secure REST API for Big Data Access Control

A Flask-based REST API designed to demonstrate secure access to a large customer dataset using authentication, authorization, password hashing, rate limiting, logging, and security testing.

**Course:** DSA4030 – Big Data Security
**Project:** Group 7
**Bradley ochola:** 
**mitchell moraa** 
---

## 1. Project Overview

This project implements a secure REST API for controlled access to a customer dataset containing **100,000 records**.

The API demonstrates how security controls can be applied when exposing customer data through RESTful services. The implementation focuses on:

* User authentication
* JWT-based access tokens
* Password hashing using Bcrypt
* Role-Based Access Control (RBAC)
* API rate limiting
* Security logging
* Protected customer endpoints
* Security testing using Postman
* Vulnerability assessment using OWASP ZAP

The project is intended as an academic demonstration of REST API security and is designed for local development and testing.

---

# 2. Project Objectives

The project aims to:

1. Develop a functional REST API using Flask.
2. Generate and store a large customer dataset containing 100,000 records.
3. Implement secure user authentication.
4. Protect passwords using Bcrypt hashing.
5. Implement JWT-based authentication.
6. Implement Role-Based Access Control.
7. Prevent unauthorized access to protected endpoints.
8. Apply rate limiting to reduce brute-force login attempts.
9. Record security-related activities using application logging.
10. Test the API against common security scenarios using Postman.
11. Assess the API using OWASP ZAP.
12. Identify security weaknesses and recommend improvements.

---

# 3. System Architecture

```text
                         ┌─────────────────────┐
                         │       POSTMAN       │
                         │    API Client/Test  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FLASK API     │
                         │       app.py        │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │ Authentication│     │ Authorization │     │ Rate Limiting │
      │    auth.py    │     │ customers.py │     │ Flask-Limiter │
      │ JWT + Bcrypt  │     │     RBAC      │     └───────────────┘
      └───────┬───────┘     └───────┬───────┘
              │                     │
              └──────────────┬──────┘
                             ▼
                    ┌──────────────────┐
                    │    SQLAlchemy    │
                    │     models.py    │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │   SQLite Database│
                    │ 100,000 Records  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   logs/api.log   │
                    └──────────────────┘

                    ┌──────────────────┐
                    │    OWASP ZAP     │
                    │ Security Testing │
                    └──────────────────┘
```

---

# 4. Technologies Used

| Technology         | Purpose                  |
| ------------------ | ------------------------ |
| Python             | Application development  |
| Flask              | REST API framework       |
| Flask-SQLAlchemy   | Database ORM             |
| SQLite             | Local database           |
| Flask-JWT-Extended | JWT authentication       |
| Flask-Bcrypt       | Password hashing         |
| Flask-Limiter      | Rate limiting            |
| Faker              | Customer data generation |
| Postman            | API and security testing |
| OWASP ZAP          | Vulnerability assessment |
| Git/GitHub         | Version control          |

---

# 5. Project Structure

```text
DSA4030secureapi/
│
├── app.py
├── database.py
├── models.py
├── extensions.py
├── securitytest.py
├── requirements.txt
├── README.md
│
├── routes/
│   ├── auth.py
│   └── customers.py
│
├── logs/
│   └── api.log
│
├── screenshots/
│
├── report/
│
└── presentation/
```

---

# 6. Main Components

## app.py

`app.py` is the main Flask application.

It:

* Creates the Flask application.
* Configures the database.
* Configures JWT.
* Initializes Bcrypt.
* Initializes rate limiting.
* Configures application logging.
* Registers API blueprints.
* Starts the development server.

The API runs locally on:

```text
http://127.0.0.1:5000
```

---

## extensions.py

This file creates the reusable Flask extensions:

```text
SQLAlchemy
JWTManager
Bcrypt
Flask-Limiter
```

Keeping these extensions separate helps prevent circular imports between the application and route modules.

---

## models.py

`models.py` defines the database models.

### User

The User table contains:

```text
id
username
password_hash
role
```

Three roles are used:

```text
admin
analyst
customer
```

### Customer

The Customer table contains:

```text
id
customer_id
name
email
country
purchase_amount
```

---

## database.py

`database.py` initializes the database and generates the test dataset.

It creates:

* Three system users
* 100,000 customer records

Customer information is generated using the Faker library.

Example customer identifier:

```text
CUST-000001
```

The database generation process uses batches of 5,000 records to reduce the memory required during insertion.

Successful execution produces:

```text
SUCCESS: 100,000 customer records created.
```

---

# 7. Authentication

Authentication is implemented in:

```text
routes/auth.py
```

The API provides:

```text
POST /login
```

A user provides a username and password.

Example:

```json
{
    "username": "admin",
    "password": "AdminPassword123!"
}
```

The API:

1. Receives the credentials.
2. Searches for the user.
3. Retrieves the stored password hash.
4. Verifies the password using Bcrypt.
5. Generates a JWT access token.
6. Returns the token to the client.

Successful authentication returns:

```text
200 OK
```

with an access token.

---

# 8. Password Security

Passwords are not stored as plaintext.

Bcrypt is used to generate password hashes:

```python
bcrypt.generate_password_hash(password)
```

During authentication, the supplied password is compared against the stored hash:

```python
bcrypt.check_password_hash(
    user.password_hash,
    password
)
```

This protects the original password from being directly stored in the database.

---

# 9. JWT Authentication

After successful authentication, the server generates a JSON Web Token.

The token contains information such as:

```text
username
role
user identity
```

Protected requests must include:

```text
Authorization: Bearer <JWT>
```

Requests without a valid JWT are rejected.

Example:

```text
GET /customers
```

without authentication:

```json
{
    "msg": "Missing Authorization Header"
}
```

---

# 10. Role-Based Access Control

Role-Based Access Control is implemented in:

```text
routes/customers.py
```

The API currently uses three roles:

| Role     | Customer Data | Admin Endpoint |
| -------- | ------------- | -------------- |
| Admin    | Allowed       | Allowed        |
| Analyst  | Allowed       | Denied         |
| Customer | Denied        | Denied         |

The role is retrieved from the JWT claims.

The application then checks whether the user's role is allowed to access the requested endpoint.

---

# 11. API Endpoints

## Home

```http
GET /
```

Returns an API status message.

---

## Health Check

```http
GET /health
```

Returns:

```json
{
    "status": "healthy"
}
```

---

## Login

```http
POST /login
```

Authenticates a user and returns a JWT.

---

## Customer Records

```http
GET /customers
```

Requires:

```text
JWT
```

Allowed roles:

```text
admin
analyst
```

The endpoint currently returns up to 100 customer records per request.

---

## Admin Endpoint

```http
GET /admin/customers
```

Requires:

```text
JWT
```

Required role:

```text
admin
```

An analyst attempting to access this endpoint receives:

```text
403 Forbidden
```

---

# 12. Rate Limiting

The login endpoint is protected using Flask-Limiter.

The current configuration limits login requests to:

```text
5 requests per minute
```

This is designed to reduce the effectiveness of repeated brute-force authentication attempts.

After the configured limit is exceeded, the client should receive a rate-limit response such as:

```text
429 Too Many Requests
```

---

# 13. Security Logging

Application activity is recorded in:

```text
logs/api.log
```

The application records events including:

* Successful logins
* Failed login attempts
* Unauthorized access attempts
* Customer data access
* Administrative endpoint access

Example:

```text
Successful login: user=admin, role=admin
```

Example:

```text
Failed login attempt for username: admin
```

Example:

```text
Unauthorized access attempt:
user=analyst
role=analyst
required_roles=['admin']
```

These logs provide evidence of security-related activity during testing.

---

# 14. Security Testing

The API is tested using Postman.

The security assessment includes the following scenarios:

### Test 1 — Missing Authentication

Attempt to access:

```http
GET /customers
```

without an Authorization header.

Expected:

```text
401 Unauthorized
```

---

### Test 2 — Invalid JWT

Send an invalid token:

```text
Authorization: Bearer invalid-token
```

Expected:

```text
401 Unauthorized
```

---

### Test 3 — Invalid Credentials

Attempt to log in using an incorrect password.

Expected:

```text
401 Unauthorized
```

---

### Test 4 — Role-Based Authorization

Authenticate as an analyst and request:

```http
GET /admin/customers
```

Expected:

```text
403 Forbidden
```

This demonstrates that authentication alone does not provide administrator privileges.

---

### Test 5 — Brute-Force Protection

Send repeated login requests.

The login endpoint is configured for:

```text
5 requests per minute
```

Expected after exceeding the limit:

```text
429 Too Many Requests
```

---

### Test 6 — OWASP ZAP Assessment

OWASP ZAP is used to scan the API for common security weaknesses.

The results are documented in the project report.

---

# 15. Postman Demonstration

The recommended demonstration sequence is:

```text
1. Start Flask
        ↓
2. Check /health
        ↓
3. Login as admin
        ↓
4. Copy JWT
        ↓
5. Access /customers
        ↓
6. Login as analyst
        ↓
7. Attempt /admin/customers
        ↓
8. Demonstrate 403
        ↓
9. Test missing JWT
        ↓
10. Test invalid credentials
        ↓
11. Demonstrate rate limiting
        ↓
12. Run OWASP ZAP
```

This demonstrates both successful and unsuccessful security scenarios.

---

# 16. Installation

## Requirements

Recommended:

```text
Python 3.10+
pip
Git
Postman
OWASP ZAP
```

---

## Clone the repository

```bash
git clone https://github.com/bradzz13/DSA4030secureapi.git
```

Enter the project directory:

```bash
cd DSA4030secureapi
```

---

## Create a virtual environment

Mac/Linux:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 17. Database Setup

Run:

```bash
python database.py
```

This creates the database tables and generates the 100,000 customer records.

The terminal should eventually display:

```text
SUCCESS: 100,000 customer records created.
```

### Important

`database.py` should normally be used to initialize a new database rather than repeatedly run against an existing database because the usernames and customer IDs are unique.

---

# 18. Start the API

Run:

```bash
python app.py
```

The server should start at:

```text
http://127.0.0.1:5000
```

Test the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

Expected:

```json
{
    "status": "healthy"
}
```

---

# 19. Example Authentication Using cURL

Login:

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"AdminPassword123!"}'
```

The response contains:

```json
{
    "message": "Login successful",
    "access_token": "JWT_TOKEN",
    "user": {
        "role": "admin",
        "username": "admin"
    }
}
```

Use the returned token:

```bash
curl http://127.0.0.1:5000/customers \
-H "Authorization: Bearer JWT_TOKEN"
```

---

# 20. Security Considerations

This implementation is an academic/local prototype and should not be deployed directly to production.

The current development implementation includes areas requiring further hardening, including:

* JWT secret management
* HTTPS/TLS
* Flask debug mode
* Production database configuration
* Security headers
* Input validation
* Production-grade rate-limit storage

For production deployment, secrets should be stored using environment variables or a dedicated secrets-management system.

---

# 21. Recommended Production Improvements

Future versions should consider:

### Database

Replace SQLite with a production database such as PostgreSQL.

### HTTPS

Deploy the API behind HTTPS/TLS.

### Secret Management

Store JWT secrets outside the source code.

### Authentication

Add:

* Multi-factor authentication
* Refresh tokens
* Account lockout policies

### Rate Limiting

Use Redis or another persistent backend for distributed rate limiting.

### Monitoring

Forward application logs to a centralized logging or SIEM platform.

### Infrastructure

Deploy behind:

* API Gateway
* Reverse Proxy
* Web Application Firewall

---

# 22. Project Evidence

The repository can contain supporting evidence in:

```text
screenshots/
```

Recommended evidence includes:

* Successful login
* Invalid login
* Missing JWT
* Invalid JWT
* Analyst attempting admin access
* Successful admin access
* Rate-limit response
* 100,000-record database creation
* OWASP ZAP results

---

# 23. Documentation

The repository may also contain:

```text
report/
```

for the full academic project report and:

```text
presentation/
```

for the Group 7 presentation.

The README provides technical documentation, while the project report provides the detailed academic analysis, methodology, testing results, discussion and conclusions.

---

# 24. Academic Project

This repository was developed as part of the DSA4030 Big Data Security project.

The project demonstrates the application of cybersecurity principles to a REST API providing controlled access to a large customer dataset.

**Group 7**

---

## Author

**Brad Ochola**

GitHub:

https://github.com/bradzz13

Repository:

https://github.com/bradzz13/DSA4030secureapi

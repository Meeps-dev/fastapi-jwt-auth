🔐 Full JWT Authentication System (FastAPI)

A production-grade authentication system built with FastAPI that demonstrates real-world security patterns including JWT authentication, refresh token rotation, role-based access control (RBAC), and server-side token revocation.

This project focuses on how authentication should be designed, not just how to make it work.

🎯 Project Goals

This project was built to demonstrate:

Strong understanding of authentication vs authorization

Secure handling of JWT access and refresh tokens

Refresh token rotation to prevent token reuse attacks

Role-based access control (user vs admin)

Clean backend architecture and separation of concerns

Defensive API design with proper error handling

Automated testing of auth flows

🧠 Key Concepts Implemented
Authentication

User registration with hashed passwords

Login with credential verification

Stateless access tokens (JWT)

Authorization

Dependency-based route protection

Role-based access control (RBAC)

Admin-only endpoints

Token Strategy

Access tokens: short-lived, used on every request

Refresh tokens: long-lived, stored server-side

Refresh token rotation: every refresh invalidates the previous token

Reuse detection: reused refresh tokens are rejected

Security Best Practices

Password hashing using bcrypt

JWT signing with a secret key

Token expiration enforcement

Server-side refresh token revocation

Environment-based configuration (.env)

🏗️ Tech Stack

FastAPI

SQLAlchemy

SQLite (local development)

python-jose (JWT handling)

passlib (bcrypt) (password hashing)

pytest (automated testing)

📂 Project Structure
jwt-auth-system/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── core/
│ │ ├── security.py
│ │ └── config.py
│ ├── auth/
│ │ ├── jwt.py
│ │ ├── dependencies.py
│ │ └── routes.py
│ ├── users/
│ │ └── routes.py
│ └── admin/
│ └── routes.py
│
├── tests/
│ ├── conftest.py
│ ├── test_auth.py
│ └── test_protected_routes.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

🔐 Authentication Flow


1️⃣ Register
POST /auth/register

Creates a new user

Password is hashed before storage

Duplicate emails are rejected

2️⃣ Login
POST /auth/login

Returns:

Access token (short-lived)

Refresh token (long-lived)

3️⃣ Access Protected Routes
GET /users/me

Requires:

Authorization: Bearer <access_token>

4️⃣ Refresh Token Rotation
POST /auth/refresh

Flow:

Client sends refresh token

Server validates token

Old refresh token is revoked

New access + refresh tokens are issued

Reusing an old refresh token results in 401 Unauthorized.

5️⃣ Logout
POST /auth/logout

Refresh token is revoked server-side

Token reuse is prevented

🛡️ Role-Based Access Control (RBAC)
Roles

user

admin

Admin-only Endpoint
GET /admin/stats

Rules:

Valid access token required

User must have admin role

Non-admin users receive 403 Forbidden

🧪 Testing

This project includes automated tests for:

User registration

Login success and failure

Accessing protected routes without a token

Accessing protected routes with a token

Refresh token rotation and reuse detection

Admin-only route enforcement

Run tests with:

pytest -v

Each test runs against a fresh database state to ensure isolation and reliability.

⚙️ Setup & Run Locally

1️⃣ Clone the Repository
git clone <your-repo-url>
cd jwt-auth-system

2️⃣ Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create .env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

5️⃣ Run the Server
uvicorn app.main:app --reload

Visit:
👉 http://127.0.0.1:8000/docs

🚀 Why This Project Matters

This is not a demo project.

It demonstrates:

Real-world auth architecture

Awareness of common security pitfalls

Token lifecycle management

Defensive backend design

Test-driven confidence

This system can be extended to production with:

PostgreSQL

Redis-backed token storage

Rate limiting

Email verification


👨‍💻 Author

Jonathan Ayomipo
Backend-focused Python developer
FastAPI • Authentication • Security Fundamentals


# E-commerce Backend System using FastAPI

## Project Overview

This project is a secure, modular and fully functional E-commerce Backend built with **FastAPI** and **SQLAlchemy ORM**.

### Key Features
- User Authentication (Signup, Signin, Forgot Password, Reset Password)
- JWT-based Authentication with Access & Refresh Tokens
- Role-Based Access Control (Admin/User)
- Admin Product Management (CRUD with Pagination)
- Public Product Browsing & Search
- Cart Management (Add, Update, Delete, View Cart)
- Dummy Checkout & Order History
- Password Reset via Email (Gmail SMTP)
- SQLite3 Database for Development
- Pydantic Data Validation & Schema Management
- Postman Collection & Environment File included

---

## Technology Stack

- **Backend Framework:** FastAPI
- **ORM:** SQLAlchemy
- **DB:** SQLite (for development)
- **Auth:** OAuth2 + JWT (PyJWT)
- **Email:** smtplib (Gmail SMTP)
- **Password Hashing:** bcrypt + passlib
- **Validation:** Pydantic

---

## Setup Instructions

### 1. Clone Repository
```
git clone <repo_url>
cd <repo_folder>
```

### 2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in root:
```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
EMAIL_PASSWORD=your_app_password_here
SENDER_EMAIL=your_email_here
```

### 5. Run the App
```
uvicorn app.main:app --reload
```

### 6. Open Swagger Docs
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Auth
- POST /auth/signup
- POST /auth/signin
- POST /auth/forgot-password
- POST /auth/reset-password

### Products (Admin)
- POST /admin/products
- GET /admin/products
- GET /admin/products/{id}
- PUT /admin/products/{id}
- DELETE /admin/products/{id}

### Products (Public)
- GET /products
- GET /products/search?keyword=mouse
- GET /products/{id}

### Cart (User)
- POST /cart
- GET /cart
- PUT /cart/{product_id}
- DELETE /cart/{product_id}

### Checkout (User)
- POST /checkout

### Orders (User)
- GET /orders
- GET /orders/{order_id}

---

---

## Testing
Manual testing done using **Postman** and **Swagger UI**.

---

## Security Notes
- JWT tokens stored in Authorization headers.
- Passwords hashed using **bcrypt**.
- Reset password tokens expire after 15 mins.

---

## Author
Adarsh Kumar | FastAPI E-commerce Project
# FastAPI E-commerce Backend

A fully functional RESTful backend API for an e-commerce platform built using **FastAPI**. This project includes secure user authentication, product browsing, admin CRUD operations, cart management, checkout, and order tracking.

## 🚀 Features

### 🔐 Authentication & Authorization
- Signup, Signin with JWT (Access & Refresh tokens)
- Forgot/Reset Password with secure token
- Role-based access control (Admin / User)

### 🛒 Product Management
- Admin-only CRUD for products
- Product listing with pagination, filters, and search
- Product detail view

### 🧺 Cart & Checkout
- Add/Remove/Update products in cart
- Dummy checkout and order creation
- Order history and detailed order view

## 🧱 Tech Stack

- **FastAPI**
- **SQLAlchemy** ORM
- **PostgreSQL** (or SQLite for development)
- **Pydantic** for data validation
- **JWT** for authentication
- **Alembic** for migrations (optional)
- **Uvicorn** for local development server

## 📁 Project Structure

```
app/
├── main.py
├── auth/
│   ├── routes.py
│   ├── models.py
│   ├── utils.py
├── products/
├── cart/
├── checkout/
├── orders/
├── core/
│   ├── config.py
│   ├── database.py
├── middlewares/
├── utils/
├── tests/
```

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fastapi-ecommerce-backend.git
   cd fastapi-ecommerce-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up `.env` file**
   Create a `.env` file in the root directory with:
   ```env
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///./ecom.db  # or your PostgreSQL URI
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API Docs**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## 🧪 Testing

- Manual testing via **Postman**
- Auth, Product, Cart, Checkout, and Order endpoints tested
- Postman collection included: `postman_collection.json`

## 🧬 Seed Data

Run the `seed.py` script to populate sample products:
```bash
python seed.py
```

## 📄 API Endpoints Overview

### 🔐 Auth
- `POST /auth/signup`
- `POST /auth/signin`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`

### 🛍 Products
- `GET /products`
- `GET /products/search`
- `GET /products/{id}`
- `POST /admin/products` *(Admin)*
- `PUT /admin/products/{id}` *(Admin)*
- `DELETE /admin/products/{id}` *(Admin)*

### 🛒 Cart
- `GET /cart`
- `POST /cart`
- `PUT /cart/{product_id}`
- `DELETE /cart/{product_id}`

### ✅ Checkout & Orders
- `POST /checkout`
- `GET /orders`
- `GET /orders/{order_id}`

## 🔐 Security

- Passwords hashed using `bcrypt`
- JWT-based authentication
- Secure password reset with time-limited tokens
- RBAC enforced on protected endpoints


**Built by [Adarsh Kumar](https://github.com/your-username) — June 2025**
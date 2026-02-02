# Food Ordering & Delivery Backend System

A modern, secure, and scalable RESTful API backend for a food ordering and delivery platform built with **FastAPI**, **PostgreSQL**, **JWT Authentication**, and **SQLAlchemy ORM**.

Users can register, browse restaurants and menus, place orders, track deliveries, while restaurant owners can manage their menu items and update order statuses. The system handles authentication, authorization, cart management, and basic order processing.

## ✨ Features

- **User & Restaurant Authentication** using JWT (OAuth2 Password Flow)
- Role-based access: Customer, Restaurant Owner (Admin optional)
- Register / Login / Profile management
- Browse restaurants, menus, search & filters
- Add items to cart, update/remove items
- Place orders with address & payment info (mock gateway support)
- Order tracking & status updates (accepted, preparing, out for delivery, delivered)
- Restaurant dashboard: Manage menu (CRUD), view & update incoming orders
- Secure password hashing (bcrypt)
- Input validation using Pydantic
- Interactive API documentation (Swagger UI & ReDoc)
- Async support for better performance

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL + SQLAlchemy (ORM) + Alembic (migrations)
- **Authentication**: JWT (PyJWT + fastapi-users or custom)
- **Validation & Serialization**: Pydantic
- **Password Hashing**: passlib[bcrypt]
- **CORS**: Enabled for frontend integration
- **Testing**: pytest (recommended)
- **ASGI Server**: Uvicorn

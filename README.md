# E-Library Management System

Backend system for an E-Library built using Django REST Framework and PostgreSQL.

## Features

- JWT Authentication
- Custom User Model
- Role Based Access Control
- Member / Librarian / Admin
- Book CRUD
- Authors and Categories
- Book Search
- Filtering
- Pagination
- Borrowing and Returning
- Due Dates
- Fine Calculation
- Borrowing History
- Overdue Books
- Reviews and Ratings
- Favourite Books
- Book Reservations
- Notifications
- AI Powered Book Summary
- Dashboard
- Swagger API Documentation

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT
- OpenAI API

## API Documentation

`/api/docs/`

## Authentication

`POST /api/auth/token/`

`POST /api/auth/token/refresh/`

## AI Summary

`POST /api/ai/books/<book_id>/summary/`

## Dashboard

`GET /api/dashboard/`

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
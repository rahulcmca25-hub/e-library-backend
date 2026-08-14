# 📚 E-Library Management System

> A modular, RESTful backend for a digital library built with **Django, Django REST Framework and PostgreSQL**, with JWT authentication, role-based authorization, book inventory management, borrowing workflows, reviews, an admin dashboard, and AI-powered book summaries using OpenAI.

---

## 🚀 Project Overview

The **E-Library Management System** is a backend-focused library platform designed around real-world library workflows rather than only basic CRUD operations.

The system provides APIs for:

- User authentication and authorization
- Role-based access control
- Book management
- Author and category management
- Book search, filtering, pagination and sorting
- Book inventory/copy tracking
- Borrowing and returning books
- Borrowing history
- Overdue tracking
- Automatic fine calculation
- Reviews and ratings
- Admin/Librarian dashboard statistics
- AI-powered book summaries
- PostgreSQL database integration
- Swagger/OpenAPI API documentation

The backend is divided into domain-specific Django applications so that each business area remains modular and maintainable.

---

# ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 JWT Authentication | Access/refresh token based authentication |
| 👤 Custom User Model | Email-based authentication with a custom user model |
| 🛡️ Role-Based Access | `MEMBER`, `LIBRARIAN`, and `ADMIN` roles |
| 📚 Book CRUD | Create, read, update, partially update and delete books |
| 🔎 Search | Search books using title, ISBN, author and category |
| 🎯 Filtering | Filter by author, category and availability |
| 📄 Pagination | Paginated book listing |
| ↕️ Sorting | Sort by title, published date and creation date |
| 📦 Inventory Tracking | Track total and available copies |
| 📖 Borrowing | Borrow books with business-rule validation |
| ⏱️ Borrow Duration | 14-day borrowing period |
| 🚫 Borrow Limit | Maximum 3 active borrowings per user |
| 🔁 Duplicate Protection | Prevent duplicate active borrowing of the same book |
| 🔄 Return System | Return books and restore available copies |
| ⚠️ Overdue Detection | Detect books whose due date has passed |
| 💰 Fine Calculation | ₹5 per overdue day |
| 📜 Borrowing History | View a user's borrowing records |
| ⭐ Reviews | Create and retrieve book reviews |
| 🔒 Review Uniqueness | One review per user per book |
| 📊 Dashboard | Library statistics for administrators/librarians |
| 🤖 AI Summary | Generate book summaries using OpenAI `gpt-5-mini` |
| 🗄️ PostgreSQL | PostgreSQL database integration |
| 📘 Swagger/OpenAPI | Interactive API documentation |
| ⚙️ Environment Config | Secrets/configuration through `.env` |

---

# 🏗️ Architecture

```text
                         ┌───────────────────────┐
                         │       Client          │
                         │  Frontend / Postman   │
                         │      / Swagger        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     Django REST API   │
                         └───────────┬───────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
   ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
   │ Authentication│          │    Books     │          │  Borrowings  │
   │    & RBAC    │          │              │          │              │
   └──────────────┘          └──────────────┘          └──────────────┘
          │                          │                          │
          └──────────────────────────┼──────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
              ┌──────────┐    ┌───────────┐    ┌────────────┐
              │ Reviews  │    │ Dashboard │    │ AI Summary │
              └──────────┘    └───────────┘    └─────┬──────┘
                                                     │
                                                     ▼
                                               ┌───────────┐
                                               │  OpenAI   │
                                               │ gpt-5-mini│
                                               └───────────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │ Django ORM  │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │ PostgreSQL  │
                              └─────────────┘
```

---

# 🧩 Django Application Architecture

The project is separated into domain-specific applications:

```text
e-library/
│
├── ai/                  # AI book-summary functionality
├── books/               # Books, authors, categories and book APIs
├── borrowings/          # Borrow/return/history/overdue/fine logic
├── dashboard/           # Admin/Librarian dashboard statistics
├── favourites/          # Favourites module
├── notifications/       # Notification module
├── reservations/        # Reservation module
├── reviews/             # Book reviews
├── users/               # Custom user model and roles
│
├── config/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend Framework | Django |
| REST API | Django REST Framework |
| Authentication | JWT / `djangorestframework-simplejwt` |
| Authorization | Custom DRF permission classes |
| Database | PostgreSQL |
| ORM | Django ORM |
| AI | OpenAI API |
| AI Model | `gpt-5-mini` |
| API Schema | OpenAPI 3 |
| API Documentation | drf-spectacular / Swagger UI |
| Configuration | `.env` environment variables |

---

# 👤 Custom User System

The project uses a custom user model instead of relying only on Django's default username-based user.

## Login identity

Users authenticate using their **email address**.

```text
email = unique
username = not used
USERNAME_FIELD = email
```

This makes email the primary authentication identifier.

---

# 🛡️ Role-Based Access Control

The system defines three roles:

```text
MEMBER
LIBRARIAN
ADMIN
```

## Role overview

| Capability | MEMBER | LIBRARIAN | ADMIN |
|---|:---:|:---:|:---:|
| View books | ✅ | ✅ | ✅ |
| Search/filter books | ✅ | ✅ | ✅ |
| Create books | ❌ | ✅ | ✅ |
| Update books | ❌ | ✅ | ✅ |
| Delete books | ❌ | ❌ | ✅ |
| Access dashboard | ❌ | ✅ | ✅ |

Custom permission classes are used to enforce role-specific operations.

This prevents a normal library member from performing administrative book-management operations.

---

# 🔐 JWT Authentication

The API uses JWT authentication with access and refresh tokens.

## Authentication endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/auth/token/` | Obtain access and refresh tokens |
| `POST` | `/api/auth/token/refresh/` | Refresh an access token |

## Authentication flow

```text
User Credentials
      │
      ▼
POST /api/auth/token/
      │
      ▼
┌───────────────────────┐
│ Access Token          │
│ Refresh Token         │
└───────────┬───────────┘
            │
            ▼
Authorization: Bearer <access-token>
            │
            ▼
Protected API Endpoint
            │
            ▼
JWT Validation
            │
            ▼
API Response
```

## Example

```http
POST /api/auth/token/
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

Example response:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Use the access token:

```http
Authorization: Bearer <access-token>
```

---

# 📚 Book Management

Books are the central entity of the library system.

The book domain includes:

- Book
- Author
- Category
- Inventory/copy tracking

## Book fields

The Book model contains:

| Field | Purpose |
|---|---|
| `title` | Book title |
| `isbn` | ISBN identifier |
| `description` | Book description |
| `author` | Associated author |
| `category` | Associated category |
| `total_copies` | Total number of copies |
| `available_copies` | Currently available copies |
| `published_date` | Publication date |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

---

# 📖 Book CRUD API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/` | List books |
| `POST` | `/api/` | Create a book |
| `GET` | `/api/{id}/` | Retrieve a book |
| `PUT` | `/api/{id}/` | Replace a book |
| `PATCH` | `/api/{id}/` | Partially update a book |
| `DELETE` | `/api/{id}/` | Delete a book |

Book creation/update/deletion is protected through role-based permissions.

---

# 🔎 Search, Filtering, Pagination & Sorting

The book listing API supports more than simple retrieval.

## Search

Search can be performed using:

```http
GET /api/?search=python
```

The implemented search covers book information including:

- title
- ISBN
- author
- category

## Author filter

```http
GET /api/?author=<author-id>
```

## Category filter

```http
GET /api/?category=<category-id>
```

## Availability filter

```http
GET /api/?available=true
```

## Pagination

Example:

```http
GET /api/?page=1&limit=10
```

## Sorting

Examples:

```http
GET /api/?ordering=title
```

```http
GET /api/?ordering=-title
```

```http
GET /api/?ordering=published_date
```

```http
GET /api/?ordering=-created_at
```

Supported sorting includes book title, publication date and creation date.

---

# 📦 Book Inventory

Each book maintains:

```text
total_copies
available_copies
```

This allows the system to track actual inventory rather than using only a boolean `is_borrowed` flag.

### Borrow

```text
available_copies -= 1
```

### Return

```text
available_copies += 1
```

This inventory relationship is integrated into the borrowing workflow.

---

# 📖 Borrowing System

Borrowing is implemented as a dedicated business domain.

Each borrowing is represented by a `BorrowRecord`.

## BorrowRecord fields

| Field | Purpose |
|---|---|
| `user` | User who borrowed the book |
| `book` | Borrowed book |
| `borrowed_at` | Borrowing timestamp |
| `due_date` | Due date/time |
| `returned_at` | Return timestamp |
| `status` | Borrowing state |
| `fine` | Fine amount |
| `created_at` | Record creation time |
| `updated_at` | Last update time |

## Status values

```text
BORROWED
RETURNED
OVERDUE
```

---

# ⏱️ Borrowing Rules

The borrowing system includes real business constraints.

### Maximum active borrowings

```text
3 books per user
```

A user cannot have more than **3 active borrowings**.

### Borrow duration

```text
14 days
```

The default borrowing period is 14 days.

### Availability validation

A book can only be borrowed when:

```text
available_copies > 0
```

### Duplicate active borrowing

A user cannot borrow the same book again while they already have an active borrowing for it.

---

# 🔄 Borrowing Workflow

```text
                 Authenticated User
                         │
                         ▼
                 Borrow Request
                         │
                         ▼
               ┌─────────────────┐
               │ Validate User   │
               │ & Book          │
               └────────┬────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
     Availability   Max 3 Limit   Duplicate Check
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                 Create BorrowRecord
                        │
                        ▼
             available_copies -= 1
                        │
                        ▼
                  Borrowed Book
```

---

# 🔒 Transaction & Concurrency Safety

The borrowing and return operations use database transactions and row-level locking.

The implementation uses:

```python
transaction.atomic()
```

and:

```python
select_for_update()
```

This helps protect book availability from race conditions when multiple requests attempt to borrow or return copies concurrently.

Conceptually:

```text
Request A ──┐
            ├──> Database Row Lock ──> Safe Update
Request B ──┘
```

This is an important backend design decision because book inventory is shared mutable state.

---

# 🔁 Return Book

Endpoint:

```http
POST /api/borrowings/return/{id}/
```

The return workflow:

```text
Borrowed Book
     │
     ▼
Return Request
     │
     ▼
Check Borrowing
     │
     ▼
Calculate Overdue/Fine
     │
     ▼
Set returned_at
     │
     ▼
Set status = RETURNED
     │
     ▼
available_copies += 1
```

---

# ⚠️ Overdue Tracking

Endpoint:

```http
GET /api/borrowings/overdue/
```

A borrowing becomes overdue when its due date has passed while the borrowing is still active.

The model also exposes an `is_overdue` property based on:

```python
status == BORROWED
and timezone.now() > due_date
```

This provides a clear distinction between:

```text
BORROWED
    │
    │ due date passes
    ▼
OVERDUE condition
    │
    │ returned
    ▼
RETURNED
```

---

# 💰 Fine Calculation

The borrowing system uses:

```text
FINE_PER_DAY = ₹5.00
```

When a book is returned after its due date, overdue days are calculated and the fine is based on:

```text
Fine = Overdue Days × ₹5
```

Example:

| Overdue Days | Fine |
|---:|---:|
| 0 | ₹0 |
| 1 | ₹5 |
| 3 | ₹15 |
| 7 | ₹35 |
| 10 | ₹50 |

The fine is stored as a decimal value in the borrowing record.

---

# 📜 Borrowing History

Endpoint:

```http
GET /api/borrowings/history/
```

The history endpoint returns borrowing records belonging to the authenticated user.

A borrowing record can contain:

- Book
- Borrowed date
- Due date
- Return date
- Status
- Fine

The history is scoped to the current authenticated user.

---

# ⭐ Reviews

The project includes a dedicated reviews module.

## Review fields

| Field | Description |
|---|---|
| `user` | Reviewer |
| `book` | Reviewed book |
| `rating` | Book rating |
| `comment` | Review text |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/reviews/` | Retrieve reviews |
| `POST` | `/api/reviews/` | Create a review |

Reviews can be filtered by book.

Example:

```http
GET /api/reviews/?book=<book-id>
```

## Duplicate review protection

A user can have only one review for a particular book.

Conceptually:

```text
(User, Book)
     │
     ▼
Unique Review
```

This is enforced using a database-level uniqueness constraint.

---

# 📊 Dashboard

Endpoint:

```http
GET /api/dashboard/
```

The dashboard is intended for **LIBRARIAN and ADMIN** users.

Regular members do not have access to the administrative dashboard.

## Dashboard statistics

The dashboard provides statistics including:

| Metric | Description |
|---|---|
| `total_users` | Total registered users |
| `total_books` | Total books |
| `total_copies` | Total physical copies |
| `available_copies` | Currently available copies |
| `active_borrowings` | Active borrowing records |
| `returned_books` | Returned borrowing records |
| `overdue_books` | Overdue borrowing records |
| `total_fines` | Total fine amount |

This gives library staff a centralized view of the system.

---

# 🤖 AI-Powered Book Summary

AI summarization is one of the main features of the assignment.

## Endpoint

```http
POST /api/{id}/summary/
```

## AI provider

```text
OpenAI
Model: gpt-5-mini
```

The backend prepares book information including:

- Title
- Description
- Author
- Category

and sends the information to the AI model to generate a book summary.

---

## AI Workflow

```text
              Client
                │
                │ POST /api/{id}/summary/
                ▼
        ┌──────────────────┐
        │   Book Endpoint   │
        └────────┬─────────┘
                 │
                 ▼
          Retrieve Book
                 │
                 ▼
       Prepare Book Context
       ┌─────────┼─────────┐
       │         │         │
     Title  Description  Author
                 │
                 ▼
             Category
                 │
                 ▼
        ┌─────────────────┐
        │  OpenAI API     │
        │   gpt-5-mini    │
        └────────┬────────┘
                 │
                 ▼
        Generated Summary
                 │
                 ▼
            JSON Response
```

## Example request

```http
POST /api/1/summary/
Authorization: Bearer <access-token>
```

Example response:

```json
{
  "book_id": 1,
  "title": "Example Book",
  "summary": "Generated AI summary..."
}
```

The actual response is generated by the backend using the configured AI service.

---

# 🧩 Notifications

The repository contains a notifications module for user-specific notifications.

The notification implementation supports:

- Retrieving notifications
- Marking an individual notification as read
- User-specific notification access

The notification view scopes notification data to the authenticated user.

---

# 📌 Reservations

The repository also contains a reservations module designed for unavailable books.

The reservation logic supports:

- Checking whether a book exists
- Allowing reservation when a book is unavailable
- Preventing duplicate waiting reservations
- Creating reservation records

This module provides the foundation for a library reservation/waiting-list workflow.

---

# 💾 PostgreSQL Database

The application uses **PostgreSQL** as its database.

Database configuration is loaded from environment variables.

Typical configuration values include:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

The Django application connects using:

```text
django.db.backends.postgresql
```

Using PostgreSQL provides a production-oriented relational database for the application's users, books, borrowing records, reviews and other entities.

---

# 🔗 API Reference

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/token/` | Obtain JWT access and refresh tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |

## Books

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/` | List/search/filter books |
| POST | `/api/` | Create book |
| GET | `/api/{id}/` | Retrieve book |
| PUT | `/api/{id}/` | Replace book |
| PATCH | `/api/{id}/` | Partially update book |
| DELETE | `/api/{id}/` | Delete book |

## AI

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/{id}/summary/` | Generate AI book summary |

## Borrowings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/borrowings/borrow/` | Borrow a book |
| GET | `/api/borrowings/history/` | View borrowing history |
| GET | `/api/borrowings/overdue/` | View overdue borrowings |
| POST | `/api/borrowings/return/{id}/` | Return a book |

## Reviews

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/reviews/` | Retrieve reviews |
| POST | `/api/reviews/` | Create review |

## Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/` | Retrieve dashboard statistics |

---

# 🧪 Example End-to-End Workflow

A typical user journey can look like this:

```text
1. Login
   │
   ▼
2. Receive JWT
   │
   ▼
3. Search / Filter Books
   │
   ▼
4. View Book Details
   │
   ├───────────────────────┐
   ▼                       ▼
5. Borrow Book          AI Summary
   │                       │
   ▼                       ▼
6. Track Borrowing      OpenAI
   │                       │
   ▼                       ▼
7. Check History        Summary
   │
   ▼
8. Due Date
   │
   ├── On time ──────► Return
   │
   └── Overdue ──────► Fine Calculation
                           │
                           ▼
                         Return
                           │
                           ▼
                     available_copies += 1
```

---

# 🗃️ Core Data Relationships

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                ┌───────────────┼────────────────┐
                │               │                │
                ▼               ▼                ▼
          BorrowRecord       Review        Notification
                │               │
                │               │
                ▼               ▼
             Book ◄─────────────┘
              │
        ┌─────┴─────┐
        ▼           ▼
     Author      Category
```

### Borrowing relationship

```text
User 1 ───────── N BorrowRecord N ───────── 1 Book
```

This allows the system to maintain a complete borrowing history over time.

---

# 🔄 Borrowing Lifecycle

```text
              ┌─────────────┐
              │   BORROWED  │
              └──────┬──────┘
                     │
                     │ due date passed
                     ▼
              ┌─────────────┐
              │   OVERDUE   │
              └──────┬──────┘
                     │
                     │ return
                     ▼
              ┌─────────────┐
              │   RETURNED  │
              └─────────────┘
```

The overdue condition is evaluated from the borrowing status and due date, while the return workflow updates the record and inventory.

---

# 📘 Swagger / OpenAPI Documentation

Interactive API documentation is available through Swagger UI.

### Swagger

```text
http://127.0.0.1:8000/api/docs/
```

### OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

Swagger makes it easy to:

- Explore endpoints
- Inspect request/response schemas
- Test APIs
- Authorize using JWT
- Understand available operations

---

# ⚙️ Environment Configuration

The project uses environment variables for sensitive configuration.

The repository includes:

```text
.env.example
```

Create your local `.env` from the example:

```powershell
Copy-Item .env.example .env
```

Then configure the required values.

Typical configuration includes:

```text
DJANGO_SECRET_KEY
DEBUG
DATABASE_URL / PostgreSQL configuration
OPENAI_API_KEY
```

Use the exact variable names provided by the project's `.env.example`.

### Never commit

```text
.env
```

Real passwords, API keys, JWT tokens and secret keys should never be committed to the repository.

---

# 🚀 Local Setup

## 1. Clone

```bash
git clone https://github.com/rahulcmca25-hub/e-library-backend.git
cd e-library-backend
```

## 2. Create virtual environment

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment

```powershell
Copy-Item .env.example .env
```

Add your PostgreSQL and AI configuration.

## 5. Run migrations

```bash
python manage.py migrate
```

## 6. Create superuser

```bash
python manage.py createsuperuser
```

## 7. Start server

```bash
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

Swagger:

```text
http://127.0.0.1:8000/api/docs/
```

Schema:

```text
http://127.0.0.1:8000/api/schema/
```

---

# 🧪 Testing

Django tests can be executed using:

```bash
python manage.py test
```

The APIs were also manually exercised during development through the API documentation/testing workflow.

Important areas for API verification include:

- JWT authentication
- Book CRUD
- Search and filters
- Borrowing
- Borrowing limits
- Book availability
- Return flow
- Overdue detection
- Fine calculation
- Reviews
- Dashboard permissions
- AI summary

---

# 🛡️ Security

The project includes several security-oriented mechanisms.

### JWT authentication

Protected APIs require:

```http
Authorization: Bearer <access-token>
```

### Role-based permissions

Different user roles receive different capabilities.

### User-specific data access

Borrowing history and notifications are scoped to the authenticated user.

### Environment secrets

Sensitive values are kept in environment variables.

### Database transactions

Borrowing/return operations use atomic transactions and row-level locking to reduce concurrency problems around book inventory.

---

# 🧠 Important Backend Design Decisions

## 1. Domain separation

Each major business area is separated into its own Django application.

This improves:

- maintainability
- readability
- scalability
- separation of concerns

## 2. Custom user model

Email is used as the authentication identity instead of depending on Django's default username flow.

## 3. Role-based authorization

Library members, librarians and administrators have different responsibilities.

## 4. Inventory-aware borrowing

The system tracks actual copy counts instead of only using a borrowed/not-borrowed flag.

## 5. Transactional borrowing

`transaction.atomic()` and `select_for_update()` are used around inventory-sensitive operations.

## 6. Dedicated AI endpoint

AI summarization is exposed independently from normal CRUD operations.

## 7. PostgreSQL

PostgreSQL is used as the relational database for the application.

## 8. OpenAPI documentation

Swagger/OpenAPI makes the API easier to test and integrate with a frontend.

---

# 📈 Future Improvements

The following are natural next steps for evolving the project:

- Redis caching
- Celery/background jobs
- Automated overdue notifications
- Email notifications
- Reservation queue processing
- API rate limiting
- Advanced full-text search
- Recommendation engine
- AI-powered semantic search
- Docker containerization
- CI/CD pipeline
- Production deployment
- Expanded automated test coverage
- Centralized logging and monitoring
- More granular role/permission policies
- Audit logging

---

# 📊 Project Capability Map

```text
                       E-LIBRARY MANAGEMENT SYSTEM
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
          ▼                       ▼                        ▼
     AUTHENTICATION             BOOKS                  BORROWINGS
          │                       │                        │
      JWT + RBAC          CRUD + Search + Filters     Borrow
      3 Roles             Pagination + Sorting        Return
          │               Inventory Tracking           History
          │                                             Overdue
          │                                             Fine
          │
          ├─────────────────────────────────────────────────────┐
          │                                                     │
          ▼                                                     ▼
       REVIEWS                                              DASHBOARD
          │                                                     │
     Rating/Comment                                   Library Statistics
     One per user/book                                Admin/Librarian
          │
          └──────────────────────────┐
                                     ▼
                                AI SUMMARY
                                     │
                                     ▼
                              OpenAI gpt-5-mini
```

---

# 🎯 What This Project Demonstrates

This project demonstrates practical backend engineering concepts beyond simple CRUD:

- REST API development
- Django application architecture
- Django REST Framework
- JWT authentication
- Role-based authorization
- Custom user models
- PostgreSQL integration
- ORM-based database operations
- Business-rule validation
- Inventory management
- Transaction management
- Row-level locking
- Overdue/fine calculation
- API filtering and pagination
- Database constraints
- AI API integration
- Swagger/OpenAPI documentation
- Environment-based configuration

---

# 🔮 Production Architecture

A possible production evolution of the system:

```text
                         ┌───────────────────┐
                         │      Client       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Django REST     │
                         │       API         │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
       ┌───────────┐         ┌───────────┐         ┌───────────┐
       │PostgreSQL │         │   Redis   │         │  Celery   │
       └───────────┘         └───────────┘         └───────────┘
             │                     │                     │
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   ▼
                           ┌──────────────┐
                           │ AI / OpenAI  │
                           └──────────────┘
```

The current project already uses PostgreSQL and OpenAI; Redis/Celery and other infrastructure shown here represent possible production extensions.

---

# 📌 API Quick Reference

```text
AUTH
POST   /api/auth/token/
POST   /api/auth/token/refresh/

BOOKS
GET    /api/
POST   /api/
GET    /api/{id}/
PUT    /api/{id}/
PATCH  /api/{id}/
DELETE /api/{id}/

AI
POST   /api/{id}/summary/

BORROWINGS
POST   /api/borrowings/borrow/
GET    /api/borrowings/history/
GET    /api/borrowings/overdue/
POST   /api/borrowings/return/{id}/

REVIEWS
GET    /api/reviews/
POST   /api/reviews/

DASHBOARD
GET    /api/dashboard/
```

---

# 👨‍💻 Author

**Rahul Chadar**

GitHub:  
https://github.com/rahulcmca25-hub

Repository:  
https://github.com/rahulcmca25-hub/e-library-backend

---

# ⭐ Final Note

This project was built as an end-to-end backend assignment with an intentionally open-ended scope. The implementation focuses on realistic library workflows, secure API access, business-rule validation, inventory consistency, AI integration, and maintainable Django architecture.

The combination of **JWT + RBAC + PostgreSQL + transactional borrowing + inventory management + reviews + dashboard analytics + AI-powered summaries** makes the project substantially more than a basic CRUD backend.

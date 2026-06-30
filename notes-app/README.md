# Notes API

A REST API built with FastAPI that lets users register, log in and manage their personal notes.

My first backend project. Built it to understand how APIs, authentication, databases and user authorization work together.

This started as a simple CRUD project but I gradually expanded it to learn how authentication and authorization work in backend applications. I first implemented JWT manually to understand how it works internally, and then switched to PyJWT for the final implementation.

## Features

- User registration
- User login
- Password hashing using Argon2
- JWT authentication
- OAuth2 Password Bearer
- Protected routes
- CRUD operations for notes
- Basic Pagination (Search and filters)
- Users can only access their own notes
- Request validation using Pydantic

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyJWT
- pwdlib (Argon2)
- Uvicorn

## Running the project

Clone the repository

```bash
git clone <repo-url>
cd notes-app
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
SECRET_KEY=your_secret_key
```

Run the server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint          |
|--------|-------------------|
| POST   | `/register`       |
| POST   | `/login`          |
| GET    | `/notes`          |
| GET    | `/notes/{note_id}`|
| POST   | `/notes`          |
| PUT    | `/notes/{note_id}`|
| DELETE | `/notes/{note_id}`|

> All note endpoints require authentication.

## What I learned

Some of the things I learned while building this project:

- How basic pagination works.
- How JWTs are created and verified.
- The difference between authentication and authorization.
- How OAuth2 Password Bearer works in FastAPI.
- Password hashing and verification using Argon2.
- SQLAlchemy relationships and foreign keys.
- Using FastAPI dependencies for protected routes.
- Designing custom exceptions instead of exposing database errors.
- Making sure users can only access their own resources.

## Possible improvements

There are still a few things I'd like to add in the future:

- Refresh tokens
- PostgreSQL
- Alembic migrations
- Unit tests
- Docker support

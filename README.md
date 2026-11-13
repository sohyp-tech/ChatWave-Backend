# ChatWave Backend

A FastAPI-powered backend for the ChatWave app — built for user accounts, social posts, chat data, and media uploads. The project focuses on a clean API layer, SQLAlchemy models, and a simple structure that can grow with the frontend.

## Overview

ChatWave Backend is the server-side foundation of a social communication platform. It handles:

- user registration and auth flow
- profile management
- media uploads for avatar images
- post creation data models
- chat/message storage foundation
- API endpoints for frontend integration

The backend is designed to work with MySQL and is wired with SQLAlchemy for ORM-based database interaction.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PyMySQL
- MySQL
- Passlib
- Python-dotenv
- Static file serving for uploads

## Project Structure

```text
ChatWave-Backend/
├── .env.example
├── .gitignore
├── README.md
├── backend/
│   └── app/
│       ├── main.py
│       ├── logger.py
│       ├── core/
│       │   ├── security.py
│       │   └── database/
│       │       ├── database.py
│       │       ├── models/
│       │       │   ├── users.py
│       │       │   ├── posts.py
│       │       │   └── chats.py
│       │       └── schema/
│       │           ├── users.py
│       │           ├── posts.py
│       │           └── chats.py
│       └── routers/
│           ├── users.py
│           ├── posts.py
│           └── chats.py
└── uploads/
```

## Core Architecture

### 1. App entry point
The main FastAPI app is created in `backend/app/main.py`.

It does a few important things:

- initializes the FastAPI application
- enables CORS for frontend communication
- mounts the `uploads` folder so user images can be served
- includes the user, post, and chat routers
- creates database tables automatically at startup

### 2. Database layer
The database connection is configured in `backend/app/core/database/database.py`.

It:

- loads environment variables from `.env`
- builds a MySQL connection URL
- creates the SQLAlchemy engine
- provides a `get_db()` dependency for routes

This keeps the app modular and ensures each endpoint can access the database cleanly.

### 3. Models
The backend uses SQLAlchemy ORM models located in `backend/app/core/database/models/`:

- `User` → stores user profile data, phone number, token, photo URL
- `Post` → stores post content and creator relationship
- `Chat` → stores message metadata such as room, sender, receiver, and content

These models form the foundation for the app's social and messaging features.

### 4. Routers
The API layer is split by feature in `backend/app/routers/`:

- `users.py` handles signup, login, profile retrieval, update, and deletion
- `posts.py` is prepared for post operations
- `chats.py` is prepared for chat logic

### 5. Security
The project uses `passlib` and a hashed token system in `backend/app/core/security.py`.

This gives the app a simple security layer for:

- password-like hashing support
- secure token generation
- token validation for authenticated actions

## Features

### User system
The backend supports:

- account signup with photo upload
- login by name + phone number
- cookie-based user sessions using a token
- fetching user information by name and phone number
- profile updates and account deletion

### Media handling
The app saves uploaded profile pictures into the local `uploads/` folder and exposes them through the `/uploads` static route.

This lets the frontend display user avatars without complicated storage setup.

### Social and chat foundations
The models and routes are designed around:

- user-generated posts
- user-to-user communication
- chat rooms and conversations
- future expansion into full real-time messaging

## Environment Setup

Create a local `.env` file based on `.env.example`:

```env
DB_NAME=Wave
DB_USER=sohyp
DB_PASSWORD=123##abc##456;
DB_HOST=localhost
```

Make sure MySQL is running and the database exists before starting the app.

## Running the Backend

From the project root:

```bash
cd backend
uvicorn app.main:app --reload
```

The app will be available by default at:

```text
http://127.0.0.1:8000
```

## Main API Endpoints

### Users

- `POST /users/signup` → register a user with profile image
- `POST /users/login` → login using name and phone number
- `GET /users/{user_name}` → fetch user profile details
- `PUT /users/profile_update` → update profile using cookie auth
- `DELETE /users/delete` → delete a user account using cookie auth

### Root

- `GET /` → simple health/home endpoint

## Notes

This backend is already structured for a social app and is intentionally modular, so it can be extended easily for:

- real-time chat with WebSockets
- richer post APIs
- likes/comments
- better auth with JWT
- deployment to production servers

## Summary

ChatWave Backend is the server foundation for a modern social messaging platform. It combines FastAPI, SQLAlchemy, MySQL, and media upload handling to create a strong base for user management, content, and future chat features.

Built to be practical, scalable, and easy to extend.

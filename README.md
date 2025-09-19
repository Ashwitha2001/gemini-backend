# Gemini Backend – Online Chat & Subscription Platform

# Project Overview

Gemini Backend is a Django-based backend system for a chat application integrated with Gemini AI. It supports user authentication, chatrooms, message handling (async AI replies), subscriptions via Stripe, and rate-limiting for basic/free users.
The system is designed to be scalable, modular, and ready for deployment on cloud platforms like Render.

# Table of Contents

1. Features
2. Tech Stack
3. Architecture Overview
4. Queue System (Celery + Redis)
5. Gemini API Integration
6. Assumptions & Design Decisions
7. Setup & Run Instructions
8. Testing via Postman
9. Deployment & Access


## Features

* **Authentication**
  *  Sign up, login, OTP verification, forgot/change password
    
* **User Management**
  *  `/user/me/` to get authenticated user details
    
* **Chatrooms**
  * Create, list (cached in Redis), view details
  * Send messages with async Gemini AI replies via Celery
    
* **Subscriptions**
  * Upgrade to Pro plan using Stripe (mocked or real)
  * Rate-limiting for Basic users (5 messages/day)
    
* **Admin Panel**
  * Monitor subscriptions, chatrooms, messages
    
* **Caching & Async**
  * Redis caching for `/chatroom/` list
  * Celery worker for AI message handling


## Tech Stack

* **Backend:** Django 5.x, Django REST Framework (DRF)
* **Async Tasks:** Celery 5.x
* **Cache & Rate Limiting:** Redis
* **Database:** PostgreSQL (production)
* **Authentication:** JWT with DRF SimpleJWT
* **Payments:** Stripe (mocked integration)
* **Deployment:** Render


## Architecture Overview

User --HTTP--> Django REST APIs --Database--> PostgreSQL
                     |         
                     |--Redis Cache (chatroom list)
                     |
                     |--Celery Queue---> Gemini API ---> DB


* User requests hit DRF endpoints.
* Chatroom list is cached per user in Redis (TTL 5–10 mins).
* Messages are pushed to Celery worker for async AI processing.
* Responses from Gemini API are stored in DB and returned asynchronously.


## Queue System (Celery + Redis)

* Redis acts as a broker and result backend for Celery.
* Flow:
  1. User sends a message → saved in DB
  2. Task pushed to Celery queue
  3. Worker calls Gemini API
  4. AI reply saved in DB asynchronously
* Enables non-blocking user experience and scales with multiple workers.


## Gemini API Integration
* Each user message triggers a Celery task.
* Worker calls Gemini AI API(chat model).
* Response includes:
  * `content`
  * `created_at`
  * `role` (model)
* Stored in Message model and linked to the chatroom.


## Assumptions & Design Decisions
* Free users (Basic plan) limited to 5 messages/day.
* Subscription period: Pro plan valid for 30 days from upgrade.
* Gemini API used for asynchronous responses to ensure responsiveness.
* Redis TTL for cached chatrooms: 10 minutes.
* Stripe integration is mocked, real checkout would require a Stripe account.


## Setup & Run Instructions

# Prerequisites
* Python 3.12.8
* PostgreSQL
* Redis
* Git

# Clone Repository
```bash
git clone https://github.com/Ashwitha2001/gemini-backend.git
cd gemini-backend
```

# Install Dependencies
```bash
pip install -r requirements.txt
```

# Environment Variables

Create `.env` file:
```
STRIPE_SECRET_KEY=stripesecretkey
STRIPE_PUBLISHABLE_KEY=stripepublishablekey
STRIPE_WEBHOOK_SECRET=stripewebhookkey
STRIPE_PRICE_PRO_ID=strpepriceid
REDIS_URL=redis://localhost:6379/0
```

# Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser 
```

# Run Development Server
```bash
python manage.py runserver
```

# Start Celery Worker
```bash
celery -A gemini_backend worker -l info -P solo
```

# Testing via Postman
* Import Postman collection: `Gemini Backend APIs.postman_collection`
* Set environment variable for **JWT token**:

  * Key: `Authorization`
  * Value: `Bearer <your_token_here>`
    
* Test all endpoints:
  * `/auth/*`
  * `/user/me`
  * `/chatroom/*`
  * `/subscribe/pro`
  * `/webhook/stripe`
  * `/subscription/status`


# Deployment & Access

* **Render Public URL:** [https://gemini-backend-eldp.onrender.com](https://gemini-backend-eldp.onrender.com)
* **Access Admin Panel:** `/admin` (use superuser credentials)
* **Environment Variables** configured in Render settings.


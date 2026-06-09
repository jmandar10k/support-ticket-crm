# Support CRM with AI Assistant

A modern customer support CRM built with FastAPI, MySQL, JavaScript, and AI-powered ticket assistance. The platform streamlines support operations through ticket management, email-to-ticket automation, status tracking, authentication, and intelligent ticket insights.

## Features

### Authentication & Security

* User Signup and Login
* Password Hashing using BCrypt
* JWT-based Authentication
* Protected API Endpoints
* Auto Logout on Invalid/Expired Tokens

### Ticket Management

* Create Support Tickets Manually
* Search and Filter Tickets
* Update Ticket Status
* Add Internal Notes
* Track Complete Ticket Lifecycle

### Status Timeline Tracking

Every ticket maintains a status history:

```text
Open → In Progress → Closed
```

All status changes are recorded with timestamps, providing full visibility into ticket progression.

### Email-to-Ticket Automation

* Gmail Integration using Gmail API
* Automatic Ticket Creation from Emails
* Duplicate Email Detection
* Email Content Cleaning Pipeline
* New emails only are imported during synchronization

### AI Ticket Assistant

Built-in AI assistant powered by Groq LLM that can:

* Summarize ticket information
* Answer ticket-related questions
* Provide support insights
* Assist support agents with faster resolution

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* MySQL
* JWT Authentication
* Gmail API
* Groq API

### Frontend

* HTML
* CSS
* JavaScript

### Database

* MySQL

## System Architecture

```text
User
  │
  ▼
Frontend (HTML/CSS/JS)
  │
  ▼
FastAPI Backend
  │
  ├── Authentication (JWT)
  ├── Ticket Management
  ├── AI Assistant (Groq)
  ├── Email Sync Service
  │
  ▼
MySQL Database
```

## Key Highlights

* End-to-end authentication system
* Automated email ticket generation
* AI-powered ticket assistant
* Status timeline tracking
* Notes history management
* MySQL-backed persistence
* Production-ready architecture

## Project Structure

```text
backend/
├── main.py
├── auth.py
├── gmail_service.py
├── email_cleaner.py
├── models.py
└── schemas.py

frontend/
├── templates/
├── static/

.env
requirements.txt
README.md
```

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_mysql_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

## Installation

```bash
git clone <repository_url>

cd support-crm

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

## Future Enhancements

* Role-Based Access Control (Admin / Agent)
* Email Notifications
* Attachment Support
* Analytics Dashboard
* Customer Portal
* Multi-Agent Assignment System

## Author

Mandar Joshi

Electronics & Telecommunication Engineer | AI Developer | Founder - TuringTechLabs

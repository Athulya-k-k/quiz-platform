Quiz Platform - RESTful Backend API

A comprehensive Django REST API backend for a quiz platform with role-based access control, supporting both admin and normal user functionalities.
Features
👨‍💼 Admin Users

User registration and authentication
Create and manage quiz categories
Create and manage quizzes
Add questions with 4 multiple choice options
Activate/deactivate quizzes and questions
View all user submissions and scores
Full CRUD operations on all entities

👤 Normal Users

User registration and authentication
View all active quizzes
Submit quiz answers
View personal quiz submission history
Automatic score calculation
Duplicate submission prevention

Tech Stack

Backend Framework: Django 5.0.4
API Framework: Django REST Framework 3.15.2
Authentication: JWT (djangorestframework-simplejwt)
Database: SQLite (default, easily configurable)
CORS: django-cors-headers

Installation & Setup
Prerequisites

Python 3.8+
pip

1. Clone the Repository
bashgit clone <repository-url>
cd quiz-platform
2. Create Virtual Environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt
4. Database Setup
python manage.py makemigrations
python manage.py migrate
5. Create Superuser (Optional)
bashpython manage.py createsuperuser
6. Run Development Server
bashpython manage.py runserver
The API will be available at http://127.0.0.1:8000/


API Endpoints

🔐 Authentication Endpoints

POST /api/auth/register/ - User registration (Public Access)

Register new admin or normal users

POST /api/auth/login/ - User login (Public Access)

Login and get JWT tokens

POST /api/auth/token/refresh/ - Refresh JWT token (Public Access)

Get new access token using refresh token

GET /api/auth/profile/ - Get user profile (Authenticated Users)

Get current user information

📂 Category Endpoints

GET /api/categories/ - List all categories (Authenticated Users)

View all quiz categories

POST /api/categories/ - Create category (Admin Only)

Create new quiz category

GET /api/categories/{id}/ - Get category details (Authenticated Users)

View specific category information

PUT/PATCH /api/categories/{id}/ - Update category (Admin Only)

Modify existing category

DELETE /api/categories/{id}/ - Delete category (Admin Only)

Remove category from system

📝 Quiz Endpoints

GET /api/quizzes/ - List quizzes (Authenticated Users)

Normal users see only active quizzes

Admins see all quizzes

POST /api/quizzes/ - Create quiz (Admin Only)

Create new quiz in a category

GET /api/quizzes/{id}/ - Get quiz with questions (Authenticated Users)

View quiz details and questions

Normal users don't see correct answers

PUT/PATCH /api/quizzes/{id}/ - Update quiz (Admin Only)

Modify quiz information

DELETE /api/quizzes/{id}/ - Delete quiz (Admin Only)

Remove quiz from system

❓ Question Endpoints

GET /api/quizzes/{quiz_id}/questions/ - List questions for quiz (Admin Only)

View all questions in a specific quiz

POST /api/quizzes/{quiz_id}/questions/ - Add question to quiz (Admin Only)

Create new question with 4 options

GET /api/questions/{id}/ - Get question details (Admin Only)

View specific question information

PUT/PATCH /api/questions/{id}/ - Update question (Admin Only)

Modify question or options

DELETE /api/questions/{id}/ - Delete question (Admin Only)

Remove question from quiz

📊 Submission Endpoints

POST /api/quizzes/{quiz_id}/submit/ - Submit quiz answers (Normal Users Only)

Submit answers for a quiz attempt

GET /api/my-submissions/ - Get user's submissions (Authenticated Users)

View personal quiz submission history

GET /api/all-submissions/ - Get all submissions (Admin Only)

View all user submissions across platform

GET /api/submissions/{id}/ - Get submission details (Owner/Admin)

View detailed submission with answers

API Usage Examples
User Registration
jsonPOST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "is_admin": false
}
User Login
jsonPOST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
Response:
json{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "is_admin": false
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
Create Category (Admin)
jsonPOST /api/categories/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "General Knowledge",
    "description": "Questions about general knowledge topics"
}
Create Quiz (Admin)
jsonPOST /api/quizzes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Basic Science Quiz",
    "description": "Test your basic science knowledge",
    "category": 1,
    "is_active": true
}
Add Question (Admin)
jsonPOST /api/quizzes/1/questions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "question_text": "What is the chemical symbol for water?",
    "option_a": "H2O",
    "option_b": "CO2",
    "option_c": "NaCl",
    "option_d": "O2",
    "correct_answer": "A",
    "is_active": true
}
Submit Quiz (Normal User)
jsonPOST /api/quizzes/1/submit/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "answers": [
        {
            "question_id": "1",
            "selected_answer": "A"
        },
        {
            "question_id": "2",
            "selected_answer": "B"
        }
    ]
}
Authentication
This API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:
Authorization: Bearer <your_access_token>
Token Lifecycle:

Access tokens expire after 60 minutes
Refresh tokens expire after 7 days
Use refresh token to get new access token

Refresh Token Usage:
jsonPOST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "<your_refresh_token>"
}
User Roles & Permissions
Admin Users (is_admin: true)

✅ Full CRUD access to categories, quizzes, and questions
✅ Can view all user submissions
✅ Can activate/deactivate quizzes and questions
❌ Cannot submit quiz answers (business logic restriction)

Normal Users (is_admin: false)

✅ Read-only access to active quizzes and categories
✅ Can submit quiz answers (once per quiz)
✅ Can view only their own submissions
❌ Cannot create or modify quizzes/questions
❌ Cannot view other users' submissions

Database Models
User Model

Extends Django's AbstractUser
Additional is_admin boolean field
Tracks creation and update timestamps

Category Model

Name and description fields
Created by admin users only
Related to multiple quizzes

Quiz Model

Title, description, and category
is_active flag for visibility control
Contains multiple questions
Tracks total questions count

Question Model

Question text and 4 multiple choice options
Correct answer (A, B, C, or D)
is_active flag for individual question control
Belongs to a specific quiz

QuizSubmission Model

Links user to quiz attempt
Stores score and total questions
Prevents duplicate submissions
Calculates percentage score

SubmissionAnswer Model

Individual question answers
Selected answer and correctness flag
Automatic validation on save

Testing with Postman
Environment Setup
Create a new environment in Postman with:

Variable: base_url = http://127.0.0.1:8000
Variable: access_token = (will be set after login)

Testing Flow
Step 1: User Management

Register an admin user with is_admin: true
Register a normal user with is_admin: false
Login with both users to get JWT tokens

Step 2: Admin Setup

Create categories using admin token
Create quizzes in those categories
Add questions to quizzes with 4 options each

Step 3: User Interaction

Login as normal user
Get list of active quizzes
View specific quiz (questions without correct answers)
Submit quiz answers
View submission history

Step 4: Admin Monitoring

Login as admin
View all user submissions
Check detailed submission answers

Common Headers
Authorization: Bearer {{access_token}}
Content-Type: application/json
Development Configuration
Settings Overview

DEBUG: True (disable for production)
CORS: Allows all origins (configure for production)
Database: SQLite (easily changeable)
JWT Tokens: 60min access, 7day refresh

Security Features

Custom permission classes
Role-based access control
JWT token authentication
Password validation
Duplicate submission prevention

Project Structure
quiz_platform/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                   # Documentation
├── quiz_platform/              # Main project directory
│   ├── __init__.py
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI server config
│   └── asgi.py                 # ASGI server config
├── users/                      # User management app
│   ├── __init__.py
│   ├── models.py               # Custom User model
│   ├── serializers.py          # User data serializers
│   ├── views.py                # Authentication views
│   ├── urls.py                 # User-related URLs
│   ├── admin.py                # Django admin config
│   ├── apps.py                 # App configuration
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migrations
└── quiz_app/                   # Quiz functionality app
    ├── __init__.py
    ├── models.py               # Quiz, Question, Submission models
    ├── serializers.py          # Quiz data serializers
    ├── views.py                # Quiz operation views
    ├── urls.py                 # Quiz-related URLs
    ├── permissions.py          # Custom permission classes
    ├── admin.py                # Django admin config
    ├── apps.py                 # App configuration
    ├── tests.py                # Unit tests
    └── migrations/             # Database migrations
Error Handling
The API returns appropriate HTTP status codes:

200 OK: Successful GET, PUT, PATCH requests
201 Created: Successful POST requests
400 Bad Request: Invalid data or validation errors
401 Unauthorized: Missing or invalid authentication
403 Forbidden: Insufficient permissions
404 Not Found: Resource not found
500 Internal Server Error: Server-side errors

Common Error Responses
Authentication Error:
json{
    "detail": "Authentication credentials were not provided."
}
Permission Error:
json{
    "detail": "You do not have permission to perform this action."
}
Validation Error:
json{
    "field_name": [
        "This field is required."
    ]
}
Production Considerations
Before deploying to production:

Security:

Set DEBUG = False
Configure ALLOWED_HOSTS
Use environment variables for sensitive data
Update CORS settings



#  Finance Backend API

##  Project Overview

This is a backend system built using Flask that manages financial records with secure authentication and role-based access control.

The system allows different users to interact with data based on their roles and provides summary insights for a dashboard.

---

Features

* JWT Authentication (Login system)
* Role-Based Access Control (Admin, Analyst, Viewer)
* User Management APIs
* Financial Records CRUD (Create, Read, Update, Delete)
* Dashboard Analytics (Income, Expense, Net Balance)

---

##  Tech Stack

* Python (Flask)
* SQLite Database
* SQLAlchemy ORM
* Flask-JWT-Extended

---

## Roles & Permissions

| Role    | Permissions                   |
| ------- | ----------------------------- |
| Admin   | Full access (users + records) |
| Analyst | View records + dashboard      |
| Viewer  | View-only access              |

---

## API Endpoints

### Authentication

* POST /login → Generate JWT token

### Users

* POST /users → Create user (Admin only)
* GET /users → Get all users (Admin only)

### Records

* POST /records → Add record (Admin only)
* GET /records → View records (All roles)
* PUT /records/{id} → Update record (Admin only)
* DELETE /records/{id} → Delete record (Admin only)

### Dashboard

* GET /dashboard → Get financial summary

---

##  Dashboard Logic

* Total Income = Sum of all income records
* Total Expense = Sum of all expense records
* Net Balance = Income - Expense

---

## Setup Instructions

1. Clone the repository
2. Install dependencies
3. Run the app

```bash
python app.py
```

4. Use Postman to test APIs

---

## Assumptions

* Simplified authentication (username only)
* SQLite used for lightweight database
* Roles are predefined (admin, analyst, viewer)

---

## Conclusion

This project demonstrates backend development skills including API design, authentication, role-based authorization, and financial data processing.

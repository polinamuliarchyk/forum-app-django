# Django Discussion Forum 

**Author:** Palina Muliarchyk  
**Project Type:** Pet project

## Project Overview
A fully functional multi-user forum application built with Python and Django. This project demonstrates the implementation of a classic **Model-View-Template (MVT)** architecture, featuring nested relationships between users, topics, and comments.

## Key Features
* **User Authentication:** Complete registration, login, and logout flow using Django's built-in Auth system.
* **Content Management:** Users can create new discussion threads and post comments.
* **Relational Database:** Optimized schema with ForeignKey relationships linking Articles and Comments.
* **Admin Dashboard:** Integrated Django Admin panel for easy moderation and data management.
* **Responsive UI:** Clean and intuitive interface styled with Bootstrap.

## Tech Stack
* **Framework:** Django
* **Language:** Python
* **Frontend:** Django Templates, Bootstrap 5
* **Database:** SQLite (Development) / PostgreSQL (Production ready)

## Installation & Local Setup

### 1. Clone the repository
Extract the project files into your chosen directory or clone the repo.

### 2.  Create a virtual environment (Recommended)
``` bash
python -m venv venv
```

#### Activation:
* Windows: venv\Scripts\activate
* Linux/Mac: source venv/bin/activate

### 3. Install dependencies
``` bash 
pip install -r requirements.txt
```

### 4. Database Migrations
``` bash
python manage.py migrate
```

### 5. Create a Superuser (for Admin access)
``` bash
python manage.py createsuperuser
```
### 6. Run the server
``` bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the forum in action!
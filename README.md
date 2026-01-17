# International Student Marketplace (Flask)

This project is a full-stack web application built with Flask that provides a marketplace and information hub for international students. It includes user authentication, product listings, admin management, order handling, and messaging between users. The application is designed as a functional MVP that demonstrates real-world backend patterns such as role-based access, CRUD operations, relational models, and modular routing.

## Features

Authentication  
Users can register, log in, and log out. Admin users have elevated privileges.

Marketplace  
Users can browse products, view details, create listings, manage their own listings, upload media, and interact with products through cart and checkout flows.

Admin Panel  
Admins can:
- View all products  
- Approve or reject listings  
- Soft delete or permanently delete content  
- View all orders  
- Access user activity  

Orders and Cart  
Users can add items to cart, place orders, and view their order history. Quantity handling and stock validation are supported.

Info Hub  
Admins can create and manage articles. Users can browse, search, and bookmark content.

Messaging  
Buyers and sellers can communicate through a simple internal messaging system.

## Tech Stack

- Python 3  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-Login  
- SQLite (local development)  
- HTML + Jinja templates  
- Bootstrap for UI  

The project is structured to make migration to PostgreSQL and deployment straightforward.

## Project Structure (High Level)

- `app/` – Core application package  
  - `models/` – SQLAlchemy models  
  - `routes/` – Blueprints for auth, marketplace, admin, infohub  
  - `templates/` – Jinja HTML templates  
  - `forms.py` – WTForms definitions  
  - `utils.py` – Decorators and helpers  
- `migrations/` – Database migration history  
- `run.py` – Application entry point  
- `requirements.txt` – Dependencies  

## Running Locally

### Prerequisites
- Python 3.10 or higher  
- pip  
- Git (optional)  

### Setup

Create and activate virtual environment:

Windows (cmd):
```bash
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Database setup
```bash
Set Flask app:
```
Windows (PowerShell):
```bash
$env:FLASK_APP="run.py"
```
Mac/Linux:
```bash
export FLASK_APP=run.py
```
Run migrations:
```bash
flask db upgrade
```
(Optional) Create admin and seed sample data:
```bash
flask create-admin
flask seed
```
Run the app
```bash
python run.py
```
Open in browser:
http://127.0.0.1:5000

### Development Notes

- SQLite is used for development simplicity.

- Models and migrations are compatible with PostgreSQL.

- Role-based access is implemented using decorators.

- The admin panel is custom-built to demonstrate control over architecture.

- The project focuses on backend logic and system design rather than UI polish.

### Future Improvements

- PostgreSQL integration

- Cloud file storage (S3 or similar)

- API layer (FastAPI or Flask REST)

- React frontend

- Payment integration

- CI/CD pipeline

- Deployment on cloud platforms
# intl_student_marketplace_repo

<<<<<<< HEAD
# intl_student_marketplace_repo
=======
# StudentMarket (Flask) — International Student Marketplace + Info Hub

This is a complete local MVP web app:
- Auth (register/login/logout)
- Marketplace (browse/search, product detail, create listing, my listings)
- Admin approval flow for listings
- Cart + demo checkout (creates an order; no payments)
- Info Hub (articles, categories, search, bookmarks)
- Messaging (buyer ↔ seller chat + inbox)

## 1) Run locally (Windows / macOS / Linux)

### Prereqs
- Python 3.10+ recommended
- Git (optional)

### Setup
```bash
# 1) go into repo
cd intl_student_marketplace

# 2) create venv
python -m venv .venv

# 3) activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (cmd):
.\.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# 4) install deps
pip install -r requirements.txt
```

### Configure environment
Copy `.env.example` to `.env` and update secrets:
```bash
copy .env.example .env   # Windows
# or
cp .env.example .env     # macOS/Linux
```

### Initialize DB
```bash
# set flask app
# Windows PowerShell:
$env:FLASK_APP="run.py"
# macOS/Linux:
export FLASK_APP=run.py

# create tables
flask db init
flask db migrate -m "init"
flask db upgrade
```

### Create admin + seed data
```bash
flask create-admin
flask seed
```

### Run
```bash
python run.py
```

Open: http://127.0.0.1:5000

## 2) How to use
- Register as a student (or login as admin you created)
- Student creates a listing: Marketplace → Sell (it goes to `pending`)
- Admin approves listings: Admin dashboard → Approve
- Add items to cart → Checkout (demo)
- Info Hub: Admin can publish new articles; students can bookmark

## Notes
- This uses image URLs for product images in MVP (simple + safe). Later we can implement file uploads.
- SQLite is default for local dev. For production, switch `DATABASE_URL` to PostgreSQL.
>>>>>>> 5491fee (Initial commit: StudentMarket Flask MVP)

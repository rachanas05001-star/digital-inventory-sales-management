# Digital Inventory and Sales Management System

A beginner-friendly Django mini project using SQLite, HTML, and CSS.

## Features
- Admin login (Django's built-in authentication)
- Dashboard with product count, stock value, and sales revenue
- Add, edit, and delete products
- Record sales with quantity validation
- Automatic stock reduction when a sale is recorded
- Low-stock indicators
- Sales history

## Setup on Windows (VS Code terminal)

1. Extract this ZIP file.
2. Open the extracted `DigitalInventorySalesManagement` folder in VS Code.
3. In the terminal, run:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   python manage.py makemigrations inventory
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Open `http://127.0.0.1:8000/` in your browser.
5. Log in with the superuser account you created.

## Important
- Use Python 3.10 or newer.
- Keep the terminal running while you use the website.
- This is a college mini-project starter, not a production-ready commercial system.
- Do not upload your local database or passwords publicly.

## Suggested demo
1. Log in.
2. Add a product (for example, Notebook, price 40, quantity 50).
3. Record a sale of 5 notebooks.
4. Show that stock becomes 45 and total sale is ₹200.
5. Open Sales History and the dashboard.

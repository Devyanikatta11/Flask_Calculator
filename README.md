# Flask JWT Authentication App

A simple Flask application with user authentication using JWT (JSON Web Tokens) and MySQL for data storage.

---

## 🔧 Features

- User registration and login
- JWT-based authentication
- MySQL database integration
- Password hashing (using Werkzeug)
- Utility functions (`utils.py`)
- Environment-safe configuration 

---

## 🏗️ Project Structure

/project-root
├── app.py                      # Main Flask app
├── requirements.txt            # Python dependencies
├── proj_config_template.py     # Sample config (do NOT commit real config)
├── Project/
│   └── utils.py                # Utility functions (e.g., Calculator)
├── database.sql                # SQL script to create DB schema
└── static/
    └── favicon.ico             # Optional browser tab icon

---

## 🚀 Getting Started

### 1. Clone the repository**

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2. Create and activate a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up configuration

Create a .env file in the project root directory to store environment variables (do not commit this file to version control).

Example .env:
env
Copy
Edit
JWT_SECRET_KEY=your-secret-key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD="yourpassword" 
MYSQL_DB=mydatabase
⚠️ Note: If your password contains special characters (like #, !, or spaces), wrap it in double quotes.

This .env file is loaded automatically by the app using python-dotenv.

### 5. Set up the database

# Using MySQL CLI or GUI
source path/to/database.sql

### 6. Run the app

python app.py

### 📫 API Endpoints (example)

Method	Route	Description
POST	/register	User registration
POST	/login	User login
GET	/protected	JWT-protected endpoint

⚠️ Make sure to include the JWT token in the Authorization: Bearer <token> header for protected routes.


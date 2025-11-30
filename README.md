# EB-Bill Calculation (Django)

## 📄 Project Overview  
This is a web application built using Django that allows users to calculate electricity (EB) bills based on the power units consumed. It can be used by households or small shops to estimate monthly electricity costs.

<img width="1365" height="646" alt="eb-index" src="https://github.com/user-attachments/assets/3f4c39f2-ca59-4ad5-97d9-f411074934b0" />

## 🧰 Tech Stack & Tools  
- Python (version 3.12.7)  
- Django (version 5.2.7)  
- HTML / CSS / JavaScript — for frontend templates  
- (Optional) SQLite / any other database — for development or production  
- Environment variables for configuration (SECRET_KEY, DB credentials, debug settings, etc.)
  

<img width="1358" height="689" alt="customer dashboard" src="https://github.com/user-attachments/assets/e40ef788-5ba9-4f97-980e-eaf4503c0d17" />


<img width="1364" height="679" alt="customer-bill" src="https://github.com/user-attachments/assets/47e3a05c-7f45-41dd-a417-40c812541578" />


<img width="1366" height="640" alt="meter reading" src="https://github.com/user-attachments/assets/65670455-e04a-47f6-acec-e08ce692912f" />


## 🔧 Setup & Installation  

Follow these steps to set up and run the project locally:

```bash
# 1. Clone the repository  
git clone https://github.com/your-username/your-repo-name.git  
cd your-repo-name

# 2. (Recommended) Create a virtual environment  
python3 -m venv venv  
# On Windows:
venv\\Scripts\\activate  
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies  
pip install -r requirements.txt

# 4. Create configuration file  
cp .env.example .env
# Then edit .env and add your own values (see Configuration section below)

# 5. Run database migrations  
python manage.py migrate

# 6. Start the development server  
python manage.py runserver

⚙️ Configuration
This project uses environment variables for sensitive configuration values. Copy .env.example to .env and fill in your own values. Example:
# .env

SECRET_KEY=your-very-long-secret-key-here (The `SECRET_KEY` in Django is used for cryptographic signing — sessions, CSRF protection, cookies, password resets and other security-critical functions. If this key is exposed publicly (e.g. pushed to a public GitHub repo), it becomes a security risk. For this reason, you should **never hard-code** `SECRET_KEY` or commit it to version control.  
)
DEBUG=True            # or False in production
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost     # or your DB host
DB_PORT=5432          # or your DB port

📂 Project Structure
project-root/
│
├── manage.py
├── your_app_name/        # Django app folder
│   ├── models.py
│   ├── views.py
│   ├── templates/        # HTML templates
│   ├── static/           # CSS, JS, images
│   └── ...
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

📝 Usage / Features

-Input electricity units consumed.
-Choose (or define) tariff slab / rate structure if applicable.
-Calculate and display the estimated electricity bill
-The project has a two users one is employee and another one is customer has individual signup and signin pages.
-(Optional) Extend the project to support features like:
-Storing past bills / consumption history
-Generating PDF bills
-User authentication (so each user has own history)
-Different tariff rates / slabs

✅ What is Ignored / Not Committed

-The following are excluded from version control (via .gitignore):
-Virtual environment folders (venv/, .venv/, etc.)
-Local database files (e.g. SQLite files)
-Environment / configuration files with sensitive data (.env, secret configs)
-Compiled and cache files (__pycache__/, .pyc, etc.)
-OS / IDE / editor-specific files (e.g. .DS_Store, .vscode/, etc.)

🤝 Contributing

-Fork the repository
-Create a feature branch: git checkout -b feature/YourFeature
    git checkout -b feature/YourFeature
-Make your changes
-Stage and commit:
    git add .
    git commit -m "Add some feature"
-Push to your branch:
    git push origin feature/YourFeature
-Create a Pull Request explaining your changes

📜 License & Disclaimer

This project is intended for educational / demonstration purposes. Use it as you like — but if you deploy in a production environment, review the code carefully, manage secrets properly, and adjust configurations (e.g. DEBUG, allowed hosts, database, etc.) as needed.

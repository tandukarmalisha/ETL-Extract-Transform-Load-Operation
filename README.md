# ETL-Extract-Transform-Load-Operation
PostgreSQL ETL Engine : A high-performance Python script for migrating 10k+ rows from Excel to Postgres. Built for speed and reliability, it features batch processing, regex-based data cleaning, and automated error reporting.
🚀 PostgreSQL ETL Engine
A high-performance Python pipeline designed to clean, validate, and migrate large Excel datasets into PostgreSQL.

✨ Key Features
Batch Processing: Processes data in chunks (1,000 rows) to maximize speed and minimize memory usage.

Data Normalization: Automated cleaning for names (Title Case), phone numbers (Digits only), and email domains.

Validation & Error Tracking: Instead of crashing on bad data, it generates a user_error_report.txt pinpointing exactly which Excel rows need fixing.

System Logging: Keeps a technical "diary" of the import process in import_log.log.

🛠️ Setup & Installation
Clone the repo:
Bash:
git clone https://github.com/tandukarmalisha/ETL-Extract-Transform-Load-Operation.git
cd ETL-Extract-Transform-Load-Operation

Install Dependencies:
Bash:
pip install -r requirements.txt

Configure Environment: Create a .env file in the root folder:
Then include the following:
DB_HOST=localhost
DB_NAME=your_db
DB_USER=postgres
DB_PASS=your_password

🚀 Usage
Simply run the script and provide the path to your Excel file:

Bash
python etl.py data_10000.xlsx

📁 Project Structure
1. etl.py - The core engine and data cleaning logic.

2. requirements.txt - Required Python packages.

3. .env.example - Template for database credentials.

4. .gitignore - Prevents sensitive data and logs from being uploaded.

💡 Why I built this
This project was developed to solve the problem of "dirty data" and slow insertion speeds when moving massive Excel sheets to relational databases. It ensures that the database remains the "Single Source of Truth" with clean, standardized records.

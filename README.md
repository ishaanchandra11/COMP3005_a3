COMP3005 A3 – PostgreSQL CRUD (Python)

This project uses PostgreSQL and a Python CLI to list, add, update by student_id, and delete by student_id.

Prerequisites

PostgreSQL installed locally (with pgAdmin).

Python 3.10+.

Your Postgres user (usually postgres) and password.

Project layout

db/create_students.sql

db/seed_students.sql

app/main.py

requirements.txt

README.md

Step 1: open a terminal in the project root
Windows PowerShell recommended. The project root is the folder that contains db and app.

Step 2: create and activate a virtual environment, then install dependencies
py -m venv .venv
..venv\Scripts\Activate.ps1
pip install -r requirements.txt

Step 3: set database connection environment variables for this session
$env:PGDATABASE = "comp3005_a3"
$env:PGUSER = "postgres"
$env:PGPASSWORD = "YOUR_POSTGRES_PASSWORD"
$env:PGHOST = "localhost"
$env:PGPORT = "5432"

Step 4: create the database and load schema and seed

Set password for noninteractive calls:
$env:PGPASSWORD = "YOUR_POSTGRES_PASSWORD"

Run these commands (adjust version if needed):
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -h localhost -p 5432 -U postgres -d postgres -c "DROP DATABASE IF EXISTS comp3005_a3;"
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -h localhost -p 5432 -U postgres -d postgres -c "CREATE DATABASE comp3005_a3;"
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -h localhost -p 5432 -U postgres -d comp3005_a3 -f db/create_students.sql
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -h localhost -p 5432 -U postgres -d comp3005_a3 -f db/seed_students.sql

Verify:
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -h localhost -p 5432 -U postgres -d comp3005_a3 -c "SELECT * FROM students ORDER BY student_id;"

Step 5: run the CLI (CRUD)

List all students
python .\app\main.py list

Add a student (email must be unique)
python .\app\main.py add --first-name Alex --last-name Rivera --email demo.alex@example.com
 --date 2023-09-03

Update that student’s email by student_id
Replace N with the id printed by the add command.
python .\app\main.py update-email --id N --email demo.alex.r@example.com

Delete that student by student_id
python .\app\main.py delete --id N

List again to verify
python .\app\main.py list

Optional helper commands (only if you added them to main.py)
Update email by old email
python .\app\main.py update-email-by-email --old-email demo.alex@example.com
 --new-email demo.alex.r@example.com

Delete by email
python .\app\main.py delete-by-email --email demo.alex.r@example.com

Useful SQL in pgAdmin
SELECT * FROM students;
SELECT * FROM students ORDER BY student_id;
SELECT student_id FROM students WHERE email = 'demo.alex@example.com';
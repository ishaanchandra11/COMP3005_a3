import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import argparse

def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("PGDATABASE", "comp3005_a3"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    )

def getAllStudents():
    # Retrieve all students ordered by student_id
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id;
            """
        )
        return cur.fetchall()

def addStudent(first_name, last_name, email, enrollment_date):
    # Insert a new student and return the generated student_id
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id;
            """,
            (first_name, last_name, email, enrollment_date),
        )
        new_id = cur.fetchone()[0]
        return new_id

def updateStudentEmail(student_id, new_email):
    # Update a student's email using student_id
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE students
            SET email = %s
            WHERE student_id = %s;
            """,
            (new_email, student_id),
        )
        return cur.rowcount

def deleteStudent(student_id):
    # Delete a student by student_id
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        return cur.rowcount

def main():
    parser = argparse.ArgumentParser(
        description="Students CRUD CLI (PostgreSQL)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # list
    sub.add_parser("list", help="List all students")

    # add
    p_add = sub.add_parser("add", help="Add a new student")
    p_add.add_argument("--first-name", required=True)
    p_add.add_argument("--last-name", required=True)
    p_add.add_argument("--email", required=True, help="Must be unique")
    p_add.add_argument("--date", required=True, help="Enrollment date (YYYY-MM-DD)")

    # update by id
    p_upd = sub.add_parser("update-email", help="Update a student's email by student_id")
    p_upd.add_argument("--id", type=int, required=True)
    p_upd.add_argument("--email", required=True, help="New unique email")

    # delete by id
    p_del = sub.add_parser("delete", help="Delete a student by student_id")
    p_del.add_argument("--id", type=int, required=True)

    # NEW: update by old email
    p_upd2 = sub.add_parser("update-email-by-email", help="Update a student's email using the old email")
    p_upd2.add_argument("--old-email", required=True)
    p_upd2.add_argument("--new-email", required=True)

    # NEW: delete by email
    p_del2 = sub.add_parser("delete-by-email", help="Delete a student by email")
    p_del2.add_argument("--email", required=True)

    args = parser.parse_args()

    try:
        if args.cmd == "list":
            print_rows(getAllStudents())
            return 0

        elif args.cmd == "add":
            sid = addStudent(args.first_name, args.last_name, args.email, args.date)
            print(f"Inserted student_id={sid}")
            print_rows(getAllStudents())
            return 0

        elif args.cmd == "update-email":
            n = updateStudentEmail(args.id, args.email)
            print(f"Rows updated: {n}")
            rows = [r for r in getAllStudents() if r["student_id"] == args.id]
            print_rows(rows)
            return 0 if n else 1

        elif args.cmd == "delete":
            n = deleteStudent(args.id)
            print(f"Rows deleted: {n}")
            print_rows(getAllStudents())
            return 0 if n else 1

        elif args.cmd == "update-email-by-email":
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute("SELECT student_id FROM students WHERE email = %s;", (args.old_email,))
                row = cur.fetchone()
                if not row:
                    print(f"No student found with email={args.old_email}")
                    return 1
                sid = row[0]
            n = updateStudentEmail(sid, args.new_email)
            print(f"Rows updated: {n}")
            rows = [r for r in getAllStudents() if r["student_id"] == sid]
            print_rows(rows)
            return 0 if n else 1

        elif args.cmd == "delete-by-email":
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute("DELETE FROM students WHERE email = %s;", (args.email,))
                n = cur.rowcount
            print(f"Rows deleted: {n}")
            print_rows(getAllStudents())
            return 0 if n else 1

        else:
            parser.print_help()
            return 2

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
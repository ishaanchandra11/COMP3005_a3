-- Create the table per assignment spec (re-runnable)
DROP TABLE IF EXISTS students;

CREATE TABLE students (
  student_id       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name       TEXT    NOT NULL,
  last_name        TEXT    NOT NULL,
  email            TEXT    NOT NULL UNIQUE,
  enrollment_date  DATE
);

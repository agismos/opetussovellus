CREATE TABLE students (id SERIAL PRIMARY KEY, realname TEXT, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'student');
CREATE TABLE teachers (id SERIAL PRIMARY KEY, realname TEXT, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'teacher');
CREATE TABLE usernames (id SERIAL PRIMARY KEY, username TEXT UNIQUE);

CREATE TABLE courses (id SERIAL PRIMARY KEY, course_name TEXT, teacher_id INTEGER, teacher_username TEXT, contents TEXT);

CREATE TABLE enrollments (id SERIAL PRIMARY KEY, course_id INTEGER REFERENCES courses(id), course_name TEXT, student_username TEXT REFERENCES students(username), teacher_username TEXT REFERENCES teachers(username));

CREATE TABLE mathematics (id SERIAL PRIMARY KEY, course_name TEXT, teacher_id INTEGER REFERENCES teachers, task1 TEXT, task2 TEXT, task3 TEXT);
CREATE TABLE english (id SERIAL PRIMARY KEY, course_name TEXT, teacher_id INTEGER REFERENCES teachers, task1 TEXT, task2 TEXT, task3 TEXT);
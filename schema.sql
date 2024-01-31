CREATE TABLE students (id SERIAL PRIMARY KEY, realname TEXT, username TEXT, password TEXT, role TEXT DEFAULT 'student');
CREATE TABLE teachers (id SERIAL PRIMARY KEY, realname TEXT, username TEXT, password TEXT, role TEXT DEFAULT 'teacher');

CREATE TABLE students (id SERIAL PRIMARY KEY, realname TEXT, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'student');
CREATE TABLE teachers (id SERIAL PRIMARY KEY, realname TEXT, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'teacher');
CREATE TABLE usernames (id SERIAL PRIMARY KEY, username TEXT UNIQUE);
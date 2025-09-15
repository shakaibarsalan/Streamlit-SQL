-- Create database
CREATE DATABASE IF NOT EXISTS test_db;

-- Switch to that database
USE test_db;

-- Create a simple employees table
CREATE TABLE IF NOT EXISTS employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10,2)
);

-- Insert sample data
INSERT INTO employees (emp_id, name, department, salary) VALUES
(1, 'Alice Johnson', 'HR', 50000.00),
(2, 'Bob Smith', 'Engineering', 75000.00),
(3, 'Charlie Brown', 'Marketing', 60000.00),
(4, 'Diana Prince', 'Engineering', 85000.00),
(5, 'Ethan Hunt', 'Finance', 70000.00);

-- Create another table for testing joins
CREATE TABLE IF NOT EXISTS departments (
    dept_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

-- Insert departments
INSERT INTO departments (dept_id, department_name) VALUES
(1, 'HR'),
(2, 'Engineering'),
(3, 'Marketing'),
(4, 'Finance');

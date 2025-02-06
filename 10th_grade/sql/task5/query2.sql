DROP VIEW upt_employees;

CREATE VIEW upt_employees AS
SELECT emp.emp_name, dp.dept_name, salary * 12 as year_salary
FROM employees as emp
LEFT JOIN departments as dp ON dp.dept_id = emp.dept_id;

SELECT * FROM upt_employees;
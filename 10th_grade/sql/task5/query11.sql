CREATE VIEW copy_emps AS
SELECT * FROM employees;

INSERT into copy_emps(salary, dept_id) values (200, 2);

DROP VIEW v_high_salary;

CREATE VIEW v_high_salary AS
SELECT * FROM employees
where salary > 10000;

select * from v_high_salary;
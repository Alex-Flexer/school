drop view salary_rating;
CREATE VIEW salary_rating AS
SELECT
    emp.emp_id,
    emp.emp_name,
    row_number() over (order by salary desc) as raing
FROM employees as emp;

SELECT sr.emp_id, sr.emp_name, emp.salary, sr.raing from salary_rating as sr
left join employees as emp on emp.emp_id = sr.emp_id;


CREATE view average_position_salary as
SELECT
    emp.emp_name,
    emp.salary,
    emp.position,
    avg(salary) over (partition by position) as avg_position_salary
FROM employees as emp
left join departments as dp on dp.dept_id = emp.dept_id;

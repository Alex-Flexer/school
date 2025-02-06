SELECT
    emp.emp_name,
    dp.dept_name,
    avg(salary) over (partition by dp.dept_id) as avg_salary
FROM employees as emp
left join departments as dp on dp.dept_id = emp.dept_id;
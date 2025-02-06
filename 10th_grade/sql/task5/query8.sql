SELECT
    emp.emp_name,
    emp.salary,
    dp.dept_name,
    DENSE_RANK() over (order by dp.dept_id, salary desc) as num
FROM employees as emp
left join departments as dp on dp.dept_id = emp.dept_id;
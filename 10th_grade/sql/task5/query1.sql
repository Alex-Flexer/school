drop view avg_salary;
create view avg_salary as
select
    dp.dept_id,
    avg(emp.salary) as salary
from employees as emp
left join departments as dp on emp.dept_id = dp.dept_id
group by dp.dept_id;

create view v_employee_info as
SELECT
    emp_name,
    emp.salary,
    dp.dept_name
from employees as emp
left join departments as dp
on dp.dept_id = emp.dept_id
left join avg_salary as avs
on emp.dept_id = avs.dept_id
where emp.salary > avs.salary;
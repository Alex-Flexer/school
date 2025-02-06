select emp_name, salary, lag(salary) over(order by salary desc) salary_comp
from employees;
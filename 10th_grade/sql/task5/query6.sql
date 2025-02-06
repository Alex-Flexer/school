SELECT
*,
rank() over (order by salary desc) as row_num 
FROM employees;
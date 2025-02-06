SELECT
*,
row_number() over (order by salary desc) as row_num 
FROM employees;
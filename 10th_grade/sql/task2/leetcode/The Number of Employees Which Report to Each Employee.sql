SELECT
    t.reports_to as employee_id,
    (SELECT tt.name FROM Employees as tt WHERE tt.employee_id = t.reports_to) as name,
    (SELECT COUNT(t.name) FROM Employees as tt WHERE tt.employee_id = t.reports_to) as reports_count,
    ROUND(AVG(t.age)) as average_age
FROM Employees AS t
GROUP BY t.reports_to
HAVING NOT t.reports_to IS NULL
ORDER BY employee_id ASC;
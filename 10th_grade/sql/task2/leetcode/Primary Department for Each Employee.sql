SELECT t.employee_id, t.department_id
FROM Employee as t
WHERE
    t.primary_flag = "Y" OR
    (
        SELECT COUNT(tt.employee_id)
        FROM Employee AS tt
        WHERE tt.employee_id = t.employee_id
    ) = 1;
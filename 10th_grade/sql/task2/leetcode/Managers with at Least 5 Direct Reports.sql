SELECT t1.name
FROM Employee as t1
JOIN Employee as t2
ON t1.id = t2.managerId
GROUP BY t1.id
HAVING count(*) >= 5;
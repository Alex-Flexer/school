SELECT "Low Salary" as category, low_t.amount as accounts_count
FROM (SELECT COUNT(t.income) as amount FROM Accounts as t WHERE t.income < 20000) as low_t

UNION ALL

SELECT "Average Salary" as catetory, avg_t.amount as accounts_count
FROM (SELECT COUNT(t.income) as amount FROM Accounts as t WHERE t.income <= 50000 AND t.income >= 20000) as avg_t

UNION ALL

SELECT "High Salary" as catetory, high_t.amount as accounts_count
FROM (SELECT COUNT(t.income) as amount FROM Accounts as t WHERE t.income > 50000) as high_t;
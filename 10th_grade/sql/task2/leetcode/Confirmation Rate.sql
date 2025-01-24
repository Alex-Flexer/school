SELECT
    t1.user_id,
    IFNULL(ROUND(t2.confirmed_count / t2.total_count, 2), 0.00) AS confirmation_rate
FROM Signups AS t1
LEFT JOIN (
    SELECT
        user_id,
        COUNT(CASE WHEN action = 'confirmed' THEN 1 END) AS confirmed_count,
        COUNT(*) AS total_count
    FROM Confirmations
    GROUP BY user_id) AS t2
ON t1.user_id = t2.user_id;

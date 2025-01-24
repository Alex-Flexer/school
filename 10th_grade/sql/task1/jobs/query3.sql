SELECT Major
FROM recent_grads
WHERE ShareWomen >= 0.5 AND ShareWomen <= 0.8
ORDER BY ShareWomen DESC
LIMIT 10;

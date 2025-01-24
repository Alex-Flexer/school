SELECT Major, (1 - ShareWomen) * 100 AS "ShareMen_%"
FROM recent_grads
GROUP BY Major;

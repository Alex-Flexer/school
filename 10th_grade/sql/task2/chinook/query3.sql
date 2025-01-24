SELECT
  cus.first_name,
  cus.last_name,
  SUM(inv.total) AS summary_bills
FROM customer AS cus
JOIN invoice AS inv
ON cus.customer_id = inv.customer_id
GROUP BY cus.customer_id
ORDER BY summary_bills DESC;

SELECT * 
FROM task
WHERE (name LIKE '%' || ? || '%') OR (author LIKE '%' || ? || '%');
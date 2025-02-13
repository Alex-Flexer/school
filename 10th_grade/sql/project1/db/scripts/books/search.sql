SELECT * 
FROM books
WHERE (name LIKE '%' || ? || '%') OR (author LIKE '%' || ? || '%');
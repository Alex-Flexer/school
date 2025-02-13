SELECT b.id, b.name, b.author, b.edition, b.publication_year
FROM debtors as d
LEFT JOIN books AS b ON b.id = d.book_id
WHERE d.user_id = ?;
SELECT b.id, b.name, b.author, b.publication_year, b.edition, b.wardrobe_id, b.shelf_id FROM books as b
LEFT JOIN debtors AS d ON d.book_id = b.id
WHERE d.user_id IS NULL;
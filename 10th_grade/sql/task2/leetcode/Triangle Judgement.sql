SELECT x, y, z,
    CASE
        WHEN x + y <= z OR y + z <= x OR z + x <= y
        THEN 'No' ELSE 'Yes' END AS triangle
FROM triangle;
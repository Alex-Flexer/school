SELECT title from titles as tit
LEFT JOIN film_genres as fg ON fg.title_id = tit.title_id
LEFT JOIN genre_types as gt ON gt.id = fg.genre_id
LEFT JOIN rating as rt ON rt.title_id = tit.title_id
GROUP BY title
HAVING count(gt.genre_name) = 2 AND rt.votes > 100000
ORDER BY rt.rating DESC
LIMIT 10;

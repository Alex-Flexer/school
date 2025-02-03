SELECT * from titles as tit
LEFT JOIN film_genres as fg ON tit.title_id = fg.title_id
LEFT JOIN genre_types as gt ON fg.genre_id = gt.id
WHERE premiered >= 2019 AND gt.genre_name = 'Comedy'
LIMIT 10;

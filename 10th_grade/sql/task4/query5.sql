SELECT title, rt.rating, rt.votes from titles as tit
LEFT JOIN film_types as ft ON ft.id = tit.type
LEFT JOIN film_genres as fg ON fg.title_id = tit.title_id
LEFT JOIN genre_types as gt ON gt.id = fg.genre_id
LEFT JOIN rating as rt ON rt.title_id = tit.title_id
WHERE
ft.film_type = 'movie' AND
gt.genre_name = 'Comedy' AND
rt.rating > 8 and rt.votes > 100000;
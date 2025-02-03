WITH actors_counts(name, genres_count) AS
(
    SELECT pep.name, count(gt.genre_name) as cnt
    FROM titles AS tit
    LEFT JOIN crew as cr ON cr.title_id = tit.title_id
    LEFT JOIN people as pep ON pep.person_id = cr.person_id
    LEFT JOIN film_genres as fg ON fg.title_id = tit.title_id
    LEFT JOIN genre_types as gt ON gt.id = fg.genre_id
    GROUP BY pep.name
    HAVING pep.name IS NOT NULL and cnt > 100
)

select
    tit.title,
    tit.premiered,
    rt.rating,
    group_concat(gt.genre_name) as genres,
    count(DISTINCT ac.name) as count_actors,
    group_concat(DISTINCT ac.name) as actors
from actors_counts as ac
LEFT JOIN people as pep ON pep.name = ac.name
LEFT JOIN crew as cr on pep.person_id = cr.person_id
LEFT JOIN titles as tit on tit.title_id = cr.title_id
LEFT JOIN rating as rt on rt.title_id = tit.title_id
left join film_genres as fg on fg.title_id = tit.title_id
left join genre_types as gt on gt.id = fg.genre_id
GROUP BY tit.title
HAVING count_actors > 1
ORDER BY count_actors DESC;

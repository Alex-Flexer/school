SELECT title, premiered from titles as tit
LEFT JOIN crew as cr on tit.title_id = cr.title_id
LEFT JOIN people as pep on pep.person_id = cr.person_id
WHERE pep.name = 'Tom Hanks'
ORDER BY tit.premiered DESC;
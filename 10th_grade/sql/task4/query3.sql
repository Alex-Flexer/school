select title, pep.name, rt.rating from titles as tit
LEFT JOIN rating as rt ON rt.title_id = tit.title_id
LEFT JOIN crew as cr ON cr.title_id = tit.title_id
LEFT JOIN people as pep ON pep.person_id = cr.person_id
WHERE pep.name IN ('Tom Hanks', 'Julia Roberts', 'Natalie Portman')
ORDER BY rt.rating DESC;
select 
    pep.name,
    AVG(rt.rating) as 'average rating',
    max(rt.rating) as 'max raging',
    min(rt.rating) as 'min rating'
from titles as tit
LEFT JOIN rating as rt ON rt.title_id = tit.title_id
LEFT JOIN crew as cr ON cr.title_id = tit.title_id
LEFT JOIN people as pep ON pep.person_id = cr.person_id
WHERE pep.name IN ('Tom Hanks', 'Julia Roberts', 'Natalie Portman')
GROUP BY pep.name;
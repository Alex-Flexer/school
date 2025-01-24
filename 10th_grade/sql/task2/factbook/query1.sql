SELECT
    facts.name AS country,
    SUM(cities.population) AS summary_cities_population,
    CAST(SUM(cities.population) AS FLOAT) / 
    facts.population * 100 AS ratio_population_cities_to_total
FROM facts
JOIN cities ON facts.id = cities.facts_id
WHERE
    (NOT cities.population IS NULL) AND 
    (NOT facts.population IS NULL)
GROUP BY facts.name, facts.population;

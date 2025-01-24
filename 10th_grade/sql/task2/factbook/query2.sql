SELECT
    facts.name AS country,
    COUNT(cities.id) AS cities_amount,
    capital.name AS capital,
    capital.population AS capital_population,
    CASE
        WHEN NOT capital.population IS NULL THEN
            ROUND(CAST(capital.population AS FLOAT) / facts.population * 100, 4)
        ELSE
            NULL
    END AS ration_population_capital_to_total
FROM facts
LEFT JOIN cities
ON facts.id = cities.facts_id
LEFT JOIN cities AS capital
ON facts.id = capital.facts_id AND cities.capital = 1
GROUP BY facts.id
ORDER BY cities_amount DESC;
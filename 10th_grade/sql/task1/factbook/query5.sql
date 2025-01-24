SELECT ROUND(
            100 * CAST(population AS FLOAT) /
            (SELECT SUM(population) FROM cities),
            4
        ) AS "Population_%"
FROM cities;

SELECT *
FROM facts
WHERE
    code is NULL OR
    name is NULL OR
    area is NULL OR
    area_land is NULL OR
    area_water is NULL OR
    population is NULL OR
    population_growth is NULL OR
    birth_rate is NULL OR
    death_rate is NULL OR
    migration_rate is NULL;

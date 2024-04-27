-- SQL script that lists all bands with Glam rock as their main style
-- SELECT band_name, (IFNULL(split, YEAR(CURRENT_DATE())) - formed) AS lifespan
SELECT band_name, (IFNULL(split, 2022) - formed) as lifespan FROM metal_bands WHERE style LIKE '%Glam rock%' ORDER BY lifespan DESC;

# Write your MySQL query statement below
SELECT x, y, z, 
CASE
    WHEN 2 * GREATEST(x, y, z) < x + y + z
    THEN "Yes" ELSE "No"
    END AS triangle
FROM Triangle


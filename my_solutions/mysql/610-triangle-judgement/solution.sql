# Write your MySQL query statement below
SELECT 
  x, y, z,
  IF(2 * GREATEST(x, y, z) < x + y + z, 'Yes', 'No') AS triangle
FROM Triangle;


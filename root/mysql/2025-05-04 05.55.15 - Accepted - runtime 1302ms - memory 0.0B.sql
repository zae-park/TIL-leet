# Write your MySQL query statement below
SELECT p.name
FROM SalesPerson AS p
LEFT JOIN (
    SELECT o.sales_id
    FROM Orders AS o 
    JOIN Company AS c ON o.com_id = c.com_id
    WHERE c.name = "RED"
) AS co
ON p.sales_id = co.sales_id
WHERE co.sales_id IS NULL
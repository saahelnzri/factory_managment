USE factory_management;

SELECT p.category, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY p.category ORDER BY revenue DESC;

SELECT c.city, SUM(oi.quantity * oi.unit_price) AS revenue, COUNT(DISTINCT o.order_id) AS orders_count
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY c.city ORDER BY revenue DESC;

SELECT p.product_name, SUM(oi.quantity) AS units_sold, SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id, p.product_name ORDER BY revenue DESC LIMIT 10;

SELECT e.employee_id, CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
       d.department_name, e.salary,
       ROUND(e.salary / NULLIF(AVG(e.salary) OVER (PARTITION BY e.department_id), 0), 2) AS salary_vs_department_avg
FROM employees e JOIN departments d ON d.department_id = e.department_id;

SELECT p.product_id, p.product_name, p.stock_quantity,
       CASE WHEN p.stock_quantity < 20 THEN 'Low' WHEN p.stock_quantity < 100 THEN 'Medium' ELSE 'Healthy' END AS stock_status
FROM products p ORDER BY p.stock_quantity;

SELECT o.status, COUNT(DISTINCT o.order_id) AS order_count,
       SUM(oi.quantity * oi.unit_price) AS order_value
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.status ORDER BY order_count DESC;

USE factory_management;

CREATE OR REPLACE VIEW vw_order_detail AS
SELECT o.order_id, o.order_date, o.status, c.customer_id,
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name, c.city AS customer_city,
       oi.order_item_id, p.product_id, p.product_name, p.category,
       oi.quantity, oi.unit_price, oi.quantity * oi.unit_price AS line_total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id;

CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
       SUM(oi.quantity * oi.unit_price) AS sales_amount,
       SUM(oi.quantity) AS units_sold,
       COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m');

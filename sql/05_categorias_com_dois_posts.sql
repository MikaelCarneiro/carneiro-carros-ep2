SELECT c.id, c.name, c.description, COUNT(pc.post_id) AS post_count
FROM blog_category AS c
JOIN blog_post_categories AS pc ON pc.category_id = c.id
GROUP BY c.id, c.name, c.description
HAVING COUNT(pc.post_id) >= 2
ORDER BY c.name;

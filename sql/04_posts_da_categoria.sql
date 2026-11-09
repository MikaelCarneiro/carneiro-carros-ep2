SELECT c.id AS category_id, c.name, c.description,
       p.id AS post_id, p.title, p.content, p.published_at
FROM blog_category AS c
JOIN blog_post_categories AS pc ON pc.category_id = c.id
JOIN blog_post AS p ON p.id = pc.post_id
WHERE c.name = 'Anos 2000'
ORDER BY p.published_at DESC, p.id DESC;

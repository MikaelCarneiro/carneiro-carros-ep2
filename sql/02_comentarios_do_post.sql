SELECT c.*
FROM blog_comment AS c
JOIN blog_post AS p ON p.id = c.post_id
WHERE p.title = 'Honda Civic LX 2005'
ORDER BY c.published_at DESC, c.id DESC;

SELECT c.id, c.author_id, c.text, c.published_at,
       p.title AS post_title, p.published_at AS post_date
FROM blog_comment AS c
JOIN blog_post AS p ON p.id = c.post_id
WHERE p.title = 'Honda Civic LX 2005'
ORDER BY c.published_at DESC, c.id DESC;

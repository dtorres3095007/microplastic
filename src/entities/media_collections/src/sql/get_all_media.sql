SELECT id, title, description, date 
FROM media_collections
WHERE (
    %(search)s IS NULL OR title LIKE CONCAT('%', %(search)s, '%')
    OR description LIKE CONCAT('%', %(search)s, '%')
)
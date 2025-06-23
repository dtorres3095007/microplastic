SELECT id, 
       title, 
       summary, 
       content, 
       media_type, 
       media_url, 
       thumbnail_url, 
       published_at, 
       status 
FROM media_collections
WHERE (
    %(search)s IS NULL OR title LIKE CONCAT('%', %(search)s, '%')
    OR summary LIKE CONCAT('%', %(search)s, '%')
)
LIMIT %(limit)s OFFSET %(offset)s;
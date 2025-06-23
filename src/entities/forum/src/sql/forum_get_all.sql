SELECT	*
FROM
comments
WHERE (
    %(search)s IS NULL OR content LIKE CONCAT('%', %(search)s, '%')
)
LIMIT %(limit)s OFFSET %(offset)s;
SELECT 
	id,
	title, 
	type, 
	url, 
	thumbnail_url, 
	description
FROM media_files
WHERE (
		%(search)s IS NULL OR title LIKE CONCAT('%', %(search)s, '%')
	)
LIMIT %(limit)s OFFSET %(offset)s;
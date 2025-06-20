SELECT 
	id,
	collection_id,
	title, 
	type, 
	url, 
	thumbnail_url, 
	description
FROM media_files
WHERE collection_id = %(collection_id)s
AND (
		%(search)s IS NULL OR title LIKE CONCAT('%', %(search)s, '%')
	)
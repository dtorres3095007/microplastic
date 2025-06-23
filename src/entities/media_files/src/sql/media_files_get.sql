SELECT
    id,
	type, 
	title, 
	url, 
	thumbnail_url, 
	description 
FROM media_files
WHERE id = %(id)s

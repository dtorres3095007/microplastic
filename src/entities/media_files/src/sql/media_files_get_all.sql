SELECT collection_id, 
	type, 
	title, 
	url, 
	thumbnail_url, 
	description
FROM media_files
WHERE collection_id = %(collection_id)s

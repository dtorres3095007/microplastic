SELECT id, title, description, date 
FROM media_collections
WHERE id = %(media_id)s

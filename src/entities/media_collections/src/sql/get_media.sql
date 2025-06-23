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
WHERE id = %(media_id)s

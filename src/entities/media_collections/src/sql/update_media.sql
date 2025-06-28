UPDATE media_collections 
	SET
	title = %(title)s, 
	summary = %(summary)s, 
	content = %(content)s, 
	media_type = %(media_type)s, 
	media_url = %(media_url)s, 
	thumbnail_url = %(thumbnail_url)s, 
	published_at = %(published_at)s, 
	status = %(status)s,
	updated_at = %(updated_at)s
	WHERE
	id = %(media_id)s;
    
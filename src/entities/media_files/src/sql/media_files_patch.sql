UPDATE media_files
	SET
	type = %(type)s,
	title = %(title)s,
	url = %(url)s,
	thumbnail_url = %(thumbnail_url)s,
	description = %(description)s,
	updated_at = %(updated_at)s,
	updated_by = %(updated_by)s
	WHERE
	id = %(id)s ;
	
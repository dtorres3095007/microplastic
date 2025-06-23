UPDATE media_files
	SET
	type = %(type)s,
	title = %(title)s,
	url = %(url)s,
	thumbnail_url = %(thumbnail_url)s,
	description = %(description)s,
	uploaded_at = %(uploaded_at)s,
	uploaded_by = %(uploaded_by)s
	WHERE
	id = %(id)s ;
	
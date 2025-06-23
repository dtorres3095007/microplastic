INSERT INTO media_files 
	(
	type, 
	title, 
	url, 
	thumbnail_url, 
	description,
	uploaded_by
	)
	VALUES
	(
    %(type)s,
    %(title)s,
    %(url)s,
    %(thumbnail_url)s,
    %(description)s,
    %(uploaded_by)s
	);
	
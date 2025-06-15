INSERT INTO media_files 
	(
	collection_id, 
	type, 
	title, 
	url, 
	thumbnail_url, 
	description,
	uploaded_by
	)
	VALUES
	(
	%(collection_id)s,
    %(type)s,
    %(title)s,
    %(url)s,
    %(thumbnail_url)s,
    %(description)s,
    %(uploaded_by)s
	);
	
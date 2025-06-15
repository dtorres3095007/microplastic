UPDATE users 
	SET
	email = %(email)s,
	profile = %(profile)s,
	active = %(active)s,
	updated_by = %(updated_by)s
	WHERE
	user_id = %(user_id)s;
	
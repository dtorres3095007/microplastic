INSERT INTO users 
    (
        email, 
        password,
        created_by
	) VALUES
        (
            %(email)s, 
            %(password)s,
            %(created_by)s
        );
        
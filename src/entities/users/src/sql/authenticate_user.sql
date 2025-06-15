SELECT user_id, email, password
FROM users
WHERE email = %(email)s AND active = 1
  LIMIT 1;
  
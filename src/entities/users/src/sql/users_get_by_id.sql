SELECT user_id, email, profile, active
FROM users 
WHERE user_id = %(user_id)s; AND active = 1

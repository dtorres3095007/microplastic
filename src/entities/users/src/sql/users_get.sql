SELECT user_id, email, profile, active 
FROM users 
WHERE active = 1
AND (
    %(search)s IS NULL OR email LIKE CONCAT('%', %(search)s, '%')
)
LIMIT %(limit)s OFFSET %(offset)s
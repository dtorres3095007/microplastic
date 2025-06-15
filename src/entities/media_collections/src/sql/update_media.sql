UPDATE media_collections
SET
    title = %(title)s,
    description = %(description)s,
    date = %(date)s,
    updated_by = %(updated_by)s
WHERE id = %(media_id)s

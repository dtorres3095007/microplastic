summary_forum_get_all = ("Get All Forum Posts",)

description_forum_get_all = """
    This endpoint retrieves all forum posts from the database. It supports pagination and optional search functionality.
    You can specify the maximum number of posts to return, the number of posts to skip, and an optional search term to filter posts by content.
    The default values for pagination are 10 posts per page, starting from the first post (offset 0).
    The search term is optional and can be used to filter posts based on their content.
    """

response_description_forum_get_all = (
    "The response will include a list of forum posts, each containing the post ID, content, author name, and creation date."
    "If no posts are found, the response will indicate that no forum posts were found."
)

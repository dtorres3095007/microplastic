summary_login = "Authenticate user and issue access tokens"

description_login = (
    "Receives user credentials (email and password), "
    "validates them against the authentication backend, "
    "and issues a JWT access token and refresh token if the credentials are correct. "
    "These tokens can be used for accessing protected endpoints."
)

response_description_login = "Returns a JWT access token and a refresh token if authentication is successful"

summary_create = "Create a new user"

description_create = (
    "Receives user details (email, password), "
    "creates a new user in the system, and returns the created user's details. "
    "This endpoint is typically used for user registration."
)

response_description_create = (
    "Returns the details of the newly created user."
)

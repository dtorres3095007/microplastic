from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.users.src.queries import UsersQueries
from src.shared.db_config import DatabaseConnection
import bcrypt


class Users:
    def __init__(self, conn: DatabaseConnection):
        self.users_queries = UsersQueries()
        self.conn = conn

    def login_user(self, email: str, password: str) -> tuple:
        """
        This method will authenticate a user based on email and password.

        args:
            email (str): The email of the user.

        Returns:
            tuple: The status code and response message.
        """
        user = self.users_queries.authenticate_user(
            email=email,
            conn=self.conn,
        )

        if not user:
            return STATUS_BAD_REQUEST, {"message": "Invalid email or password"}
        
        stored_password = user[0]["password"].encode("utf-8")
        provided_password = password.encode("utf-8")

        if not bcrypt.checkpw(provided_password, stored_password):
            return STATUS_BAD_REQUEST, {"message": "Invalid email or password"}
        
        del user[0]["password"]

        return STATUS_OK, {"message": "User authenticated successfully", "user": user}
    
    def create_user(self, email: str, password: str) -> tuple:
        """
        This method will create a new user with the provided email and password.

        args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            tuple: The status code and response message.
        """
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
        user = self.users_queries.create_user(
            email=email,
            password=hashed_password.decode("utf-8"),
            conn=self.conn,
        )

        if not user:
            return STATUS_BAD_REQUEST, {"message": "User creation failed"}
        
        return STATUS_OK, {"message": "User created successfully", "email": email}
    
    def get_users(self) -> tuple:
        """
        This method will retrieve the user data.

        Returns:
            tuple: The status code and response message.
        """
        user = self.users_queries.get_users(
            conn=self.conn,
        )

        if not user:
            return STATUS_BAD_REQUEST, {"message": "User not found"}
        
        return STATUS_OK, {"message": "User retrieved successfully", "user": user}
    
    def get_user_by_id(self, user_id: int) -> tuple:
        """
        This method will retrieve a user by their ID.

        args:
            user_id (int): The ID of the user.

        Returns:
            tuple: The status code and response message.
        """
        user = self.users_queries.get_user_by_id(
            user_id=user_id,
            conn=self.conn,
        )

        if not user:
            return STATUS_BAD_REQUEST, {"message": "User not found"}
        
        return STATUS_OK, {"message": "User retrieved successfully", "user": user}
    
    def patch_user(self, user_id: int, email: str = None, profile: str = None, active: str = None) -> tuple:
        """
        This method will update a user's details.

        args:
            user_id (int): The ID of the user.
            email (str): The new email of the user.
            password (str): The new password of the user.

        Returns:
            tuple: The status code and response message.
        """
        if not email:
            return STATUS_BAD_REQUEST, {"message": "No fields to update"}

        user = self.users_queries.patch_user(
            user_id=user_id,
            email=email,
            profile=profile,
            active=active,
            conn=self.conn,
        )

        if not user:
            return STATUS_BAD_REQUEST, {"message": "User update failed"}
        
        return STATUS_OK, {"message": "User updated successfully", "user": user}
    
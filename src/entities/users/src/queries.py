from src.shared.db_config import DatabaseConnection
from src.shared.decorators.query_reader import sql_query_reader
import os
from typing import Optional
from datetime import datetime


base_dir = os.path.dirname(os.path.abspath(__file__))


class UsersQueries:
    @sql_query_reader(base_dir, "authenticate_user.sql")
    def authenticate_user(
        self,
        email: str,
        conn: DatabaseConnection,
    ) -> Optional[dict]:
        """
        This method will authenticate a user based on email and password.

        args:
            email (str): The email of the user.
            password (str): The password of the user.
            conn (DatabaseConnection): The database connection object.

        Returns:
            dict: The user data if authentication is successful.
            None: If authentication fails.
        """
        query: str = self.authenticate_user.query
        params = {
            "email": email,
        }
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "users_create_post.sql")
    def create_user(
        self,
        email: str,
        password: str,
        profile: str,
        conn: DatabaseConnection,
    ) -> Optional[dict]:
        """
        This method will create a new user with the provided email and password.

        args:
            email (str): The email of the user.
            password (str): The password of the user.
            conn (DatabaseConnection): The database connection object.

        Returns:
            dict: The user data if creation is successful.
            None: If creation fails.
        """
        query: str = self.create_user.query
        params = {
            "email": email,
            "password": password,
            "profile": profile,
            "created_by": 1,
        }
        resp = conn.execute_update(query, params)
        return resp

    @sql_query_reader(base_dir, "users_get.sql")
    def get_users(
        self,
        conn: DatabaseConnection,
        limit: int,
        offset: int,
        search: Optional[str],
    ) -> Optional[dict]:
        """
        This method will retrieve a user by their ID.

        args:
            conn (DatabaseConnection): The database connection object.

        Returns:
            dict: The user data if found.
            None: If no user is found with the given ID.
        """
        query: str = self.get_users.query
        params = {
            "limit": limit,
            "offset": offset,
            "search": search if search else None,
        }
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "users_get_by_id.sql")
    def get_user_by_id(
        self,
        user_id: int,
        conn: DatabaseConnection,
    ) -> Optional[dict]:
        """
        This method will retrieve a user by their ID.

        args:
            user_id (int): The ID of the user.
            conn (DatabaseConnection): The database connection object.

        Returns:
            dict: The user data if found.
            None: If no user is found with the given ID.
        """
        query: str = self.get_user_by_id.query
        params = {
            "user_id": user_id,
        }
        resp = conn.execute_query(query, params)
        return resp

    @sql_query_reader(base_dir, "users_patch.sql")
    def patch_user(
        self,
        user_id: int,
        email: str,
        profile: str,
        active: str,
        conn: DatabaseConnection,
        updated_by: int = 1,
    ) -> Optional[dict]:
        """
        This method will update a user by their ID.
        args:
            user_id (int): The ID of the user.
            email (str): The new email of the user.
            conn (DatabaseConnection): The database connection object.
        Returns:
            dict: The updated user data if the update is successful.
            None: If the update fails or no user is found with the given ID.
        """
        query: str = self.patch_user.query
        params = {
            "user_id": user_id,
            "email": email,
            "profile": profile,
            "active": active,
            "updated_at": datetime.now(),
            "updated_by": updated_by,
        }
        resp = conn.execute_update(query, params)
        return resp

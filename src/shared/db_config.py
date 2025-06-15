import os
import logging
from mysql.connector import pooling, Error
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self):
        try:
            self.db_host = os.getenv("DATABASE_HOST")
            self.db_user = os.getenv("DATABASE_USER")
            self.db_password = os.getenv("DATABASE_PASSWORD")
            self.db_database = os.getenv("DATABASE_NAME")
            self.db_port = int(os.getenv("DATABASE_PORT"))
            self.pool_size = int(os.getenv("DB_POOL_SIZE", 5))

            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=self.pool_size,
                pool_reset_session=True,
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_database,
                port=self.db_port,
            )
            logger.info("Connection pool created successfully with size %d", self.pool_size)
        except Error as err:
            logger.error("Error initializing the connection pool: %s", err)

    def connect(self):
        """
        Establishes a connection to the database from the connection pool and creates a cursor.

        Returns:
            tuple: (connection, cursor) or (None, None) if connection fails
        """
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            logger.info("Connection and cursor obtained from pool")
            return connection, cursor
        except Error as err:
            logger.error("Error getting connection from pool: %s", err)
            return None, None

    def close(self, connection, cursor):
        """
        Closes the connection and cursor, returning the connection to the pool.

        Args:
            connection (object): The connection object to be closed
            cursor (object): The cursor object to be closed
        """
        try:
            if cursor:
                cursor.close()
                logger.info("Cursor closed successfully")
            if connection:
                connection.close()
                logger.info("Connection returned to the pool")
        except Error as err:
            logger.error("Error closing connection or cursor: %s", err)

    def execute_query(self, query, params=None):
        """
        Executes a SELECT query and fetches the results.

        Args:
            query (str): The SQL query to be executed
            params (tuple, optional): The parameters to be used in the query

        Returns:
            list: The results of the query
            None: If an error occurs
        """
        connection, cursor = self.connect()
        if not connection or not cursor:
            return None
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            logger.info("Query executed successfully: %s")
            return results
        except Error as err:
            logger.error("Error executing query: %s", err)
            return None
        finally:
            self.close(connection, cursor)

    def execute_update(self, query, params=None):
        """
        Executes an UPDATE query and commits the changes to the database.

        Args:
            query (str): The SQL query to be executed
            params (tuple, optional): The parameters to be used in the query

        Returns:
            bool: True if the update was successful, False otherwise
        """
        connection, cursor = self.connect()
        if not connection or not cursor:
            return False
        try:
            cursor.execute(query, params)
            connection.commit()
            logger.info("Update executed and committed successfully: %s", query)
            return True
        except Error as err:
            logger.error("Error executing update: %s", err)
            return False
        finally:
            self.close(connection, cursor)
            
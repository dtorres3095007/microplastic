import pytest
from unittest.mock import patch, MagicMock
from mysql.connector import Error
from src.shared.db_config import DatabaseConnection


# ----------------------------
# Test creación de pool
# ----------------------------
@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_init_connection_pool(mock_pool):
    instance = mock_pool.return_value
    db = DatabaseConnection()
    mock_pool.assert_called_once()
    assert db.connection_pool == instance


# ----------------------------
# Test connect()
# ----------------------------
@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_connect_success(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    conn, cursor = db.connect()

    assert conn == mock_conn
    assert cursor == mock_cursor
    mock_conn.cursor.assert_called_once_with(dictionary=True)


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_connect_fail(mock_pool):
    mock_pool.return_value.get_connection.side_effect = Error("Connection failed")
    db = DatabaseConnection()
    conn, cursor = db.connect()
    assert conn is None
    assert cursor is None


# ----------------------------
# Test close()
# ----------------------------
@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_close_success(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    db = DatabaseConnection()
    db.close(mock_conn, mock_cursor)
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_close_fail(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.close.side_effect = Error("Cursor fail")
    mock_conn.close.side_effect = Error("Connection fail")
    db = DatabaseConnection()
    db.close(mock_conn, mock_cursor)


# ----------------------------
# Test execute_query()
# ----------------------------
@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_execute_query_success(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "Test"}]
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    result = db.execute_query("SELECT * FROM table")

    assert result == [{"id": 1, "name": "Test"}]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM table", None)
    mock_cursor.fetchall.assert_called_once()


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_execute_query_fail(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Error("Query failed")
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    result = db.execute_query("SELECT * FROM table")
    assert result is None


# ----------------------------
# Test execute_update()
# ----------------------------
@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_execute_update_success(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    success = db.execute_update("UPDATE table SET col=1")
    assert success is True
    mock_conn.commit.assert_called_once()
    mock_cursor.execute.assert_called_once_with("UPDATE table SET col=1", None)


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_execute_update_fail(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Error("Update fail")
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    success = db.execute_update("UPDATE table SET col=1")
    assert success is False


# ----------------------------
# Test executemany_insert()
# ----------------------------
@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_executemany_insert_success(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    batch = [(1, "a"), (2, "b")]
    success = db.executemany_insert("INSERT INTO table VALUES (%s,%s)", batch)
    assert success is True
    mock_cursor.executemany.assert_called_once_with(
        "INSERT INTO table VALUES (%s,%s)", batch
    )
    mock_conn.commit.assert_called_once()


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_executemany_insert_fail(mock_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.executemany.side_effect = Error("Insert fail")
    mock_conn.cursor.return_value = mock_cursor
    mock_pool.return_value.get_connection.return_value = mock_conn

    db = DatabaseConnection()
    batch = [(1, "a"), (2, "b")]
    success = db.executemany_insert("INSERT INTO table VALUES (%s,%s)", batch)
    assert success is False


@patch("mysql.connector.pooling.MySQLConnectionPool", side_effect=Error("Pool fail"))
def test_init_connection_pool_fail(mock_pool):
    import logging

    with patch.object(
        logging.getLogger("src.shared.db_config"), "error"
    ) as mock_logger_error:
        db = DatabaseConnection()
        mock_logger_error.assert_called_with(
            "Error initializing the connection pool: %s", mock_pool.side_effect
        )


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_execute_query_no_connection(mock_pool):
    mock_pool.return_value.get_connection.side_effect = Error("Connection fail")
    db = DatabaseConnection()
    result = db.execute_query("SELECT * FROM table")
    assert result is None


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_execute_update_no_connection(mock_pool):
    mock_pool.return_value.get_connection.side_effect = Error("Connection fail")
    db = DatabaseConnection()
    success = db.execute_update("UPDATE table SET col=1")
    assert success is False


@patch("mysql.connector.pooling.MySQLConnectionPool")
def test_executemany_insert_no_connection(mock_pool):
    mock_pool.return_value.get_connection.side_effect = Error("Connection fail")
    db = DatabaseConnection()
    success = db.executemany_insert("INSERT INTO table VALUES (%s,%s)", [(1, "a")])
    assert success is False


def test_close_with_none(monkeypatch):
    from src.shared import db_config

    db = db_config.DatabaseConnection()
    db.close(None, None)

"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 03.09.24
Latest update: 24.09.24
Version : 0.2

Description:    this file contains the code for
                connection the database to the game.
"""

# Imports
import mysql.connector
import tkinter
from tkinter import messagebox

# functions ...
# ...to open the database
import mysql.connector

def db_connection(host, user, password, database):
    """Opens a connection to the MySQL database.

    Args:
        host: The hostname of the MySQL server.
        user: The username for the database connection.
        password: The password for the database connection.
        database: The name of the database to connect to.

    Returns:
        The database connection object.
    """

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error opening database connection: {e}")
        return None

def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()


# ...get only the top score
def get_top_scores(conn):
    """Retrieves the top scores from the MySQL database.

    Args:
        conn: The database connection object.

    Returns:
        A list of tuples representing the top scores.
    """

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name.players AS player, score.games, datetime.games FROM games INNER JOIN players ON games.Players_id = players.id; ORDER BY score DESC LIMIT 10")
        top_scores = cursor.fetchall()
        return top_scores
    except mysql.connector.Error as e:
        print(f"Error getting top scores: {e}")
        return []

# ...to insert a new student in the students' data
def add_player(pseudo):
    query = "INSERT INT players (name) VALUES (%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (pseudo,))
    cursor.close()

# ...to get a student id by his pseudo
def get_player_id_by_name(pseudo):
    query = "SELECT id FROM players WHERE name = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (pseudo,))
    result_id = cursor.fetchall()
    cursor.close()
    return result_id



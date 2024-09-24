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
def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='CPNV',
                                            password='Pa$$w0rd', database='solitaire',
                                            buffered=True, autocommit=True)
# ...to close the database
def close_dbconnection():
    db_connection.close()

# ...to insert a new student in the students' data
def add_player(pseudo):
    query = "INSERT INTO players (name) VALUES (%s)"
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

# ...get only the top score
def get_top_scores():
    query = """
    SELECT
        RANK() OVER (ORDER BY Games.score DESC) AS rank,
        Players.name AS player,
        Games.score,
        Games.datetime
    FROM
        Games
    INNER JOIN
        Players ON Games.Players_id = Players.id
    ORDER BY
        Games.score DESC
    LIMIT 10;
    """

    cursor = db_connection.cursor()
    cursor.execute(query)
    top_scores = cursor.fetchall()
    cursor.close()

    return top_scores
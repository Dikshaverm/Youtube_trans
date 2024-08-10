import os
import sys
import uuid
import mysql.connector
from mysql.connector import Error
from youtube_translator.logger import logging
from youtube_translator.exception import YoutubeException
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path


class Youtube_Db:
    def __init__(self):
        self.user = os.getenv('USER_NAME')
        self.password = os.getenv('PASSWORD')
        self.host = os.getenv('HOST')
        self.database = os.getenv('DATABASE_NAME')
        self.conn = self.connect_to_db()

    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if conn.is_connected():
                logging.info("Connected to MySQL database")
                return conn
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise YoutubeException(e, sys)

    def create_database(self):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.close()

    def use_database(self):
        cursor = self.conn.cursor()
        cursor.execute(f"USE {self.database}")
        logging.info(f"Using database: {self.database}")
        cursor.close()

    def create_table(self):
        cursor = self.conn.cursor()
        table_name = os.getenv('TABLE_NAME', 'mp3_files')

        try:
            # Check if the table already exists
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            table_name_list = [table[0] for table in tables]

            if table_name not in table_name_list:
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id int PRIMARY KEY AUTO_INCREMENT,
                    sessionid varchar(255) NOT NULL,
                    filename varchar(255) NOT NULL,
                    filedata longblob NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(create_table_sql)
                logging.info(f"Table {table_name} created successfully.")
            else:
                logging.info(f"Table {table_name} already exists.")

        except Error as e:
            logging.error(f"Error creating table: {e}")
            raise YoutubeException(e, sys)

        finally:
            cursor.close()


class Mp3FileStorage:
    def __init__(self):
        logging.info("Initializing Mp3FileStorage")
        self.db = Youtube_Db()
        self.db.create_database()
        self.db.use_database()
        self.db.create_table()

    def insert_mp3_file(self, session_id: str, file_path: str, file_name: str):
        try:
            logging.info("Inserting mp3 file into the database")
            cursor = self.db.conn.cursor()

            with open(file_path, 'rb') as f:
                data = f.read()

            SQL = "INSERT INTO mp3_files (sessionid, filedata, filename) VALUES (%s, %s, %s)"
            values = (session_id, data, file_name)
            cursor.execute(SQL, values)
            self.db.conn.commit()  # Commit the transaction to save changes
            cursor.close()
            logging.info("MP3 file inserted successfully")

        except Error as e:
            logging.error(f"Error inserting mp3 file: {e}")
            self.db.conn.rollback()  # Rollback the transaction if any error occurs
            raise YoutubeException(e, sys)

    def get_mp3_file(self, session_id: str, file_name: str):
        try:
            logging.info("Fetching mp3 file from the database")
            cursor = self.db.conn.cursor()

            SQL="SELECT filedata FROM mp3_files WHERE sessionid = %s AND filename = %s"
            cursor.execute(SQL, (session_id, file_name))
            result = cursor.fetchone()

            if result:
                file_data = result[0]
                with open(os.path.join(Path(r"C:\Users\savit\PycharmProjects\Youtube_translator\data"), file_name+'.mp3'), 'wb') as f:
                    f.write(file_data)

                file_name=os.path.join(os.getcwd(), 'temp.mp3')

                with open(file_name, 'wb') as f:
                    f.write(file_data)

                logging.info(f"MP3 file {file_name} fetched successfully")

                return file_name
            else:
                logging.warning("File not found")
                file_data = None

            cursor.close()
            return file_data

        except Error as e:
            logging.error(f"Error fetching mp3 file: {e}")
            raise YoutubeException(e, sys)


import pygame
from playsound import playsound


if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    path = Path(r"C:\Users\savit\PycharmProjects\Youtube_translator\Girlfriend ｜ Stand up Comedy ｜ Aaditya Kulshreshth aka Kullu [LGXSPMfwqcs].mp3")
    file_name = str(uuid.uuid4())
    file_storage = Mp3FileStorage()
    file_storage.insert_mp3_file(session_id=session_id, file_path=path, file_name=file_name)
    logging.info(f"MP3 file stored with session_id: {session_id}")

    data = file_storage.get_mp3_file(session_id=session_id, file_name=file_name)
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(data)

    # Play the MP3 file
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass




def connect_to_db():
    try:
        logging.info("Connecting to MySQL database...")

        conn = connect(user=os.getenv('USER_NAME'),
                       password=os.getenv('PASSWORD'),
                       host=os.getenv('HOST'),
                       database=os.getenv('DATABASE_NAME')
                       )
        con = conn.cursor()

        logging.info(f"Connected to Database successfully {conn.database}")
        logging.info("Connected to MySQL database")

        con.close()

        logging.info("MySQL database connection successful")

        return conn

    except Exception as e:
        logging.error(e)
        raise e


class Mp3FileStorage:
    def __init__(self):
        logging.info("Initializing mp3_file_storage constructor component \n")
        self.db = Youtube_Db()

    def initialize_database(self):
        try:
            logging.info("Initializing database\n")
            self.db.create_database()
            self.db.use_database()
            self.db.create_table()
        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def insert_mp3_file(self, session_id: str, file_path: str, file_name: str):
        try:
            logging.info("Inserting mp3_file into the database\n")
            cursor = self.db.conn.cursor()

            with open(file_path, 'rb') as f:
                data = f.read()

            SQL = f"INSERT INTO mp3_files (sessionid , filedata , filename) VALUES (%s, %s, %s)"

            values = (session_id, data, file_name)
            cursor.execute(SQL, values)

            cursor.close()
            logging.info("Inserted mp3_file into the database\n")

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def get_mp3_file(self, session_id: str, file_name: str):
        try:
            logging.info("Fetching mp3_file from the database\n")
            cursor = self.db.conn.cursor()

            SQL = "SELECT filedata FROM mp3_files WHERE sessionid = %s AND filename = %s"

            cursor.execute(SQL, (session_id, file_name))
            result = cursor.fetchone()

            if result:
                file_data = result[0]
                with open(file_name, 'wb') as f:
                    data = f.write(file_data)
            else:
                print("File not found")

            cursor.close()
            self.db.conn.close()
            logging.info("Fetched mp3_file from the database\n")

            return data

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

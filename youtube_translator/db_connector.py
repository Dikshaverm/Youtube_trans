import os
from youtube_translator.logger import logging
from youtube_translator.exception import YoutubeException
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
logging.info('Loaded environment variables')

logging.info(f"{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}")


def connect_to_db():
    try:
        logging.info("Connecting to MySQL database...")

        conn = mysql.connector.connect(
                       user=os.getenv('USER_NAME'),
                       password=os.getenv('PASSWORD'),
                       host=os.getenv('HOST'),
                       database=os.getenv('DATABASE_NAME')
                       )
        con = conn.cursor()

        logging.info(f"Connected to Database successfully {conn.database}")
        con.close()
        logging.info("MySQL database connection successful")
        return conn

    except Exception as e:
        logging.error(e)
        raise YoutubeException(e, sys) from e


class ConnectToDb:
    def __init__(self):
        try:
            logging.info("Initializing MySQL database connection inside the ConnectToDb Class\n")
            self.user = os.getenv('USER_NAME')
            self.password = os.getenv('PASSWORD')
            self.host = os.getenv('HOST')
            self.database = os.getenv('DATABASE_NAME')
            self.conn = self.connect_to_db()
            logging.info("MySQL database connection successful\n")

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys) from e

    def connect_to_db(self):
        try:
            logging.info("Inside the ConnectToDb Class initiating connect_to_db methods.\n")
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if conn.is_connected():
                logging.info("Connected to MySQL database")
                logging.info("Exiting the ConnectToDb Class initiating connect_to_db methods\n")
                return conn

        except Exception as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise YoutubeException(e, sys)

    def create_database(self):
        try:
            logging.info("Inside the ConnectToDb Class initiating create_database methods.\n")
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def use_database(self):
        logging.info("Inside the ConnectToDb Class initiating use_database methods.\n")
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

        except Exception as e:
            logging.error(f"Error creating table: {e}")
            raise YoutubeException(e, sys)

        finally:
            cursor.close()


"""
if __name__ == '__main__':
    connect_to_db()
    logging.info("Exiting fro main Connected to MySQL database
"""

from youtube_translator.logger import logging
from youtube_translator.db_connector import ConnectToDb
from youtube_translator.exception import YoutubeException
import sys
import os
from pathlib import Path
import pygame
import uuid


class Mp3FileStorage:
    def __init__(self):
        logging.info("Initializing Mp3FileStorage")
        self.db = ConnectToDb()
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

        except Exception as e:
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

        except Exception as e:
            logging.error(f"Error fetching mp3 file: {e}")
            raise YoutubeException(e, sys)


if __name__ == "__main__":
    session_id = int(uuid.uuid1())
    path = r"C:\Users\savit\PycharmProjects\Youtube_translator\Girlfriend ｜ Stand up Comedy ｜ Aaditya Kulshreshth aka Kullu [LGXSPMfwqcs].mp3"
    file_name = str(uuid.uuid1())
    print(session_id)
    file_storage = Mp3FileStorage()
    file_storage.insert_mp3_file(session_id=session_id,
                                 file_path=path,
                                 file_name=file_name)

    data=file_storage.get_mp3_file(session_id=session_id, file_name=file_name)
    logging.info(f"Initializing mp3_file_storage constructor component with {session_id} \n")

    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(data)

    # Play the MP3 file
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass





from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor


class DB:
    @staticmethod
    def start_db():
        while True:
            try:
                conn = psycopg2.connect(host="localhost", database="FastAPI_DB", user="postgres",
                                        password="pass1234", cursor_factory=RealDictCursor)

                print("Database connection was successful!")
                curser = conn.cursor()
                return curser, conn

            except Exception as error:
                print("Database connection failed")
                print("Error: ", error)
                sleep(2)

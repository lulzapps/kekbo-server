import logging
import mysql.connector

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class DBConnector:
    def __init__(self, host, user, password, database):
        logger.debug("Connecting to database")
        self.db = mysql.connector.connect(
            host='localhost',
            user="root",
            password="rootpassword",
            database="yourdatabase",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci')
        logger.debug("Connected to database");

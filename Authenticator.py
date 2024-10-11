import logging
import mysql.connector

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class Authenticator:
    def __init__(self):
        logger.debug("Connecting to database")
        self.db = mysql.connector.connect(
            host='localhost',
            user="root",
            password="rootpassword",
            database="yourdatabase",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci')
        logger.debug("Connected to database");
        
    def authenticate(self, username, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", username)
        result = cursor.fetchall()
        for row in result:
            logger.debug(f"Found user: {row}")
        cursor.close()
        return len(result) > 0
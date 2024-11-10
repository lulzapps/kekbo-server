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
        try:
            logger.debug(f"Authenticating user [{username}] with password [{password}]")
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = cursor.fetchall()
            for row in result:
                username2 = row[1]
                password2 = row[3]
                if username == username2 and password == password2:
                    logger.debug(f"User {username} authenticated")
                    return True
            logger.debug(f"User {username} not authenticated")
            return False
        finally:
            cursor.close()

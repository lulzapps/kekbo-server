import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class SessionManager:
    def __init__(self):
        self.__sessions = []

    def add_session(self, session):
        self.__sessions.append(session)
        logger.debug(f"Added session {session}")

    def remove_session(self, session):
        self.__sessions.remove(session)
        logger.debug(f"Removed session {session}")

    def get_session_count(self):
        return len(self.__sessions)
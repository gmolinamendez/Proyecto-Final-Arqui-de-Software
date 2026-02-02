from database import database
from emailmanager import EmailManager

database = database()
emailmanager = EmailManager()

class BusinessLogic:
    def __init__(self):
        self.database = database

    def run_database_test(self):
        result = self.database.db_test()
        emailmanager.send_email(
            "gmolinamendez04@gmail.com",
            "Database Test Result",
            str(result),
        )
        print("DB Test Result:", result)
        return result